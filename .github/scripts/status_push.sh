#!/usr/bin/env bash
# Push live status (heartbeat JSON + log tails) to branch wikitrends-status every INTERVAL seconds.
# Usage: status_push.sh <label> [interval]   (run in background; stops when the job ends)
LABEL="$1"; INTERVAL="${2:-180}"
DIR=/tmp/wt-status; SRC="$GITHUB_WORKSPACE/wikitrends"
git config --global user.name "wikitrends-bot"; git config --global user.email "actions@users.noreply.github.com"
rm -rf "$DIR"
if git ls-remote --exit-code --heads origin wikitrends-status >/dev/null 2>&1; then
  git clone -q --depth 1 --branch wikitrends-status "https://x-access-token:${GH_TOKEN}@github.com/${GITHUB_REPOSITORY}.git" "$DIR"
else
  mkdir -p "$DIR" && cd "$DIR" && git init -q && git checkout -q -b wikitrends-status && \
  git remote add origin "https://x-access-token:${GH_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
fi
while true; do
  OUT="$DIR/${GITHUB_RUN_ID}/${LABEL}"; mkdir -p "$OUT"
  cp "$SRC"/data/status/*.json "$OUT/" 2>/dev/null
  for f in "$SRC"/logs/*.log; do [ -f "$f" ] && tail -n 40 "$f" > "$OUT/$(basename "$f").tail"; done
  date -u +%FT%TZ > "$OUT/last_push"
  cd "$DIR" && git add -A >/dev/null 2>&1 && git commit -qm "status ${GITHUB_RUN_ID} ${LABEL}" >/dev/null 2>&1
  for i in 1 2 3; do git pull -q --rebase origin wikitrends-status >/dev/null 2>&1; git push -q origin HEAD:wikitrends-status >/dev/null 2>&1 && break; sleep 5; done
  sleep "$INTERVAL"
done
