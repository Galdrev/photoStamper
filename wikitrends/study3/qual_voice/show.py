import json,sys
d=json.load(open('/home/user/photoStamper/wikitrends/data/study3/qual_discovery.json'))
n=int(sys.argv[1])
for i in map(int,sys.argv[2:]):
    x=d[i]; print(f'\n######## [{i}] {x["title"]} ({x["group"]})\n--- BEFORE ---\n{(x["lead0"] or "")[:n]}\n--- AFTER ---\n{(x["lead1"] or "")[:n]}')
