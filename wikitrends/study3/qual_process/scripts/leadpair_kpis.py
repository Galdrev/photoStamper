"""Process-proxy KPIs computable from lead pairs alone (no revision history). Discovery half only."""
import json,re,sys,difflib,statistics as st
d=json.load(open(sys.argv[1]))
def sents(t): return [s for s in re.split(r'(?<=[.!?])\s+(?=[A-Z"(])',re.sub(r'\s+',' ',t or '').strip()) if s]
def sim(a,b): return difflib.SequenceMatcher(None,a.split(),b.split()).ratio()
ATTR=r"\b(according to|described (as|by)|accused|alleg\w+|critics?|some (scholars|historians|academics)|has been (called|termed|characteri[sz]ed|described)|considers?|regarded as|viewed as|claim(s|ed)?)\b"
DENY=r"\b(den(y|ies|ied)|disputes?|rejects?|maintains? that|negates?)\b"
CAMP=r"\b(pro-Israel|pro-Palestinian|and its (supporters|allies)|supporters of Zionism)\b"
COL=r"\bcoloni[sz]\w*|\bsettler[- ]colonial\w*"
GEN=r"\bgenocid\w*|\bethnic cleansing\b|\bapartheid\b"
ALT=r"\b(also (known|called|referred to) as|or the|officially( known as)?|abbreviated)\b"
def feat(t):
    S=sents(t); n=max(len(S),1); fs=S[0] if S else ''
    f={'chars':len(t or ''),'sents':len(S)}
    for k,p in (('attr',ATTR),('deny',DENY),('camp',CAMP),('col',COL),('gen',GEN)):
        f[k]=len(re.findall(p,t or '',re.I))/n
    f['alt_fs']=len(re.findall(ALT,fs,re.I))
    f['was_fs']=bool(re.search(r'\b(was|were)\b',fs[:200]))
    # first sentence position (index) of genocide/apartheid/colonial terms
    f['gen_pos']=min([i for i,s in enumerate(S) if re.search(GEN,s,re.I)],default=None)
    return f,fs,S
out={}
for g in ('treatment','control','control_contaminated'):
    X=[x for x in d if x['group']==g]
    rows=[]
    for x in X:
        a,fa,Sa=feat(x['lead0']); b,fb,Sb=feat(x['lead1'])
        fs_chg=1-sim(fa,fb); rest_chg=1-sim(' '.join(Sa[1:]),' '.join(Sb[1:])) if len(Sa)>1 and len(Sb)>1 else None
        rows.append(dict(fs_chg=fs_chg,rest_chg=rest_chg,len_ratio=(b['chars']+1)/(a['chars']+1),
            d_attr=b['attr']-a['attr'],d_deny=b['deny']-a['deny'],camp_new=b['camp']>0 and a['camp']==0,
            col_new=b['col']>0 and a['col']==0,gen_new=b['gen']>0 and a['gen']==0,
            gen_promoted=(a['gen_pos'] is not None and b['gen_pos'] is not None and b['gen_pos']<a['gen_pos']) or (a['gen_pos'] is None and b['gen_pos'] is not None and b['gen_pos']<=2),
            d_alt=b['alt_fs']-a['alt_fs'],tense_flip=a['was_fs']!=b['was_fs']))
    R=rows; m=lambda k:[r[k] for r in R if r[k] is not None]
    po=[r['fs_chg']-r['rest_chg'] for r in R if r['rest_chg'] is not None]
    out[g]={'n':len(R),
      'median_fs_change':round(st.median(m('fs_chg')),3),'median_rest_change':round(st.median(m('rest_chg')),3),
      'share_protected_opening(fs_chg<rest_chg-0.2)':round(sum(p< -0.2 for p in po)/len(po),3),
      'median_len_ratio':round(st.median(m('len_ratio')),2),
      'share_attr_density_up':round(sum(r['d_attr']>0 for r in R)/len(R),3),'share_attr_density_down':round(sum(r['d_attr']<0 for r in R)/len(R),3),
      'share_denial_density_up':round(sum(r['d_deny']>0 for r in R)/len(R),3),
      'share_camp_label_new':round(sum(r['camp_new'] for r in R)/len(R),3),
      'share_colonial_vocab_new':round(sum(r['col_new'] for r in R)/len(R),3),
      'share_genocide_cleansing_apartheid_new':round(sum(r['gen_new'] for r in R)/len(R),3),
      'share_gca_promoted_to_top3_sentences':round(sum(r['gen_promoted'] for r in R)/len(R),3),
      'share_altname_in_fs_up':round(sum(r['d_alt']>0 for r in R)/len(R),3),'share_altname_in_fs_down':round(sum(r['d_alt']<0 for r in R)/len(R),3),
      'share_fs_tense_flip':round(sum(r['tense_flip'] for r in R)/len(R),3)}
print(json.dumps(out,indent=1))
