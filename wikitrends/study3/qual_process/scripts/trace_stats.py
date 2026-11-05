import json,re,sys,difflib
from collections import Counter,defaultdict
d=json.load(open(sys.argv[1]))
CATS={
 'policy_content':r'NPOV|\bPOV\b|neutral|WP:RS|reliable|\bRS\b|\bDUE\b|UNDUE|WP:OR|\bOR\]|weight|WP:V\b|verif',
 'policy_style':r'MOS:|LEADCLUTTER|AVOIDBOLD|MOS:FIRST|LEADCITE|MTAU|boldface|CURLY|Oxford spelling|style template|SOB',
 'talk_consensus':r'per talk|talk page|discussion|consensus|RfC|\bRM\b|per FAC',
 'sources':r'source|cited|citation|scholar|per body|\brefs?\b',
 'revert':r'\brv\b|revert|undid|restore',
 'accuracy':r'accura|precise|more accurate|clarif|correct',
 'copyedit':r'\bce\b|c/e|copyedit|grammar|typo|cleanup|clean up|readab|comma|spelling|wikilink|linking|template|AWB|Monkbot|format',
}
rows=[]
for x in d:
  E=sorted(x['first_sentence_edits'] or [],key=lambda e:e['timestamp'])
  if not E: continue
  gaps=0
  for a,b in zip(E,E[1:]):
    if a['after'].strip()!=b['before'].strip(): gaps+=1
  for e in E:
    c=e['comment'] or ''
    cats=[k for k,p in CATS.items() if re.search(p,c,re.I)]
    sm=difflib.SequenceMatcher(None,e['before'].split(),e['after'].split())
    rows.append(dict(title=x['title'],group=x['group'],ts=e['timestamp'],rev=e['reverted'],empty=not c.strip(),cats=cats,wordsim=round(sm.ratio(),2),sd=e['size_delta']))
  print(f"{x['title'][:40]:40s} {x['group'][:4]} n={len(E):2d} reverted={sum(e['reverted'] for e in E)} gaps={gaps} empty={sum(not (e['comment'] or '').strip() for e in E)} span={E[0]['timestamp'][:7]}..{E[-1]['timestamp'][:7]}")
for g in ('treatment','control'):
  R=[r for r in rows if r['group']==g]
  print('\n',g,'edits',len(R),'reverted',sum(r['rev'] for r in R),'empty comment',sum(r['empty'] for r in R))
  c=Counter(k for r in R for k in r['cats']);print(dict(c))
  print('nocat',sum(1 for r in R if not r['cats'] and not r['empty']))
  print('mean word-sim',round(sum(r['wordsim'] for r in R)/len(R),3),'share sim<0.7',round(sum(r['wordsim']<0.7 for r in R)/len(R),2))
