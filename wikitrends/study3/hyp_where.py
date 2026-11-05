"""WHERE / WHAT changed -- frozen hypothesis statistics (study 3).

Each h* function takes a list of articles in the discovery/holdout schema and
returns a float statistic.  Mass functions take mass-schema articles
({t,g,p,i,f,l,e,rv}); deep functions take deep-schema articles.
Run:  python3 hyp_where.py MASS_JSON DEEP_JSON [n_boot]
prints estimate, article-level bootstrap 95% CI (resampling within group) and
two-sided label-permutation p for every hypothesis.

Snapshot indices (mass): 0 = 2021-01-01, 1 = pre-war (2023-07-01), 2 = latest.
"Pre" change = 0->1, "post" change = 1->2.  Every DiD is
  (topic post - topic pre) - (comparison post - comparison pre).
Frame vector layout: x[0] = words, x[1..12] = counts in lab_frames order.
"""
import json, sys
import numpy as np

FRAMES = ['settler_colonial', 'apartheid', 'genocide', 'ethnic_cleansing', 'occupation',
          'nakba_expulsion', 'war_crimes', 'indigenous_homeland', 'persecution_antisemitism',
          'terrorism', 'militant', 'placebo_geography']
CRIT = FRAMES[:7]
IDX = {f: i + 1 for i, f in enumerate(FRAMES)}
CR_IDX = [IDX[f] for f in CRIT]
OCC_NAKBA = [IDX['occupation'], IDX['nakba_expulsion']]
GENOCIDE = [IDX['genocide']]
TAIL_THRESH = 0.5  # critical terms per 1,000 words


# ---------------------------------------------------------------- mass helpers
def _ok(a, k='f'):
    s = a.get(k)
    return s is not None and all(x is not None and x[0] > 0 for x in s)


def _cnt(x, idx=CR_IDX):
    return sum(x[i] for i in idx)


def _rate(x, idx=CR_IDX):
    return _cnt(x, idx) * 1e3 / x[0]


def _share(G, fn):
    return float(np.mean([fn(a) for a in G])) if G else float('nan')


def _did(arts, pred, k='f'):
    """pred(a, i0, i1) -> bool. DiD of share(pred) post vs pre, topic vs comparison."""
    out = {}
    for g in 'tc':
        G = [a for a in arts if a['g'] == g and _ok(a, k)]
        out[g] = _share(G, lambda a: pred(a, 1, 2)) - _share(G, lambda a: pred(a, 0, 1))
    return out['t'] - out['c']


def _up(idx, k='f'):
    return lambda a, i0, i1: _cnt(a[k][i1], idx) > _cnt(a[k][i0], idx)


# ---------------------------------------------------------------- H1 (mass)
def h1_tail_share_did(arts):
    """DiD in share of articles whose full-text critical rate rose by > 0.5 per 1k words."""
    return _did(arts, lambda a, i0, i1: _rate(a['f'][i1]) - _rate(a['f'][i0]) > TAIL_THRESH)


def h1b_any_gain_did(arts):
    """Sensitivity: DiD in share of articles gaining >= 1 critical-term mention (net count up)."""
    return _did(arts, _up(CR_IDX))


def h1c_net_gain_did(arts):
    """Sensitivity: DiD in (share count up - share count down)."""
    return _did(arts, lambda a, i0, i1: (_cnt(a['f'][i1]) > _cnt(a['f'][i0])) - (_cnt(a['f'][i1]) < _cnt(a['f'][i0])))


def h1_placebo_did(arts):
    """Artefact check: same as h1b for the placebo_geography frame (should be ~0)."""
    return _did(arts, _up([IDX['placebo_geography']]))


# ---------------------------------------------------------------- H2 (mass)
def h2_occnakba_minus_genocide(arts):
    """DiD(share gaining occupation/nakba_expulsion terms) - DiD(share gaining genocide terms). >0 predicted."""
    return _did(arts, _up(OCC_NAKBA)) - _did(arts, _up(GENOCIDE))


