"""Verify that every quoted string in codebook.json occurs verbatim in the discovery data."""
import json,sys
d=json.load(open(sys.argv[1])); cb=json.load(open(sys.argv[2]))
by={x['title']:x for x in d}
def texts(t):
    x=by[t]; T=[x['lead0'] or '',x['lead1'] or '']
    for e in x['first_sentence_edits'] or []: T+= [e['before'],e['after'],e['comment'] or '']
    return T
bad=0
for m in cb:
    for ex in m['examples']:
        for k in ('before','after','comment'):
            q=ex.get(k)
            if not q or q.startswith('(no '): continue
            if not any(q in s for s in texts(ex['title'])):
                bad+=1; print('NOT FOUND',m['move'][:30],ex['title'],k,q[:80])
print('missing',bad)
