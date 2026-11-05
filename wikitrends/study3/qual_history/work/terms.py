import json,re
d=json.load(open('/home/user/photoStamper/wikitrends/data/study3/qual_discovery.json'))
T={'coloni':r'\bcoloni[sz]|\bcolonial|\bcolonist|\bcolonizer|\bcolonies\b',
'settler_col':r'settler[- ]colonial',
'ethnic_cleansing':r'ethnic cleansing',
'genocide':r'genocid',
'nakba':r'\bnakba\b',
'expel':r'\bexpel|\bexpuls|dispossess',
'indigen':r'\bindigen|\bnative (?:people|population)',
'ancestral':r'ancestral|homeland of their ancestors|historic(?:al)? homeland',
're-establish':r'\bre-?establish|\brestor(?:e|ation) of|\breturn to zion|\brepatriat',
'zionist_agent':r'\bzionists?\b(?! movement| congress| organi)',
'occupation':r'\boccup(?:ied|ation)',
'apartheid':r'apartheid',
'arab_majority':r'arab majority|predominantly (?:palestinian )?arab|overwhelming arab',
'rejected':r'\brejected\b',
'holocaust':r'holocaust|shoah',
'antisemit':r'antisemit|anti-semit',
'scholars_say':r'scholars?|historians?|experts?',
'disputed':r'\bdisputed?\b|\bcontested\b|\bcontroversial\b|\bdebated?\b|\bsome (?:scholars|historians)\b',
'israel_since_1967':r'since (?:the )?1967|since the six-day war',
}
from collections import defaultdict
res={}
for g in ['T','C']:
    sel=[x for x in d if (x['group']=='treatment')==(g=='T')]
    for k,p in T.items():
        gain=loss=both=0
        for x in sel:
            a=bool(re.search(p,x['lead0'],re.I)); b=bool(re.search(p,x['lead1'],re.I))
            gain+= (b and not a); loss+=(a and not b); both+=(a and b)
        res[(g,k)]=(gain,loss,both,len(sel))
for k in T:
    t=res[('T',k)];c=res[('C',k)]
    print(f"{k:16s} T gain/loss/both/n={t}  C={c}")