def h2_occnakba_did(arts):
    return _did(arts, _up(OCC_NAKBA))


def h2_genocide_did(arts):
    return _did(arts, _up(GENOCIDE))


# ---------------------------------------------------------------- H3 (mass, lead)
def h3_lead_any_gain_did(arts):
    """DiD in share of LEADS gaining >= 1 critical-term mention (articles with all 3 lead snapshots)."""
    return _did(arts, _up(CR_IDX, 'l'), k='l')


# ---------------------------------------------------------------- H4 (mass, WikiProject)
def _within_t_change(G):
    G = [a for a in G if _ok(a)]
    f = _up(CR_IDX)
    return _share(G, lambda a: f(a, 1, 2)) - _share(G, lambda a: f(a, 0, 1))


def h4_ip_minus_judaism(arts):
    """(post-pre share gaining crit terms) in Israel+Palestine projects minus same in Judaism project."""
    ip = [a for a in arts if a['g'] == 't' and a['p'] in ('Israel', 'Palestine')]
    ju = [a for a in arts if a['g'] == 't' and a['p'] == 'Judaism']
    return _within_t_change(ip) - _within_t_change(ju)


def h4b_judaism_vs_comparison(arts):
    """Judaism project vs all comparison articles (predicted ~0; equivalence bound +/-0.03)."""
    ju = [a for a in arts if a['g'] == 't' and a['p'] == 'Judaism']
    c = [a for a in arts if a['g'] == 'c']
    return _within_t_change(ju) - _within_t_change(c)


# ---------------------------------------------------------------- H5 (salience)
def h5_mass_importance_gradient(arts):
    """[DiD Top/High - DiD Mid] within topic minus same within comparison, using h1b's outcome."""
    def ch(g, imps):
        return _within_t_change([a for a in arts if a['g'] == g and a['i'] in imps])
    return (ch('t', 'TH') - ch('t', 'M')) - (ch('c', 'TH') - ch('c', 'M'))


def h5_mass_importance_TH_did(arts):
    """Simpler: DiD restricted to Top+High importance articles (t vs c)."""
    return h1b_any_gain_did([a for a in arts if a['i'] in ('T', 'H')])


# ---------------------------------------------------------------- deep helpers
DEEP_DATES = ['%d-%02d' % (y, m) for y in range(2021, 2027) for m in (1, 4, 7, 10)]


def _deep_ok(a):
    return (not a['created_in_window']) and a['group'] in ('treatment', 'control')


def _aligned(a, ser):
    m = dict(zip(a['crit_series_dates'], ser)); out = []; last = None
    for d in DEEP_DATES:
        if m.get(d) is not None:
            last = m[d]
        out.append(last)
    return out


def _deep_counts(a):
    cols = [_aligned(a, a['frame_series'][f]) for f in CRIT]
    return np.array([sum((c[i] or 0) for c in cols) for i in range(len(DEEP_DATES))], float)


def _deep_hazard_change(a):
    """Share of post quarters (2023-07..2026-10) with critical count up minus share of pre quarters (2021-01..2023-07)."""
    up = np.diff(_deep_counts(a)) > 0
    return up[10:].mean() - up[:10].mean()


def h6_deep_addition_hazard_did(arts):
    """Deep: mean per-article change in quarterly 'addition hazard', treatment minus control."""
    A = [a for a in arts if _deep_ok(a)]
    t = [_deep_hazard_change(a) for a in A if a['group'] == 'treatment']
    c = [_deep_hazard_change(a) for a in A if a['group'] == 'control']
    return float(np.mean(t) - np.mean(c))


def h6b_deep_addition_hazard_topic_only(arts):
    A = [a for a in arts if _deep_ok(a) and a['group'] == 'treatment']
    return float(np.mean([_deep_hazard_change(a) for a in A]))


def _pre_edits(a):
    return sum(v for q, v in (a.get('quarter_edits') or {}).items() if q < '2023-Q4')


