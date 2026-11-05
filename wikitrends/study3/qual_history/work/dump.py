import json,sys
d=json.load(open('/home/user/photoStamper/wikitrends/data/study3/qual_discovery.json'))
for i in map(int,sys.argv[1:]):
    x=d[i]
    print(f"===== [{i}] {x['title']} | {x['group']} | change={x['change']:.3f}")
    print("--- 2021:"); print(x['lead0'])
    print("--- 2026:"); print(x['lead1'])
    print()
