import json,sys
d=json.load(open('/home/user/photoStamper/wikitrends/data/study3/qual_discovery.json'))
for i in map(int,sys.argv[1:]):
    x=d[i]; print('#####',i,x['title'],x['group'])
    for e in x['first_sentence_edits']:
        print('--',{k:v for k,v in e.items() if k not in('before','after')})
        print('  B:',e.get('before')); print('  A:',e.get('after'))