def _salience_gap(G):
    pe = np.array([_pre_edits(a) for a in G]); c = [_deep_counts(a) for a in G]
    up = np.array([x[-1] > x[10] for x in c])
    hi = pe > np.median(pe)
    return up[hi].mean() - up[~hi].mean()


def h7_deep_salience_interaction(arts):
    """Deep: [share gaining crit count 2023-07->end, above- minus below-median pre-war edits] treatment minus control."""
    A = [a for a in arts if _deep_ok(a)]
    return float(_salience_gap([a for a in A if a['group'] == 'treatment']) -
                 _salience_gap([a for a in A if a['group'] == 'control']))


# ---------------------------------------------------------------- rejected
def r1_deep_fulltext_tail(arts):
    """REJECTED: share with crit1-crit0 > 5 per 10k, treatment minus control (deep)."""
    A = [a for a in arts if _deep_ok(a) and a['crit0'] is not None]
    s = lambda g: np.mean([a['crit1'] - a['crit0'] > 5 for a in A if a['group'] == g])
    return float(s('treatment') - s('control'))


def r2_genocide_carries(arts):
    """REJECTED: share of the h1b effect that disappears when genocide is dropped (1 = genocide carries all)."""
    full = h1b_any_gain_did(arts)
    nog = _did(arts, _up([i for i in CR_IDX if i != IDX['genocide']]))
    return 1 - nog / full


# ---------------------------------------------------------------- inference
MASS = [h1_tail_share_did, h1b_any_gain_did, h1c_net_gain_did, h1_placebo_did,
        h2_occnakba_minus_genocide, h2_occnakba_did, h2_genocide_did, h3_lead_any_gain_did,
        h4_ip_minus_judaism, h4b_judaism_vs_comparison, h5_mass_importance_gradient,
        h5_mass_importance_TH_did, r2_genocide_carries]
DEEP = [h6_deep_addition_hazard_did, h6b_deep_addition_hazard_topic_only,
        h7_deep_salience_interaction, r1_deep_fulltext_tail]


def _boot(fn, arts, key, n, rng):
    groups = {}
    for a in arts:
        groups.setdefault(a[key], []).append(a)
    out = []
    for _ in range(n):
        s = []
        for G in groups.values():
            s += [G[j] for j in rng.integers(0, len(G), len(G))]
        out.append(fn(s))
    return np.nanpercentile(out, [2.5, 97.5])


def _perm(fn, arts, key, n, rng, obs):
    labels = [a[key] for a in arts]; c = 0
    for _ in range(n):
        lab = rng.permutation(labels)
        s = [dict(a, **{key: l}) for a, l in zip(arts, lab)]
        c += abs(fn(s)) >= abs(obs) - 1e-12
    return (c + 1) / (n + 1)


def main(mass_path, deep_path, n=1000):
    rng = np.random.default_rng(20261105)
    mass = json.load(open(mass_path))['articles']
    deep = json.load(open(deep_path))['articles']
    for fns, arts, key in ((MASS, mass, 'g'), (DEEP, deep, 'group')):
        for fn in fns:
            obs = fn(arts)
            ci = _boot(fn, arts, key, n, rng)
            if fn in (h4_ip_minus_judaism, h4b_judaism_vs_comparison, h6b_deep_addition_hazard_topic_only, r2_genocide_carries):
                p = float('nan')  # within-topic / ratio stats: use CI
            else:
                p = _perm(fn, arts, key, n, rng, obs)
            print(f'{fn.__name__:34s} {obs:+.4f}  CI [{ci[0]:+.4f}, {ci[1]:+.4f}]  perm p {p:.4f}')


if __name__ == '__main__':
    D = '/home/user/photoStamper/wikitrends/data/study3/'
    arg = lambda i, d: sys.argv[i] if len(sys.argv) > i and sys.argv[i] else d
    main(arg(1, D + 'discovery_mass.json'), arg(2, D + 'discovery_deep.json'), int(arg(3, '1000')))
