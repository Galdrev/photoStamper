"""Shared, observable HTTP layer for every collector.

- One token-bucket rate limit per process (env WT_RPS, default 6 requests/second)
- Respects Retry-After / 429 / maxlag, exponential backoff
- Counters: requests, ok, http_429, http_5xx, api_errors, retries, failures, bytes, latency
- heartbeat(stage, done, total): writes data/status/<WT_JOB>.json and prints one line, at most every 30 s
"""
import json, os, threading, time

import requests

UA = "WikiFramingTrends/1.0 (https://github.com/Galdrev/photoStamper; research script) python-requests"
RPS = float(os.environ.get("WT_RPS", "6"))
JOB = os.environ.get("WT_JOB", "local")
STATUS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "status")

_S = requests.Session(); _S.headers["User-Agent"] = UA
_lock = threading.Lock()
_next = [0.0]
C = {"requests": 0, "ok": 0, "http_429": 0, "http_5xx": 0, "api_errors": 0, "retries": 0, "failures": 0,
     "bytes": 0, "latency_sum": 0.0, "started": time.time()}
_last_hb = [0.0]
_state = {"stage": "start", "done": 0, "total": 0, "extra": {}}


def _wait_slot():
    with _lock:
        now = time.time()
        t = max(now, _next[0])
        _next[0] = t + 1.0 / RPS
    if t > now:
        time.sleep(t - now)


def get_json(url, params, tries=8, ok404=False):
    """GET returning parsed JSON, or None after exhausting retries (counted as a failure)."""
    for i in range(tries):
        _wait_slot()
        t0 = time.time()
        try:
            r = _S.get(url, params=params, timeout=90)
            C["requests"] += 1; C["latency_sum"] += time.time() - t0; C["bytes"] += len(r.content)
            if r.status_code == 200:
                j = r.json()
                err = j.get("error") if isinstance(j, dict) else None
                if err:
                    C["api_errors"] += 1
                    if err.get("code") in ("maxlag", "ratelimited") or "Timeout" in str(err.get("code")):
                        C["retries"] += 1; time.sleep(min(60, 5 * (i + 1))); continue
                    return j                     # non-retryable API error: caller decides
                C["ok"] += 1
                return j
            if r.status_code == 404 and ok404:
                return None
            if r.status_code == 429:
                C["http_429"] += 1; C["retries"] += 1
                ra = int(r.headers.get("retry-after", 20) or 20)
                C["retry_after_max"] = max(C.get("retry_after_max", 0), ra); C["retry_after_sum"] = C.get("retry_after_sum", 0) + ra
                time.sleep(ra); continue
            if r.status_code >= 500:
                C["http_5xx"] += 1
            C["retries"] += 1
        except (requests.RequestException, ValueError):
            C["retries"] += 1
        time.sleep(min(60, 2 ** i))
    C["failures"] += 1
    return None


_ticker = [None]


def _tick():
    while True:
        time.sleep(60)
        try:
            heartbeat(force=True)
        except Exception:
            pass


def heartbeat(stage=None, done=None, total=None, force=False, **extra):
    if _ticker[0] is None:                       # timer heartbeat: proves liveness even when no item finishes
        _ticker[0] = threading.Thread(target=_tick, daemon=True); _ticker[0].start()
    if stage is not None: _state["stage"] = stage
    if done is not None: _state["done"] = done
    if total is not None: _state["total"] = total
    if extra: _state["extra"].update(extra)
    now = time.time()
    if not force and now - _last_hb[0] < 30:
        return
    _last_hb[0] = now
    el = now - C["started"]
    d, t = _state["done"], _state["total"]
    rate = d / el if el > 0 else 0
    eta = (t - d) / rate if rate > 0 and t else None
    st = {"job": JOB, "stage": _state["stage"], "done": d, "total": t, "elapsed_min": round(el / 60, 1),
          "eta_min": round(eta / 60, 1) if eta else None, "rps_limit": RPS,
          "req_per_s": round(C["requests"] / el, 2) if el else 0,
          "avg_latency_s": round(C["latency_sum"] / C["requests"], 2) if C["requests"] else None,
          **{k: v for k, v in C.items() if k not in ("latency_sum", "started")}, **_state["extra"],
          "updated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    os.makedirs(STATUS_DIR, exist_ok=True)
    tmp = os.path.join(STATUS_DIR, f"{JOB}.json.tmp")
    json.dump(st, open(tmp, "w"), indent=1); os.replace(tmp, os.path.join(STATUS_DIR, f"{JOB}.json"))
    print(f"[hb {JOB}] {st['stage']} {d}/{t} el={st['elapsed_min']}m eta={st['eta_min']}m "
          f"req={C['requests']} 429={C['http_429']} 5xx={C['http_5xx']} retries={C['retries']} fail={C['failures']}",
          flush=True)
