import json,re
d=json.load(open('/home/user/photoStamper/wikitrends/data/study3/qual_discovery.json'))
M={
'attrib':r"\b(according to|described as|has been described|have described|considered by|regarded as|accused|alleged|allegations?|claims?|claimed|critics|proponents|supporters|is seen as|are seen as|viewed as|characteri[sz]ed)\b",
'hedge':r"\b(may|might|possibly|reportedly|purportedly|perceived|so-called|some scholars|some historians|disputed|controvers\w+)\b",
'colon':r"\bcoloni[sz]\w*|settler[- ]colon\w*",
'terror':r"\bterror\w*",
'militant':r"\bmilitan\w*",
'genocide':r"\bgenocid\w*",
'ethclean':r"ethnic cleansing",
'occup':r"\boccup\w*",
'zionistAgent':r"\bZionists?\b(?! movement)",
'expelled':r"\b(expelled|expulsions?|forcibly displaced|forced displacement|dispossess\w*)\b",
'fled':r"\b(fled|exodus|flight)\b",
'apartheid':r"\bapartheid\b",
'scare':r"\"[^\"]{1,40}\"",
'illegal':r"\b(illegal|unlawful|in violation of)\b",
}
groups={'T':[x for x in d if x['group']=='treatment'],'C':[x for x in d if x['group']!='treatment']}
def fs(t): 
    t=(t or '').strip(); m=re.match(r'(.+?[.!?])(\s|$)',t,re.S); return m.group(1) if m else t
for k,p in M.items():
    row=[]
    for g,xs in groups.items():
        up=dn=0; fsup=fsdn=0; r0=r1=0;n0=n1=0
        for x in xs:
            a=len(re.findall(p,x['lead0'] or '',re.I)); b=len(re.findall(p,x['lead1'] or '',re.I))
            up+=b>a; dn+=b<a
            fa=len(re.findall(p,fs(x['lead0']),re.I)); fb=len(re.findall(p,fs(x['lead1']),re.I))
            fsup+=fb>fa; fsdn+=fb<fa
            r0+=a; r1+=b; n0+=len((x['lead0'] or '').split()); n1+=len((x['lead1'] or '').split())
        row.append(f"{g}: lead up/down {up}/{dn} | FS up/down {fsup}/{fsdn} | per1kw {1000*r0/max(n0,1):.2f}->{1000*r1/max(n1,1):.2f}")
    print(f"{k:13s}", ' || '.join(row))
print({g:len(v) for g,v in groups.items()})
