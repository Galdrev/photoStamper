/* ---------- data lab v2: eight labs, touch over type ---------- */
(function(){
"use strict";
const D=typeof R!=="undefined"&&R?R:(window.R||null);
const root=document.getElementById("lx");
if(!root)return;
const WF=()=>window.WFD||{};
const q=(s,r=document)=>r.querySelector(s), qa=(s,r=document)=>[...r.querySelectorAll(s)];
const RMQ=matchMedia("(prefers-reduced-motion: reduce)"), still=()=>RMQ.matches;
const E=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const F=(x,d=1)=>x==null||!isFinite(x)?"–":(+x).toFixed(d);
const SG=(x,d=1)=>x==null||!isFinite(x)?"–":(x>0?"+":x<0?"−":"±")+Math.abs(x).toFixed(d);
const N=n=>Math.round(+n).toLocaleString("en-US");
const PC=x=>x==null||!isFinite(x)?"–":Math.round(x*100)+"%";
const MON=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
const DL=s=>/^\d{4}-\d{2}/.test(s||"")?MON[+s.slice(5,7)-1]+" "+s.slice(0,4):String(s||"");
const DLL=s=>/^\d{4}-\d{2}-\d{2}/.test(s||"")?(+s.slice(8,10))+" "+DL(s):DL(s);
const TM=s=>Date.UTC(+s.slice(0,4),+s.slice(5,7)-1,/^\d{4}-\d{2}-\d{2}/.test(s)?+s.slice(8,10):1);
const WARt=Date.UTC(2023,9,7);
const phone=()=>innerWidth<640;
const tokv=n=>getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const clamp=(v,a,b)=>v<a?a:v>b?b:v;
const mean=a=>{let s=0;for(let i=0;i<a.length;i++)s+=a[i];return a.length?s/a.length:NaN};
function rng(seed){let s=(seed>>>0)||1;return()=>((s=(Math.imul(s,1664525)+1013904223)>>>0)/4294967296)}
const hash=str=>{let h=2166136261;for(let i=0;i<str.length;i++){h^=str.charCodeAt(i);h=Math.imul(h,16777619)}h^=h>>>16;h=Math.imul(h,2246822507);h^=h>>>13;h=Math.imul(h,3266489909);h^=h>>>16;return (h>>>0)/4294967296};
function bootMean(v,B,seed){if(v.length<2)return [NaN,NaN];const r=rng(seed),n=v.length,o=new Float64Array(B);for(let b=0;b<B;b++){let s=0;for(let i=0;i<n;i++)s+=v[(r()*n)|0];o[b]=s/n}o.sort();return [o[Math.floor(B*.025)],o[Math.min(B-1,Math.floor(B*.975))]]}
function bootGap(t,c,B,seed){if(t.length<2||c.length<2)return [NaN,NaN];const r=rng(seed),o=new Float64Array(B),nt=t.length,nc=c.length;for(let b=0;b<B;b++){let s=0,u=0;for(let i=0;i<nt;i++)s+=t[(r()*nt)|0];for(let i=0;i<nc;i++)u+=c[(r()*nc)|0];o[b]=s/nt-u/nc}o.sort();return [o[Math.floor(B*.025)],o[Math.min(B-1,Math.floor(B*.975))]]}
function niceStep(span,n){const s=span/Math.max(1,n),p=10**Math.floor(Math.log10(s||1)),f=s/p;return (f<=1?1:f<=2?2:f<=2.5?2.5:f<=5?5:10)*p}
function tickVals(lo,hi,n=4){const st=niceStep(hi-lo,n),out=[];for(let v=Math.ceil(lo/st-1e-9)*st;v<=hi+1e-9;v+=st)out.push(+v.toFixed(10));return out}
const FEW=30;
const fewTag='<span class="lx-fewtag">too few to say</span>';
const note=msg=>`<p class="lx-note">${msg}</p>`;

/* short names */
const SHORT={settler_colonial:"Settler-colonial",apartheid:"Apartheid",genocide:"Genocide",ethnic_cleansing:"Ethnic cleansing",occupation:"Occupation",nakba_expulsion:"Nakba / expulsion",war_crimes:"War crimes",indigenous_homeland:"Indigenous / homeland",persecution_antisemitism:"Antisemitism / persecution",terrorism:"Terrorism",militant:"Militant",placebo_geography:"Placebo: river, mountain…"};
const SUBN={zionism:"Zionism",israel:"Israel",conflict:"The conflict",judaism:"Judaism",antisemitism:"Antisemitism","category-sample":"Category sample",nationalism:"Other nationalisms",states:"Other states",conflicts:"Other conflicts",religion:"Religions",settler_colonial_framings:"Colonial histories"};
const subNm=k=>SUBN[k]||(typeof subName==="function"?subName(k):String(k||"other").replace(/[_-]+/g," ").replace(/^./,c=>c.toUpperCase()));
const frNm=k=>SHORT[k]||(typeof LABEL!=="undefined"&&LABEL[k])||String(k).replace(/_/g," ");
const LNG={en:"English",de:"German",fr:"French",es:"Spanish",it:"Italian",nl:"Dutch",ru:"Russian",he:"Hebrew",ar:"Arabic",pl:"Polish",pt:"Portuguese"};

/* tooltip: page helper if present */
const tipOn=(h,x,y)=>{if(typeof showTip==="function")showTip(h,x,y)};
const tipOff=()=>{if(typeof hideTip==="function")hideTip()};

/* open an article: the page's drawer if present, else a small sheet */
function openArt(title,from){
  const w=WF();
  if(typeof w.openArticle==="function"){try{w.openArticle(title,{from});return}catch(e){console.error(e)}}
  const od=typeof w.openDrawer==="function"?w.openDrawer:typeof openDrawer==="function"?openDrawer:null;
  if(od&&A.some(a=>a.title===title)){try{od(title,{from,noLedger:false});return}catch(e){console.error(e)}}
  sheet(title);
}
function sheet(title){
  let s=q("#lxSheet");if(!s){s=document.createElement("div");s.id="lxSheet";s.className="lx-sheet";s.setAttribute("role","dialog");root.append(s)}
  const a=A.find(x=>x.title===title);
  const r0=a&&rate(a,idxAt(a,FIRST,true),"full",CRIT),r1=a&&rate(a,idxAt(a,LAST,false),"full",CRIT);
  s.innerHTML=`<div class="lx-sheet-h"><b>${E(title)}</b><button type="button" aria-label="Close">×</button></div>${a?`<p class="n">${a.group==="treatment"?"Topic article":"Comparison article"} · ${E(subNm(a.subgroup))}</p><p>Loaded words per 10,000 words of full text: <b>${F(r0,1)}</b> in ${DL(FIRST)} → <b>${F(r1,1)}</b> in ${DL(LAST)}</p>`:""}<a href="https://en.wikipedia.org/wiki/${encodeURIComponent(String(title).replace(/ /g,"_"))}" target="_blank" rel="noopener">Open on Wikipedia</a>`;
  s.hidden=false;q("button",s).onclick=()=>{s.hidden=true};
}

/* ---------- shared data ---------- */
const A=(D&&D.articles)||[];
const DATES=(D&&D.dates)||[];
const FIRST=(D&&D.first)||DATES[0], LAST=(D&&D.last)||DATES[DATES.length-1];
const PRE=(D&&D.pre_war)||DATES.filter(d=>TM(d)<WARt).pop();
const CRIT=(D&&D.critical)||[];
const DID=(D&&D.did)||[];
const isPrim=a=>(a.group==="treatment"||a.group==="control")&&a.primary!==false;
const TOP=A.filter(a=>a.group==="treatment"&&isPrim(a)), CMP=A.filter(a=>a.group==="control"&&isPrim(a));
function ixMap(a){if(!a._lxix){const m={};(a.crit_series_dates||DATES).forEach((d,i)=>m[d]=i);a._lxix=m}return a._lxix}
function idxAt(a,d,exact){if(exact){const i=ixMap(a)[d];return i==null?-1:i}const ds=a.crit_series_dates||DATES;let j=-1;for(let i=0;i<ds.length;i++){if(ds[i]<=d)j=i;else break}return j}
function rate(a,i,part,keys){
  if(i<0)return null;
  if(part==="lead"){const w=a.lead_words_series&&a.lead_words_series[i];if(!w)return null;let s=0;for(const k of keys){const v=a.lead_frame_series&&a.lead_frame_series[k]&&a.lead_frame_series[k][i];if(v==null)return null;s+=v}return s*1e4/w}
  const w=a.words_series&&a.words_series[i];if(!w)return null;let s=0;for(const k of keys){const v=a.frame_series&&a.frame_series[k]&&a.frame_series[k][i];if(v!=null)s+=v}return s*1e4/w}
function change(a,d0,d1,part,keys){const r0=rate(a,idxAt(a,d0,true),part,keys);if(r0==null)return null;const r1=rate(a,idxAt(a,d1,false),part,keys);return r1==null?null:r1-r0}
const hasSeries=A.some(a=>a.frame_series&&a.words_series);

/* ---------- views explored ---------- */
const SEEN=new Set();
function view(key){if(SEEN.has(key))return;SEEN.add(key);const n=q("#lxViewsN");if(n)n.textContent=SEEN.size;const w=q("#lxViewsW");if(w)w.textContent=SEEN.size===1?"view":"views";const b=q("#lxViews");if(b&&!still()){b.classList.remove("bump");void b.offsetWidth;b.classList.add("bump");setTimeout(()=>b.classList.remove("bump"),600)}}

/* drag helper: pointer events with capture; calls mv(e,dx,dy) and up(e,moved) */
function drag(el,{down,mv,up,slop=6}){
  el.addEventListener("pointerdown",e=>{
    if(e.button>0)return;
    const st={x:e.clientX,y:e.clientY,moved:false,id:e.pointerId,data:null};
    st.data=down?down(e,st):true;if(st.data===false)return;
    try{el.setPointerCapture(e.pointerId)}catch(_){}
    const M=ev=>{if(ev.pointerId!==st.id)return;const dx=ev.clientX-st.x,dy=ev.clientY-st.y;if(!st.moved&&Math.hypot(dx,dy)>slop)st.moved=true;if(mv)mv(ev,dx,dy,st)};
    const U=ev=>{if(ev.pointerId!==st.id)return;el.removeEventListener("pointermove",M);el.removeEventListener("pointerup",U);el.removeEventListener("pointercancel",U);if(up)up(ev,st.moved,st,ev.type==="pointercancel")};
    el.addEventListener("pointermove",M);el.addEventListener("pointerup",U);el.addEventListener("pointercancel",U);
  });
}
const raf=fn=>{let p=false;return()=>{if(p)return;p=true;requestAnimationFrame(()=>{p=false;fn()})}};

/* =====================================================================
   1. SHADOW BARS
   ===================================================================== */
const S1={i0:0,i1:Math.max(0,DATES.length-1),cmp:"all",open:null,part:"full"};
const PART={full:"full text",lead:"opening paragraph"};
const CSETS=[["all","All comparison",()=>true,"All"],["quiet","Quiet comparison",a=>!a.shocked,"Quiet"],["war","Own-war comparison",a=>!!a.shocked,"Own war"],["colonial","Settler-colonial set",a=>a.subgroup==="settler_colonial_framings","Colonial"],["religion","Religions",a=>a.subgroup==="religion","Religions"]];
const SP={};
function s1Spark(){const pt=S1.part;if(SP[pt])return SP[pt];const m=arr=>DATES.map(d=>{const v=[];for(const a of arr){const i=idxAt(a,d,true);const r=rate(a,i,pt,CRIT);if(r!=null)v.push(r)}return v.length?mean(v):null});return SP[pt]={t:m(TOP),c:m(CMP)}}
function s1Calc(){
  const d0=DATES[S1.i0],d1=DATES[S1.i1];
  const vals=arr=>{const o=[];for(const a of arr){const v=change(a,d0,d1,S1.part,CRIT);if(v!=null)o.push({a,v})}return o};
  const cs=CSETS.find(c=>c[0]===S1.cmp)||CSETS[0];
  const C=vals(CMP.filter(cs[2])),C0=S1.cmp==="all"?C:vals(CMP);
  const groups=new Map();for(const a of TOP){const k=a.subgroup||"other";if(!groups.has(k))groups.set(k,[]);groups.get(k).push(a)}
  const rows=[{k:"__all",name:"All topic articles",items:vals(TOP)}];
  [...groups].map(([k,arr])=>({k,name:subNm(k),items:vals(arr)})).sort((x,y)=>y.items.length-x.items.length).forEach(r=>rows.push(r));
  rows.forEach((r,j)=>{const v=r.items.map(x=>x.v);r.n=v.length;r.m=mean(v);r.ci=bootMean(v,r.n>200?150:300,17+j)});
  const cv=C.map(x=>x.v);
  return {rows,d0,d1,sh:mean(cv),nC:cv.length,shci:bootMean(cv,300,5),gh:mean(C0.map(x=>x.v)),nC0:C0.length,cs};
}
function s1Init(){
  const box=q("#lxShadow");
  if(!hasSeries||!TOP.length||!CMP.length||DATES.length<2){q("#lxSBars").innerHTML=note("The article time series are missing from this build, so the shadow bars cannot be drawn.");q("#lxSStrip").hidden=true;return}
  const chips=q("#lxSChips");
  chips.innerHTML='<span class="lab">Shadow</span>'+CSETS.map(c=>{const n=CMP.filter(c[2]).length;return n?`<button class="lx-pill${n<FEW?" lx-few":""}" type="button" data-c="${c[0]}" aria-pressed="${c[0]===S1.cmp}"><span class="lx-lg">${E(c[1])}</span><span class="lx-sh">${E(c[3])}</span> <span class="n">${n}</span></button>`:""}).join("");
  chips.onclick=e=>{const b=e.target.closest("[data-c]");if(!b)return;S1.cmp=b.dataset.c;qa("[data-c]",chips).forEach(x=>x.setAttribute("aria-pressed",String(x===b)));s1Draw();view("s:"+S1.part+":"+S1.i0+":"+S1.i1+":"+S1.cmp)};
  const ps=q("#lxSPart");if(!A.some(a=>a.lead_words_series))ps.hidden=true;
  ps.onclick=e=>{const b=e.target.closest("[data-v]");if(!b)return;S1.part=b.dataset.v;qa("[data-v]",ps).forEach(x=>x.setAttribute("aria-pressed",String(x===b)));s1Strip();s1Draw();view("s:"+S1.part+":"+S1.i0+":"+S1.i1+":"+S1.cmp)};
  q("#lxSBars").onclick=e=>{const t=e.target.closest("[data-t]");if(t){openArt(t.dataset.t,t);return}const b=e.target.closest(".lx-bar");if(!b)return;S1.open=S1.open===b.dataset.k?null:b.dataset.k;s1Draw();if(S1.open)view("s:open:"+S1.open)};
  const strip=q("#lxSStrip"),redraw=raf(()=>{s1Strip();s1Draw()});
  const X=i=>strip._x?strip._x(i):0;
  const nearest=px=>{let b=0,bd=1e9;for(let i=0;i<DATES.length;i++){const d=Math.abs(X(i)-px);if(d<bd){bd=d;b=i}}return b};
  drag(strip,{down:e=>{const r=strip.getBoundingClientRect(),x=e.clientX-r.left,a=X(S1.i0),b=X(S1.i1);
      let mode=Math.abs(x-a)<24&&Math.abs(x-a)<=Math.abs(x-b)?"a":Math.abs(x-b)<24?"b":x>a&&x<b?"m":x<=a?"a":"b";
      const st={mode,r,i0:S1.i0,i1:S1.i1,x0:x,grab:nearest(x)};
      if(mode==="a"&&Math.abs(x-a)>=24){S1.i0=Math.min(nearest(x),S1.i1-1);redraw()}
      if(mode==="b"&&Math.abs(x-b)>=24){S1.i1=Math.max(nearest(x),S1.i0+1);redraw()}
      return st},
    mv:(e,dx,dy,st)=>{const s=st.data,x=e.clientX-s.r.left,i=nearest(x);
      if(s.mode==="a")S1.i0=Math.min(i,S1.i1-1);else if(s.mode==="b")S1.i1=Math.max(i,S1.i0+1);
      else{const d=i-s.grab,w=s.i1-s.i0;let n0=clamp(s.i0+d,0,DATES.length-1-w);S1.i0=n0;S1.i1=n0+w}
      redraw()},
    up:(e,moved,st)=>{const s=st.data,pi=DATES.indexOf(PRE),wx=strip._war;
      if(pi>=0&&wx!=null&&strip._step){const near=i=>Math.abs(X(i)-wx)<strip._step*1.3;
        if((s.mode==="a"||s.mode==="m")&&near(S1.i0)&&pi<S1.i1&&S1.i0!==pi){if(s.mode==="m"){const w=S1.i1-S1.i0;S1.i0=pi;S1.i1=Math.min(DATES.length-1,pi+w)}else S1.i0=pi;strip._snap=performance.now()}
        else if(s.mode==="b"&&near(S1.i1)&&pi>S1.i0&&S1.i1!==pi){S1.i1=pi;strip._snap=performance.now()}}
      s1Strip();s1Draw();view("s:"+S1.part+":"+S1.i0+":"+S1.i1+":"+S1.cmp)}});
  strip.tabIndex=0;
  strip.addEventListener("keydown",e=>{const k=e.key;if(k!=="ArrowLeft"&&k!=="ArrowRight")return;e.preventDefault();const d=k==="ArrowLeft"?-1:1;if(e.shiftKey)S1.i0=clamp(S1.i0+d,0,S1.i1-1);else S1.i1=clamp(S1.i1+d,S1.i0+1,DATES.length-1);s1Strip();s1Draw()});
  s1Strip();s1Draw();
}
function s1Strip(){
  const el=q("#lxSStrip");if(!el||el.hidden)return;const w=Math.max(260,el.clientWidth),h=78,pl=12,pr=12;
  const t0=TM(DATES[0]),t1=TM(DATES[DATES.length-1]),x=t=>pl+(t-t0)/((t1-t0)||1)*(w-pl-pr),X=i=>x(TM(DATES[i]));
  el._x=X;el._step=(w-pl-pr)/Math.max(1,DATES.length-1);el._war=WARt>=t0&&WARt<=t1?x(WARt):null;
  const sp=s1Spark(),all=[...sp.t,...sp.c].filter(v=>v!=null),mx=Math.max(1e-9,...all),y=v=>50-(v/mx)*30;
  const path=arr=>arr.map((v,i)=>v==null?"":`${i&&arr[i-1]!=null?"L":"M"}${X(i).toFixed(1)},${y(v).toFixed(1)}`).join("");
  const a=X(S1.i0),b=X(S1.i1),snapped=el._snap&&performance.now()-el._snap<1500;
  let s=`<svg viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" role="img" aria-label="Time window from ${DL(DATES[S1.i0])} to ${DL(DATES[S1.i1])}">`;
  s+=`<rect class="win" x="${a}" y="16" width="${b-a}" height="42"/>`;
  s+=`<line class="axis" x1="${pl}" x2="${w-pr}" y1="58" y2="58"/>`;
  const years=[...new Set(DATES.map(d=>d.slice(0,4)))];
  years.forEach(yr=>{const xx=x(Date.UTC(+yr,0,1));if(xx>=pl-1&&xx<=w-pr+1)s+=`<line class="axis" x1="${xx}" x2="${xx}" y1="58" y2="62"/><text x="${xx+3}" y="72">${phone()?"’"+yr.slice(2):yr}</text>`});
  s+=`<path d="${path(sp.c)}" fill="none" style="stroke:var(--comp)" stroke-width="1.5" stroke-dasharray="4 3"/><path d="${path(sp.t)}" fill="none" style="stroke:var(--topic)" stroke-width="2"/>`;
  if(el._war!=null)s+=`<line class="war" x1="${el._war}" x2="${el._war}" y1="14" y2="62"/><text class="war" x="${el._war+(el._war>w*.6?-4:4)}" y="${snapped?50:24}" text-anchor="${el._war>w*.6?"end":"start"}" style="font-size:10px;paint-order:stroke;stroke:var(--sheet);stroke-width:3px">${snapped?"last snapshot before the war: "+DL(PRE):"7 Oct 2023"}</text>`;
  const hd=(xx,lab,anchor)=>`<g class="hd"><rect x="${xx-1.5}" y="14" width="3" height="46" rx="1"/><rect x="${xx-6}" y="52" width="12" height="12" rx="6"/><text class="lbl" x="${xx}" y="10" text-anchor="${anchor}">${lab}</text></g>`;
  const la=DL(DATES[S1.i0]),lb=DL(DATES[S1.i1]),close=b-a<120;
  s+=hd(a,la,close?"end":a<60?"start":"middle")+hd(b,lb,close?"start":b>w-60?"end":"middle");
  el.innerHTML=s+"</svg>";
  el.setAttribute("aria-label",`Time window ${la} to ${lb}. Drag a handle, or use the arrow keys (Shift moves the start).`);
}
function s1Draw(){
  const box=q("#lxSBars");if(!box||!TOP.length)return;const C=s1Calc();
  const vals=[0,C.sh,C.gh];C.rows.forEach(r=>{vals.push(r.m);if(isFinite(r.ci[0]))vals.push(r.ci[0],r.ci[1])});
  let lo=Math.min(...vals.filter(isFinite)),hi=Math.max(...vals.filter(isFinite));const pad=(hi-lo)*(phone()?.2:.08)||1;lo=lo<0?lo-pad:0;hi=hi>0?hi+pad:0;if(hi===lo)hi=lo+1;
  const P=v=>((v-lo)/(hi-lo)*100).toFixed(2)+"%",W=(a,b)=>(Math.abs(b-a)/(hi-lo)*100).toFixed(2)+"%";
  const seg=(cls,a,b)=>`<i class="${cls}" style="left:${P(Math.min(a,b))};width:${W(a,b)}"></i>`;
  const sh=C.sh;
  let h=`<div class="lx-key"><span><i style="background:var(--topic)"></i>extra change</span><span><i style="background:var(--comp);opacity:.35"></i>shadow: ${E(C.cs[1].toLowerCase())} (${C.nC})</span><span><i style="border:1.5px dashed var(--ink);opacity:.6"></i>pre-registered comparison</span><span><i style="height:2px;background:var(--ink)"></i>95% range</span></div>`;
  for(const r of C.rows){
    const few=r.n<FEW,m=r.m;
    let bar="";
    if(isFinite(m)){
      if(!isFinite(sh)||Math.sign(m)!==Math.sign(sh))bar=seg("over",0,m);
      else if(Math.abs(m)>Math.abs(sh))bar=seg("under",0,sh)+seg("over",sh,m);
      else bar=seg("under",0,m);
    }
    const vx=isFinite(m)?(m>=0?`left:calc(${P(Math.max(m,isFinite(r.ci[1])?r.ci[1]:m))} + 6px)`:`right:calc(100% - ${P(Math.min(m,isFinite(r.ci[0])?r.ci[0]:m))} + 6px)`):"left:0";
    h+=`<button class="lx-bar${r.k==="__all"?" all":""}${few?" few":""}" type="button" data-k="${E(r.k)}" aria-expanded="${S1.open===r.k}">
      <span class="nm">${E(r.name)}<small>${N(r.n)} articles · ${SG(m,1)} vs ${SG(sh,1)}${few?" · ":""}${few?fewTag:""}</small></span>
      <span class="trk">${isFinite(sh)?seg("shadow",0,sh):""}${bar}${isFinite(C.gh)?seg("ghost",0,C.gh):""}${isFinite(r.ci[0])?`<i class="ci" style="left:${P(r.ci[0])};width:${W(r.ci[0],r.ci[1])}"></i>`:""}<i class="z" style="left:${P(0)}"></i><span class="v" style="${vx}">${SG(m,1)}</span></span></button>`;
    if(S1.open===r.k){
      const dir=m>=0?-1:1,top=[...r.items].sort((x,y)=>dir*(x.v-y.v)).slice(0,5),mx=Math.max(1e-9,...top.map(x=>Math.abs(x.v)));
      h+=`<div class="lx-top"><span class="n">The five articles that ${m>=0?"rose":"fell"} most · tap one to open it</span>${top.map(x=>`<button type="button" data-t="${E(x.a.title)}"><span>${E(x.a.title)}</span><i style="width:${(Math.abs(x.v)/mx*100).toFixed(1)}%;${x.v<0?"background:var(--dec)":""}"></i><span>${SG(x.v,1)}</span></button>`).join("")}</div>`;
    }
  }
  const tk=tickVals(lo,hi,phone()?3:5);
  h+=`<div class="lx-axis"><div></div><div>${tk.map(t=>`<span style="left:${P(t)}">${SG(t,t%1?1:0).replace("±","")}</span>`).join("")}</div></div><p class="n" style="margin:0">Per 10,000 words of ${PART[S1.part]}, ${DL(C.d0)}–${DL(C.d1)}. Bars start at zero.</p>`;
  box.innerHTML=h;
  const all=C.rows[0],ex=isFinite(all.m)&&isFinite(sh)?all.m-sh:NaN;
  q("#lxSSay").innerHTML=isFinite(ex)?`Topic articles <b>${SG(all.m,1)}</b>, ${E(C.cs[1].toLowerCase())} <b>${SG(sh,1)}</b>${C.nC<FEW?` (only ${C.nC} articles, too few to say)`:""}: an extra change of <b>${SG(ex,1)}</b> per 10,000 words. ${Math.abs(ex)<.1*Math.max(Math.abs(all.m),Math.abs(sh),.5)?"Almost all of it is shadow.":"Read it only if the black range line clears the shadow."}`:"";
}

/* =====================================================================
   2. SHUFFLE THE LABELS
   ===================================================================== */
const PDEF={P1:"loaded words in the opening paragraph",P2:"loaded words in the full text",P3:"history words in the full text"};
const PROWS=["P1","P2","P3"].map(id=>DID.find(r=>r.id===id)).filter(Boolean);
const S2={id:PROWS.some(r=>r.id==="P2")?"P2":(PROWS[0]&&PROWS[0].id),st:{}};
const S3={id:S2.id,side:"both",T:{}};
function pSeg(el,lab,cur,cb){const L=id=>`Pre-registered test ${id}: ${PDEF[id]||""}`;el.innerHTML=PROWS.map(r=>`<button type="button" data-p="${r.id}" aria-pressed="${r.id===cur}" aria-label="${E(L(r.id))}">${r.id}</button>`).join("");if(lab)lab.textContent=L(cur);el.onclick=e=>{const b=e.target.closest("[data-p]");if(!b)return;qa("[data-p]",el).forEach(x=>x.setAttribute("aria-pressed",String(x===b)));if(lab)lab.textContent=L(b.dataset.p);cb(b.dataset.p)}}
function s2State(id){
  if(S2.st[id])return S2.st[id];const r=PROWS.find(x=>x.id===id);if(!r)return null;
  const t=r.changes_t||[],c=r.changes_c||[],all=Float64Array.from([...t,...c]),nt=t.length,n=all.length;
  let tot=0;for(const v of all)tot+=v;
  const real=nt&&n-nt?mean(t)-mean(c):r.did;
  const ps=r.perm_sample||[];let L=Math.max(Math.abs(real)*1.6,...ps.map(Math.abs))*1.08;if(!(L>0))L=1;
  const B=31,perm=Int32Array.from({length:n},(_,i)=>i);
  const pre=new Float64Array(B);ps.forEach(v=>{pre[clamp(Math.floor((v+L)/(2*L)*B),0,B-1)]++});
  return S2.st[id]={r,all,nt,n,tot,real,L,B,bins:new Int32Array(B),pre,count:0,beat:0,perm,rnd:rng(99+id.charCodeAt(1)),ok:nt>=2&&n-nt>=2};
}
function s2Shuffle(st){const p=st.perm,n=st.n,r=st.rnd;for(let i=n-1;i>0;i--){const j=(r()*(i+1))|0,t=p[i];p[i]=p[j];p[j]=t}
  let s=0;for(let i=0;i<st.nt;i++)s+=st.all[p[i]];const g=s/st.nt-(st.tot-s)/(st.n-st.nt);
  st.bins[clamp(Math.floor((g+st.L)/(2*st.L)*st.B),0,st.B-1)]++;st.count++;if(Math.abs(g)>=Math.abs(st.real)-1e-12)st.beat++;return g}
function s2Tiles(st,fresh){
  const el=q("#lxTiles");if(!st||!st.ok){el.innerHTML="";return}
  if(fresh||el.childElementCount!==st.n){let h="";for(let i=0;i<st.n;i++)h+="<i></i>";el.innerHTML=h}
  const kids=el.children;
  if(st.count===0){for(let i=0;i<st.n;i++)kids[i].className=i<st.nt?"t":"";return}
  const p=st.perm;for(let j=0;j<st.n;j++)kids[p[j]].className=j<st.nt?"t":"";
}
function s2Init(){
  const seg=q("#lxPSeg");
  if(!PROWS.length){q("#lxShuffle .lx-shuf").innerHTML=note("The pre-registered test results are missing from this build.");return}
  pSeg(seg,q("#lxPSegL"),S2.id,id=>{S2.id=id;stopHold();s2Draw(true);view("p:"+id)});
  const btn=q("#lxShufBtn");let hold=null,tmo=null;
  const one=(fast)=>{const st=s2State(S2.id);if(!st||!st.ok)return;let g;const k=fast?7:1;for(let i=0;i<k;i++)g=s2Shuffle(st);q("#lxTiles").classList.toggle("fast",!!fast);s2Tiles(st);s2Hist(st,fast?null:g);s2Count(st)};
  const stopHold=()=>{clearTimeout(tmo);clearInterval(hold);hold=tmo=null;btn.classList.remove("on");q("#lxTiles").classList.remove("fast")};
  btn.addEventListener("pointerdown",e=>{if(e.button>0)return;e.preventDefault();try{btn.setPointerCapture(e.pointerId)}catch(_){}one(false);tmo=setTimeout(()=>{btn.classList.add("on");hold=setInterval(()=>one(true),still()?120:45)},380)});
  ["pointerup","pointercancel","lostpointercapture"].forEach(t=>btn.addEventListener(t,stopHold));
  btn.addEventListener("keydown",e=>{if(e.key===" "||e.key==="Enter"){e.preventDefault();one(false)}});
  btn.addEventListener("contextmenu",e=>e.preventDefault());
  s2Draw(true);
}
function s2Count(st){
  const r=st.r,pp=r.p_perm;
  q("#lxShufCount").innerHTML=st.count?`<b>${N(st.beat)}</b> of <b>${N(st.count)}</b> shuffles beat the real extra change <span class="n">(${PC(st.beat/st.count)})</span>`:`No shuffles yet.<br><span class="n" style="font-size:13px">Real extra change: ${SG(st.real,2)} per 10,000 words. Can chance match it?</span>`;
  q("#lxShufSay").innerHTML=`A shuffle “beats” the real extra change when its own is at least as big, either way (per 10,000 words). ${pp!=null?`In the study’s 5,000 shuffles, <b>${PC(pp)}</b> did (dashed outline).`:""} ${st.count>=200?(st.beat/st.count>.05?"Chance does this often, so the real extra change is not good evidence of a difference.":"Chance rarely does this. That points to a real difference, though only for this one pre-registered measure."):""} <span class="n">${N(st.nt)} topic and ${N(st.n-st.nt)} comparison articles.</span>`;
}
function s2Hist(st,drop){
  const el=q("#lxHist");if(!st)return;const w=Math.max(260,el.clientWidth),h=180,m={l:8,r:8,t:30,b:26},iw=w-m.l-m.r,ih=h-m.t-m.b;
  const x=v=>m.l+(v+st.L)/(2*st.L)*iw,bw=iw/st.B;
  let mx=0;for(const b of st.bins)mx=Math.max(mx,b);
  let pm=0;for(const b of st.pre)pm=Math.max(pm,b);
  const preScale=pm?(st.count?(st.count/st.pre.reduce((a,b)=>a+b,0)):ih*.85/pm):0;
  const top=Math.max(mx,pm*preScale,1)*(st.count?1.08:1);
  const Y=c=>m.t+ih-(c/top)*ih;
  let s=`<svg viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" role="img" aria-label="Histogram of extra change with shuffled labels">`;
  const rx=x(Math.abs(st.real)),lx=x(-Math.abs(st.real));
  s+=`<rect x="${m.l}" y="${m.t}" width="${Math.max(0,lx-m.l)}" height="${ih}" style="fill:var(--inc);opacity:.06"/><rect x="${rx}" y="${m.t}" width="${Math.max(0,w-m.r-rx)}" height="${ih}" style="fill:var(--inc);opacity:.06"/>`;
  for(let i=0;i<st.B;i++){const c=st.bins[i];if(!c)continue;const c0=-st.L+(i+.5)*2*st.L/st.B,beat=Math.abs(c0)>=Math.abs(st.real);s+=`<rect class="bin${beat?" beat":""}" x="${(m.l+i*bw+.5).toFixed(1)}" y="${Y(c).toFixed(1)}" width="${Math.max(1,bw-1).toFixed(1)}" height="${(m.t+ih-Y(c)).toFixed(1)}"/>`}
  if(pm){let d=`M${m.l},${m.t+ih}`;for(let i=0;i<st.B;i++){const yy=Y(st.pre[i]*preScale).toFixed(1);d+=`L${(m.l+i*bw).toFixed(1)},${yy}L${(m.l+(i+1)*bw).toFixed(1)},${yy}`}d+=`L${w-m.r},${m.t+ih}`;s+=`<path class="pre" d="${d}"/>`}
  s+=`<line class="axis" x1="${m.l}" x2="${w-m.r}" y1="${m.t+ih}" y2="${m.t+ih}"/><line class="zero" x1="${x(0)}" x2="${x(0)}" y1="${m.t+ih}" y2="${m.t+ih+5}"/>${tickVals(-st.L,st.L,phone()?4:6).map(t=>`<text x="${x(t)}" y="${h-6}" text-anchor="middle">${SG(t,Math.abs(t)<10&&t%1?1:0).replace("±","")}</text>`).join("")}`;
  const realX=x(st.real),mirX=x(-st.real),anc=v=>v>w*.7?"end":v<w*.3?"start":"middle";
  s+=`<line class="real" x1="${realX}" x2="${realX}" y1="${m.t-6}" y2="${m.t+ih}"/><text class="real" x="${realX}" y="${m.t-12}" text-anchor="${anc(realX)}">real extra change ${SG(st.real,2)} (pre-registered)</text>`;
  s+=`<line x1="${mirX}" x2="${mirX}" y1="${m.t}" y2="${m.t+ih}" style="stroke:var(--topic);stroke-dasharray:2 3;opacity:.7"/>`;
  el.innerHTML=s+"</svg>";
  if(drop!=null&&!still()){const cx=x(clamp(drop,-st.L,st.L)),bi=clamp(Math.floor((drop+st.L)/(2*st.L)*st.B),0,st.B-1),ty=Y(st.bins[bi]);
    const c=document.createElementNS("http://www.w3.org/2000/svg","circle");c.setAttribute("class","drop");c.setAttribute("cx",cx);c.setAttribute("cy",ty-3);c.setAttribute("r",3.5);q("svg",el).append(c);
    if(c.animate)c.animate([{transform:`translateY(${-(ty-3)}px)`,opacity:1},{transform:"translateY(0)",opacity:1},{transform:"translateY(0)",opacity:0}],{duration:700,easing:"cubic-bezier(.55,0,1,.45)"}).onfinish=()=>c.remove();else c.remove()}
}
function s2Draw(fresh){const st=s2State(S2.id);if(!st)return;
  if(!st.ok){q("#lxTiles").innerHTML="";q("#lxShufBtn").disabled=true;q("#lxShufCount").innerHTML="";q("#lxShufSay").innerHTML="Per-article changes for this test are not in this build, so it cannot be shuffled here."+(st.r.perm_sample&&st.r.perm_sample.length?" The dashed outline is the study’s own shuffles.":"");s2Hist(st,null);return}
  q("#lxShufBtn").disabled=false;s2Tiles(st,fresh);s2Hist(st,null);s2Count(st)}

/* =====================================================================
   3. PULL THE LOUDEST OUT
   ===================================================================== */
function s3Data(id){const r=PROWS.find(x=>x.id===id);if(!r||!r.changes_t||!r.changes_c)return null;
  if(!r._lx){const all=[...r.changes_t.map(v=>[v,0]),...r.changes_c.map(v=>[v,1])];const abs=all.map(x=>Math.abs(x[0])).sort((a,b)=>b-a);
    const k=Math.max(3,Math.round(all.length*.01)),T0=abs.length>k?(abs[k-1]+abs[k])/2:abs[0]+1;r._lx={all,M:(abs[0]||1)*1.04,T0}}return r}
function s3Init(){
  pSeg(q("#lxLSeg"),q("#lxLSegL"),S3.id,id=>{S3.id=id;s3Draw(true);view("l:"+id)});
  const side=q("#lxLSide");
  const TL={both:"Trim: both ends",high:"Trim: only the highest",low:"Trim: only the lowest"};
  side.innerHTML=[["both","Both"],["high","High"],["low","Low"]].map(([v,l])=>`<button type="button" data-s="${v}" aria-pressed="${v===S3.side}" aria-label="${TL[v]}">${l}</button>`).join("");q("#lxLSideL").textContent=TL[S3.side];
  side.onclick=e=>{const b=e.target.closest("[data-s]");if(!b)return;S3.side=b.dataset.s;q("#lxLSideL").textContent=TL[S3.side];qa("[data-s]",side).forEach(x=>x.setAttribute("aria-pressed",String(x===b)));s3Draw();view("l:"+S3.id+":"+S3.side)};
  const box=q("#lxLDots"),upd=raf(()=>s3Draw());
  drag(box,{down:e=>{const g=box._g;if(!g)return false;const r=box.getBoundingClientRect(),x=e.clientX-r.left,hx=g.x(S3.T[S3.id]),lx=g.x(-S3.T[S3.id]);
      const dR=S3.side!=="low"?Math.abs(x-hx):1e9,dL=S3.side!=="high"?Math.abs(x-lx):1e9;if(Math.min(dR,dL)>30)return false;return {r,h:dR<=dL?"R":"L"}},
    mv:(e,dx,dy,st)=>{const g=box._g,x=e.clientX-st.data.r.left,v=g.xi(x);S3.T[S3.id]=clamp(st.data.h==="R"?v:-v,0,g.M);upd()},
    up:()=>{s3Draw();const r=s3Data(S3.id);if(r)view("l:"+S3.id+":"+S3.side+":"+s3Removed(r).n)}});
  box.addEventListener("keydown",e=>{const g=box._g;if(!g||(e.key!=="ArrowLeft"&&e.key!=="ArrowRight"))return;e.preventDefault();S3.T[S3.id]=clamp(S3.T[S3.id]+(e.key==="ArrowLeft"?-1:1)*g.M/60,0,g.M);s3Draw()});
  s3Draw(true);
}
function s3Removed(r){const T=S3.T[r.id],sd=S3.side;const out=r._lx.all.map(([v])=>sd==="both"?Math.abs(v)>T:sd==="high"?v>T:v<-T);let n=0,nt=0;out.forEach((o,i)=>{if(o){n++;if(r._lx.all[i][1]===0)nt++}});return {out,n,nt,nc:n-nt}}
function s3Draw(fresh){
  const box=q("#lxLDots"),gap=q("#lxLGap"),r=s3Data(S3.id);
  if(!r){box.innerHTML=note("Per-article changes for this test are not in this build.");gap.innerHTML="";q("#lxLSay").innerHTML="";return}
  if(S3.T[r.id]==null)S3.T[r.id]=r._lx.T0;
  const w=Math.max(260,box.clientWidth),M=r._lx.M,m={l:10,r:10},bt=[28,phone()?96:116],bc=[bt[0]+bt[1]+14,phone()?62:72],h=bc[0]+bc[1]+30;
  const x=v=>m.l+(v+M)/(2*M)*(w-m.l-m.r),xi=px=>(px-m.l)/(w-m.l-m.r)*2*M-M;
  const rem=s3Removed(r),T=S3.T[r.id];
  if(fresh||!box._g||box._g.w!==w||box._g.id!==r.id){
    let s=`<svg viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" role="img" aria-label="Per-article changes, topic and comparison">`;
    s+=`<text x="${m.l}" y="${bt[0]-6}" class="ink" style="font-weight:600">Topic articles · ${N(r.changes_t.length)}</text><text x="${w/2}" y="${bc[0]-2}" text-anchor="middle" class="ink" style="font-weight:600;paint-order:stroke;stroke:var(--sheet);stroke-width:4px">Comparison articles · ${N(r.changes_c.length)}</text>`;
    s+=`<line class="zero" x1="${x(0)}" x2="${x(0)}" y1="${bt[0]}" y2="${bc[0]+bc[1]}" style="opacity:.35"/>`;
    s+=`<g class="dots">`;
    r._lx.all.forEach(([v,g],i)=>{const band=g?bc:bt,y=band[0]+5+hash(r.id+i)*(band[1]-10);s+=`<circle class="d" data-i="${i}" cx="${x(v).toFixed(1)}" cy="${y.toFixed(1)}" r="${phone()?2.3:2.6}" style="fill:var(${g?"--comp":"--topic"});fill-opacity:.7"/>`});
    s+=`</g><g class="hds"></g>`;
    const tk=tickVals(-M,M,phone()?4:6);s+=tk.map(t=>`<text x="${x(t)}" y="${h-8}" text-anchor="middle">${SG(t,Math.abs(t)<10&&t%1?1:0).replace("±","")}</text>`).join("");
    s+=`<text x="${w-m.r}" y="${h-20}" text-anchor="end">change per 10,000 words →</text>`;
    box.innerHTML=s+"</svg>";box.tabIndex=0;box.setAttribute("aria-label","Trim handles: use left and right arrow keys");
    box._g={w,id:r.id,x,xi,M};box._dots=qa(".d",box);
  }
  box._dots.forEach((d,i)=>d.classList.toggle("out",rem.out[i]));
  const hb=q(".hds",box),top=bt[0]-2,bot=bc[0]+bc[1]+2;let hs="";
  const hand=(xx,side)=>{const cutX=side==="R"?xx:m.l,cutW=side==="R"?w-m.r-xx:xx-m.l;return `<rect class="cut" x="${cutX}" y="${top}" width="${Math.max(0,cutW)}" height="${bot-top}"/><g class="hd"><rect class="grab" x="${xx-16}" y="${top-10}" width="32" height="${bot-top+20}"/><rect class="bar" x="${xx-1.5}" y="${top}" width="3" height="${bot-top}" rx="1"/><rect class="bar" x="${xx-7}" y="${top+bt[1]/2-14}" width="14" height="28" rx="7"/></g>`};
  if(S3.side!=="low")hs+=hand(x(T),"R");if(S3.side!=="high")hs+=hand(x(-T),"L");
  hb.innerHTML=hs;
  const kt=[],kc=[];r._lx.all.forEach(([v,g],i)=>{if(!rem.out[i])(g?kc:kt).push(v)});
  const gp=mean(kt)-mean(kc),band=bootGap(kt,kc,300,11),pr=r;
  const vals=[0,gp,band[0],band[1],pr.did,pr.lo,pr.hi].filter(isFinite);let lo=Math.min(...vals),hi=Math.max(...vals);const pd=(hi-lo)*.12||1;lo-=pd;hi+=pd;
  const gw=Math.max(260,gap.clientWidth),gh=70,X=v=>10+(v-lo)/(hi-lo)*(gw-20),few=kt.length<FEW||kc.length<FEW;
  let g=`<div class="lx-gl"><span>Extra change now <b>${SG(gp,2)}</b> <span class="n">per 10,000 words</span></span><span class="num">removed <b style="font-size:18px">${N(rem.n)}</b> of ${N(r._lx.all.length)} <span class="n">(${rem.nt} topic, ${rem.nc} comparison)</span></span></div>`;
  g+=`<svg viewBox="0 0 ${gw} ${gh}" width="${gw}" height="${gh}" role="img" aria-label="Extra change and its range">`;
  if(few)g+=`<defs><pattern id="lxH3" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="1.5" height="6" style="fill:var(--muted)" opacity=".5"/></pattern></defs>`;
  if(isFinite(pr.lo))g+=`<rect class="lx-ghost" x="${X(pr.lo)}" y="14" width="${X(pr.hi)-X(pr.lo)}" height="26" rx="2"/><line x1="${X(pr.did)}" x2="${X(pr.did)}" y1="10" y2="44" style="stroke:var(--ink);stroke-dasharray:3 2;opacity:.6"/><text x="${X(pr.did)}" y="8" text-anchor="middle">pre-registered ${SG(pr.did,2)}</text>`;
  if(isFinite(band[0]))g+=`<rect x="${X(band[0])}" y="20" width="${Math.max(1,X(band[1])-X(band[0]))}" height="14" rx="2" style="fill:${few?"url(#lxH3)":"var(--topic)"};opacity:${few?1:.3}"/>`;
  g+=`<line class="zero" x1="${X(0)}" x2="${X(0)}" y1="12" y2="${gh-16}"/><text x="${X(0)}" y="${gh-4}" text-anchor="middle">0</text>`;
  if(isFinite(gp))g+=`<circle cx="${X(gp)}" cy="27" r="6" style="fill:var(--topic);stroke:var(--sheet);stroke-width:2"/>`;
  g+=`</svg>`;
  gap.innerHTML=g+(few?`<p class="n" style="margin:0">${fewTag} fewer than ${FEW} articles left in a group.</p>`:"");
  const crosses=isFinite(band[0])&&band[0]<=0&&band[1]>=0;
  q("#lxLSay").innerHTML=`${rem.n?`Without the ${N(rem.n)} most extreme ${rem.n===1?"article":"articles"}, the extra change is <b>${SG(gp,2)}</b> per 10,000 words (range ${SG(band[0],1)} to ${SG(band[1],1)}, from 300 resamples), against the pre-registered <b>${SG(pr.did,2)}</b>.`:`Nothing removed: this is the full pre-registered comparison, extra change <b>${SG(gp,2)}</b> per 10,000 words.`} ${crosses?"The range still includes zero.":"The range is clear of zero."} ${Math.abs(gp-pr.did)>Math.max(.5,Math.abs(pr.did)*.5)&&rem.n?"A few articles carry a lot of the result.":"The result barely depends on the extremes."}`;
}

/* =====================================================================
   4. DEFINITION FLIPBOOK
   ===================================================================== */
const RT=D&&D.ratchet&&D.ratchet.articles||null, EXPO=D&&D.exposure||null;
const S4={title:null,step:0};
function fbData(t){const a=RT&&RT[t];if(!a)return null;if(a._lx)return a._lx;
  const vs=new Map((a.fs_variants||[]).map(v=>[v.id,v]));const steps=[];
  for(const e of a.fs_timeline||[]){const [d,vid,rv]=e;if(!vs.has(vid))continue;if(steps.length&&steps[steps.length-1].vid===vid){if(rv)steps[steps.length-1].rv=1;continue}steps.push({d,vid,rv:rv?1:0,t:TM(d)})}
  const ex=EXPO&&EXPO[t];const views=new Map();if(ex&&ex.variants)ex.variants.forEach(e=>{for(const v of vs.values()){if(v.s.slice(0,300)===e.s||v.s.slice(0,300)===String(e.s).slice(0,300)){views.set(v.id,(views.get(v.id)||0)+e.views);break}}});
  const order=[];const seen=new Set();steps.forEach(s=>{if(!seen.has(s.vid)){seen.add(s.vid);order.push(s.vid)}});
  for(const v of vs.values())if(!seen.has(v.id)){order.push(v.id)}
  const rvBy=new Map();steps.forEach(s=>{if(s.rv)rvBy.set(s.vid,(rvBy.get(s.vid)||0)+1)});
  const live=new Map();let sumLive=0;for(const v of vs.values())sumLive+=v.live_days||0;
  if(sumLive>0)for(const v of vs.values())live.set(v.id,v.live_days||0);
  else{const tl=a.fs_timeline||[],end=Math.max(Date.now(),tl.length?TM(tl[tl.length-1][0]):0);for(let i=0;i<tl.length;i++){const t=TM(tl[i][0]),n=i+1<tl.length?TM(tl[i+1][0]):end;if(vs.has(tl[i][1]))live.set(tl[i][1],(live.get(tl[i][1])||0)+Math.max(0,(n-t)/864e5))}}
  return a._lx={a,vs,steps,views,live,hasViews:!!(ex&&ex.variants&&views.size),order,rvBy,total:a.fs_n_variants||vs.size};
}
const toks=s=>((s||"").match(/\S+/g)||[]).join(" ");
function fbDefault(d){for(let i=d.steps.length-1;i>0;i--){if(toks(d.vs.get(d.steps[i].vid).s)!==toks(d.vs.get(d.steps[i-1].vid).s))return i}return d.steps.length-1}
function wdiff(a,b){const A_=(a||"").match(/\S+/g)||[],B_=(b||"").match(/\S+/g)||[];const n=Math.min(A_.length,160),m=Math.min(B_.length,160);
  const dp=new Uint16Array((n+1)*(m+1)),I=(i,j)=>i*(m+1)+j;
  for(let i=n-1;i>=0;i--)for(let j=m-1;j>=0;j--)dp[I(i,j)]=A_[i]===B_[j]?dp[I(i+1,j+1)]+1:Math.max(dp[I(i+1,j)],dp[I(i,j+1)]);
  const out=[];let i=0,j=0;const push=(t,w)=>{const l=out[out.length-1];if(l&&l.t===t)l.w.push(w);else out.push({t,w:[w]})};
  while(i<n&&j<m){if(A_[i]===B_[j]){push("=",A_[i]);i++;j++}else if(dp[I(i+1,j)]>=dp[I(i,j+1)]){push("-",A_[i]);i++}else{push("+",B_[j]);j++}}
  while(i<n)push("-",A_[i++]);while(j<m)push("+",B_[j++]);
  if(A_.length>n||B_.length>m)push("=",[...B_.slice(m)].join(" "));
  return out.map(o=>o.t==="="?E(o.w.join(" ")):o.t==="-"?`<del>${E(o.w.join(" "))}</del>`:`<ins>${E(o.w.join(" "))}</ins>`).join(" ");
}
function s4Init(){
  const cards=q("#lxFCards");
  if(!RT||!Object.keys(RT).length){cards.innerHTML="";q("#lxFBox").innerHTML=note("The revision-by-revision history of first sentences is not in this build.");return}
  const titles=Object.keys(RT).filter(t=>fbData(t)&&fbData(t).steps.length).sort((x,y)=>(RT[y].fs_n_variants||0)-(RT[x].fs_n_variants||0));
  if(!titles.length){q("#lxFBox").innerHTML=note("No first-sentence versions were recorded.");return}
  S4.title=titles.includes("Zionism")?"Zionism":titles[0];
  cards.innerHTML=titles.map(t=>{const d=fbData(t),t0=d.steps[0].t,t1=d.steps[d.steps.length-1].t||t0+1;const bk=new Map();d.steps.forEach(s=>{const k=Math.round((s.t-t0)/((t1-t0)||1)*60);bk.set(k,(bk.get(k)||0)|(s.rv?2:1))});
    return `<button class="lx-card" type="button" role="option" data-t="${E(t)}" aria-selected="${t===S4.title}"><b>${E(t)}</b><small>${N(d.total)} wordings · ${N(d.steps.length)} changes</small><svg viewBox="0 0 61 10" preserveAspectRatio="none" aria-hidden="true">${[...bk].map(([k,f])=>`<rect x="${k}" y="${f&2?0:3}" width=".8" height="${f&2?10:7}" style="fill:var(${f&2?"--del-bd":"--muted"})"/>`).join("")}</svg></button>`}).join("");
  cards.onclick=e=>{const b=e.target.closest("[data-t]");if(!b)return;S4.title=b.dataset.t;S4.step=fbDefault(fbData(S4.title));qa("[data-t]",cards).forEach(x=>x.setAttribute("aria-selected",String(x===b)));s4Draw(0);view("f:"+S4.title)};
  S4.step=fbDefault(fbData(S4.title));
  const sel=q('[aria-selected="true"]',cards);if(sel)cards.scrollLeft=sel.offsetLeft-cards.offsetLeft-4;
  const box=q("#lxFBox");
  box.innerHTML=`<div class="lx-fmeta" id="lxFMeta"></div><div class="lx-fs" id="lxFS" dir="auto" tabindex="0" aria-live="polite"></div><div class="lx-fnav"><button type="button" id="lxFPrev" aria-label="Earlier version">‹</button><div class="scrub" id="lxFScrub" aria-hidden="true"></div><button type="button" id="lxFNext" aria-label="Later version">›</button></div>`;
  q("#lxFPrev").onclick=()=>s4Go(-1);q("#lxFNext").onclick=()=>s4Go(1);
  const fs=q("#lxFS");
  drag(fs,{down:()=>({}),mv:(e,dx,dy,st)=>{if(!st.moved||still())return;fs.classList.add("drag");fs.style.transform=`translateX(${dx*.6}px)`;fs.style.opacity=String(1-Math.min(.6,Math.abs(dx)/400))},
    up:(e,moved,st)=>{fs.classList.remove("drag");const dx=e.clientX-st.x;if(moved&&Math.abs(dx)>40)s4Go(dx<0?1:-1,dx<0?-1:1);else{fs.style.transform="";fs.style.opacity="";if(!moved){const r=fs.getBoundingClientRect();s4Go(e.clientX>r.left+r.width/2?1:-1)}}}});
  fs.addEventListener("keydown",e=>{if(e.key==="ArrowRight"){e.preventDefault();s4Go(1)}if(e.key==="ArrowLeft"){e.preventDefault();s4Go(-1)}});
  const sc=q("#lxFScrub");
  const pick=e=>{const d=fbData(S4.title),r=sc.getBoundingClientRect(),f=clamp((e.clientX-r.left-6)/(r.width-12),0,1),t=d.steps[0].t+f*((d.steps[d.steps.length-1].t-d.steps[0].t)||1);let b=0,bd=1e18;d.steps.forEach((s,i)=>{const dd=Math.abs(s.t-t);if(dd<=bd){bd=dd;b=i}});if(b!==S4.step){S4.step=b;s4Draw(0)}};
  drag(sc,{down:e=>{pick(e);return {}},mv:e=>pick(e),up:()=>view("f:"+S4.title+":"+S4.step)});
  q("#lxFMari").addEventListener("click",e=>{const b=e.target.closest("[data-v]");if(!b)return;const d=fbData(S4.title),vid=+b.dataset.v;for(let i=d.steps.length-1;i>=0;i--)if(d.steps[i].vid===vid){S4.step=i;break}s4Draw(0)});
  s4Draw(0);
}
function s4Go(d,dir){const dd=fbData(S4.title);const n=clamp(S4.step+d,0,dd.steps.length-1);const fs=q("#lxFS");
  if(n===S4.step){fs.style.transform="";fs.style.opacity="";return}
  S4.step=n;view("f:"+S4.title+":"+n);
  if(still()){s4Draw(0);fs.style.transform="";fs.style.opacity="";return}
  const out=dir!=null?dir:(d>0?-1:1);fs.style.transform=`translateX(${out*40}px)`;fs.style.opacity="0";
  setTimeout(()=>{s4Draw(0);fs.classList.add("drag");fs.style.transform=`translateX(${-out*40}px)`;void fs.offsetWidth;fs.classList.remove("drag");fs.style.transform="";fs.style.opacity=""},170)}
function s4Draw(){
  const d=fbData(S4.title);if(!d)return;const st=d.steps[S4.step],prev=d.steps[S4.step-1],v=d.vs.get(st.vid);
  const vi=d.order.indexOf(st.vid)+1,views=d.views.get(st.vid);
  q("#lxFMeta").innerHTML=`<span><b>${DLL(st.d)}</b> · change ${N(S4.step+1)} of ${N(d.steps.length)}</span><span>wording ${vi} of ${N(d.total)} · live ${N(d.live.get(st.vid)||0)} days in all${views?` · about ${N(views)} reader views`:""}${st.rv?` · <span class="lx-rev">this edit was reverted</span>`:""}</span>`;
  const ps=prev&&d.vs.get(prev.vid).s,same=prev&&toks(ps)===toks(v.s);
  q("#lxFS").innerHTML=prev&&!same?wdiff(ps,v.s):E(v.s);
  if(same)q("#lxFMeta").insertAdjacentHTML("beforeend",`<span>only spacing or formatting changed</span>`);
  else if(!prev)q("#lxFMeta").insertAdjacentHTML("beforeend",`<span>the earliest version recorded</span>`);
  q("#lxFPrev").disabled=S4.step===0;q("#lxFNext").disabled=S4.step===d.steps.length-1;
  const sc=q("#lxFScrub"),w=Math.max(120,sc.clientWidth),h=44,t0=d.steps[0].t,t1=d.steps[d.steps.length-1].t,x=t=>6+(t-t0)/((t1-t0)||1)*(w-12);
  let s=`<svg viewBox="0 0 ${w} ${h}" width="${w}" height="${h}"><line class="axis" x1="6" x2="${w-6}" y1="22" y2="22"/>`;
  if(WARt>t0&&WARt<t1)s+=`<line class="war" x1="${x(WARt)}" x2="${x(WARt)}" y1="6" y2="38"/>`;
  const seenX=new Set();d.steps.forEach(p=>{const xx=Math.round(x(p.t));const k=xx*2+p.rv;if(seenX.has(k))return;seenX.add(k);s+=`<rect x="${xx-.5}" y="${p.rv?12:16}" width="1" height="${p.rv?20:12}" style="fill:var(${p.rv?"--del-bd":"--muted"})"/>`});
  s+=`<circle cx="${x(st.t)}" cy="22" r="7" style="fill:var(--ink);stroke:var(--sheet);stroke-width:2"/><text x="6" y="${h}" style="font-size:10px">${DL(d.steps[0].d)}</text><text x="${w-6}" y="${h}" text-anchor="end" style="font-size:10px">${DL(d.steps[d.steps.length-1].d)}</text></svg>`;
  sc.innerHTML=s;
  s4Mari(d,st.vid);
}
function s4Mari(d,cur){
  const el=q("#lxFMari"),w=Math.max(260,el.clientWidth),H=phone()?96:120,top=16;
  const vs=d.order.map(id=>d.vs.get(id)).filter(Boolean),LV=v=>d.live.get(v.id)||0,tot=vs.reduce((s,v)=>s+LV(v),0)||1;
  const mxv=Math.max(1,...vs.map(v=>d.views.get(v.id)||0));
  let s=`<svg viewBox="0 0 ${w} ${H+top+22}" width="${w}" height="${H+top+22}" role="img" aria-label="Each wording as a block: width days live, height readers">`;
  s+=`<defs><pattern id="lxH4" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="1.5" height="6" style="fill:var(--muted)" opacity=".5"/></pattern></defs>`;
  let x=0;const iw=w;
  vs.forEach((v,k)=>{const bw=Math.max(1,LV(v)/tot*iw),vw=d.views.get(v.id),hh=d.hasViews?(vw?Math.max(2,vw/mxv*H):3):H*.6,y=top+H-hh,isC=v.id===cur;
    s+=`<rect class="blk${isC?" cur":""}" data-v="${v.id}" x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${bw.toFixed(1)}" height="${hh.toFixed(1)}" style="fill:${isC?"var(--topic)":d.hasViews&&!vw?"url(#lxH4)":"var(--comp)"};opacity:${isC?1:.35+.4*(k%2)}"><title>${E(v.s.slice(0,140))} · ${N(LV(v))} days${vw?" · "+N(vw)+" views":""}</title></rect>`;
    const nr=d.rvBy.get(v.id)||0;if(nr){const nn=Math.min(nr,Math.max(1,Math.floor(bw/4)));for(let j=0;j<nn;j++)s+=`<rect class="notch" x="${(x+(j+.5)*bw/nn-1).toFixed(1)}" y="${(y-7).toFixed(1)}" width="2" height="6"/>`}
    x+=bw});
  s+=`<text x="0" y="10">↑ ${d.hasViews?"readers who saw it":"(reader counts not available)"}</text><text x="${w}" y="${H+top+16}" text-anchor="end">days live →</text><text x="0" y="${H+top+16}">${N(vs.length)} wordings · ${N(tot)} days</text></svg>`;
  el.innerHTML=s+`<p class="n" style="margin:0">One block per wording, oldest first. Wider: live longer${d.hasViews?". Taller: more reader views":""}. <span style="color:var(--del-ink)">Amber notch</span>: a reverted edit. Tap a block to jump.</p>`;
}

/* =====================================================================
   5. WORD CHIPS
   ===================================================================== */
const FR=(D&&D.frames)||[];
const PIN="placebo_geography";
const S5={on:[]};
const PAL=["--s2","--s1","--s4","--s3","--s5","--s6"];
let POOL=null;
function pool(){if(POOL)return POOL;POOL={};for(const [g,arr] of [["t",TOP],["c",CMP]]){POOL[g]={};const words=DATES.map(()=>0),cnt={};FR.forEach(k=>cnt[k]=DATES.map(()=>0));
    for(const a of arr){const m=ixMap(a);DATES.forEach((d,j)=>{const i=m[d];if(i==null||!a.words_series||!a.words_series[i])return;words[j]+=a.words_series[i];FR.forEach(k=>{const v=a.frame_series&&a.frame_series[k]&&a.frame_series[k][i];if(v)cnt[k][j]+=v})})}
    FR.forEach(k=>POOL[g][k]=cnt[k].map((c,j)=>words[j]?c*1e4/words[j]:null))}return POOL}
function s5Col(id){const i=S5.on.filter(x=>x!==PIN).indexOf(id);return id===PIN?"--muted":PAL[i%PAL.length]}
function s5Init(){
  const pal=q("#lxCPal");
  if(!FR.length||!hasSeries){pal.innerHTML="";q("#lxCChart").innerHTML=note("The word-group counts are missing from this build.");return}
  S5.on=["genocide","settler_colonial"].filter(k=>FR.includes(k));if(FR.includes(PIN))S5.on.push(PIN);if(!S5.on.length)S5.on=[FR[0]];
  pal.innerHTML=FR.map(k=>`<button class="lx-chip${k===PIN?" pin":""}" type="button" data-k="${k}" title="${k===PIN?"Pinned: the placebo should stay flat":"Tap, or drag onto the chart"}"><i></i>${E(frNm(k))}</button>`).join("");
  chipDrag(pal,"[data-k]",b=>({id:b.dataset.k,kind:"f"}));
  chipDrag(q("#lxCKey"),"[data-o]",b=>({id:b.dataset.o,kind:"legend"}));
  s5Draw();
}
function s5Toggle(id,force){const has=S5.on.includes(id);if(id===PIN){if(force===false||has){s5Msg("The placebo stays pinned. Rivers and mountains should not move. If they did, the method would be suspect.");return}}
  if(force===true&&has)return;if(force===false&&!has)return;
  if(has)S5.on=S5.on.filter(x=>x!==id);else{S5.on.push(id);const free=S5.on.filter(x=>x!==PIN);if(free.length>6)S5.on.splice(S5.on.indexOf(free[0]),1)}
  s5Draw();view("c:"+[...S5.on].sort().join(","))}
function s5Msg(t){const k=q("#lxCKey");let m=q(".lx-msg",k);if(!m){m=document.createElement("span");m.className="lx-msg n";k.append(m)}m.textContent=t;clearTimeout(m._t);m._t=setTimeout(()=>m.remove(),3200)}
function chipDrag(host,sel,info){
  let st=null;
  host.addEventListener("pointerdown",e=>{const b=e.target.closest(sel);if(!b||e.button>0)return;e.preventDefault();const it=info(b);st={b,it,x:e.clientX,y:e.clientY,id:e.pointerId,drag:false,fl:null};
    try{b.setPointerCapture(e.pointerId)}catch(_){}
    const M=ev=>{if(!st||ev.pointerId!==st.id)return;const dx=ev.clientX-st.x,dy=ev.clientY-st.y;
      if(!st.drag&&Math.hypot(dx,dy)>8){st.drag=true;const f=b.cloneNode(true);f.classList.add("lx-float");document.body.append(f);st.fl=f}
      if(st.drag){st.fl.style.left=ev.clientX+"px";st.fl.style.top=ev.clientY+"px";q("#lxCChart").classList.toggle("hot",overChart(ev))}};
    const U=ev=>{if(!st||ev.pointerId!==st.id)return;b.removeEventListener("pointermove",M);b.removeEventListener("pointerup",U);b.removeEventListener("pointercancel",U);q("#lxCChart").classList.remove("hot");
      const s=st;st=null;if(s.fl)s.fl.remove();if(ev.type==="pointercancel")return;
      const id=s.it.id;
      if(s.drag){const on=overChart(ev);if(on)s5Toggle(id,true);else if(S5.on.includes(id))s5Toggle(id,false)}
      else s5Toggle(id)};
    b.addEventListener("pointermove",M);b.addEventListener("pointerup",U);b.addEventListener("pointercancel",U)});
  host.addEventListener("keydown",e=>{const b=e.target.closest(sel);if(!b)return;if(e.key==="Enter"||e.key===" "){e.preventDefault();s5Toggle(info(b).id)}});
  host.addEventListener("contextmenu",e=>{if(e.target.closest(sel))e.preventDefault()});
}
function overChart(ev){const r=q("#lxCChart").getBoundingClientRect();return ev.clientX>=r.left&&ev.clientX<=r.right&&ev.clientY>=r.top-10&&ev.clientY<=r.bottom+10}
function s5Sync(){qa("#lxCPal [data-k]").forEach(b=>{const id=b.dataset.k,on=S5.on.includes(id);b.classList.toggle("on",on);b.setAttribute("aria-pressed",String(on));if(on)b.style.setProperty("--c",`var(${s5Col(id)})`)})}
function s5Draw(){
  const el=q("#lxCChart");if(!el||!FR.length)return;const P=pool();
  const ser=S5.on.map(id=>({id,name:frNm(id),t:P.t[id]||[],c:P.c[id]||[],col:s5Col(id)}));
  const W=Math.max(260,el.clientWidth),H=el.clientHeight||300,m={l:34,r:phone()?10:120,t:14,b:26};
  const t0=TM(DATES[0]),t1=TM(DATES[DATES.length-1]),x=t=>m.l+(t-t0)/((t1-t0)||1)*(W-m.l-m.r);
  let mx=0;ser.forEach(s=>[...s.t,...s.c].forEach(v=>{if(v!=null&&v>mx)mx=v}));mx=mx>0?mx*1.08:1;const tk=tickVals(0,mx,4);mx=Math.max(mx,tk[tk.length-1]);
  const y=v=>m.t+(1-v/mx)*(H-m.t-m.b);
  let s=`<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-label="Matches per 10,000 words over time">`;
  tk.forEach(v=>{s+=`<line class="grid" x1="${m.l}" x2="${W-m.r}" y1="${y(v)}" y2="${y(v)}"/><text x="${m.l-6}" y="${y(v)+4}" text-anchor="end">${F(v,v<10&&v%1?1:0)}</text>`});
  [...new Set(DATES.map(d=>d.slice(0,4)))].forEach(yr=>{const xx=x(Date.UTC(+yr,0,1));if(xx>=m.l&&xx<=W-m.r)s+=`<text x="${xx}" y="${H-6}" text-anchor="middle">${phone()?"’"+yr.slice(2):yr}</text>`});
  if(WARt>t0&&WARt<t1)s+=`<line class="war" x1="${x(WARt)}" x2="${x(WARt)}" y1="${m.t}" y2="${H-m.b}"/><text class="war" x="${x(WARt)+4}" y="${m.t+10}" style="font-size:10px">7 Oct 2023</text>`;
  const pth=(arr,ds)=>arr.map((v,i)=>v==null?"":`${i&&arr[i-1]!=null?"L":"M"}${x(TM(ds[i])).toFixed(1)},${y(v).toFixed(1)}`).join("");
  const ends=[];
  ser.forEach(se=>{const ds=DATES,sw=2.2;s+=`<path d="${pth(se.c,ds)}" fill="none" style="stroke:var(${se.col})" stroke-width="${sw}" stroke-dasharray="5 4" opacity=".85"/><path d="${pth(se.t,ds)}" fill="none" style="stroke:var(${se.col})" stroke-width="${sw+.6}"/>`;const lv=se.t[se.t.length-1];if(lv!=null)ends.push({y:y(lv),name:se.name,col:se.col})});
  if(!phone()){ends.sort((a,b)=>a.y-b.y);for(let i=1;i<ends.length;i++)if(ends[i].y-ends[i-1].y<13)ends[i].y=ends[i-1].y+13;ends.forEach(e=>{s+=`<text x="${W-m.r+6}" y="${e.y+4}" style="fill:var(${e.col});font-weight:600">${E(e.name.length>16?e.name.slice(0,15)+"…":e.name)}</text>`})}
  if(!ser.length)s+=`<text x="${(W)/2}" y="${H/2}" text-anchor="middle">Drag a chip here</text>`;
  el.innerHTML=s+"</svg>";
  q("#lxCKey").innerHTML=`<span><i style="--c:var(--ink)"></i>topic articles (${N(TOP.length)})</span><span><i class="d" style="--c:var(--ink)"></i>comparison (${N(CMP.length)})${CMP.length<FEW?" "+fewTag:""}</span>`+ser.map(se=>`<span class="lx-chip on${se.id===PIN?" pin":""}" data-o="${E(se.id)}" style="--c:var(${se.col});font-size:12px;padding:4px 10px;min-height:28px" role="button" tabindex="0" aria-label="${E(se.name)}${se.id===PIN?" (pinned)":", tap or flick off to remove"}"><i></i>${E(se.name)}${se.id===PIN?"":" ×"}</span>`).join("")+`<span class="n" style="width:100%">Matches per 10,000 words of full text, pooled over the articles measured at each date.</span>`;
  s5Sync();
}

/* =====================================================================
   6. LANGUAGE PRISM
   ===================================================================== */
const XL=D&&D.crosslang||null;
const S7={sort:"en",dir:-1,cmp:null,sel:null};
let XD=null;
const xlSum=x=>10*Object.values(x.rates||{}).reduce((a,b)=>a+(+b||0),0); /* crosslang stores per 1,000 words; shown per 10,000 */
function xlData(){if(XD)return XD;const langs=(XL.langs||[]).slice(),rows=[];
  for(const [t,L] of Object.entries(XL.articles||{})){const ch={},ld={};langs.forEach(l=>{const v=L[l];const s=v&&v.series;if(!s||s.length<2){ch[l]=null;return}ch[l]=xlSum(s[s.length-1])-xlSum(s[0]);ld[l]={a:s[0],b:s[s.length-1],title:v.title}});rows.push({t,ch,ld,n:langs.filter(l=>ch[l]!=null).length})}
  const all=rows.flatMap(r=>langs.map(l=>r.ch[l]).filter(v=>v!=null).map(Math.abs)).sort((a,b)=>a-b);
  return XD={langs,rows,M:all[Math.floor(all.length*.9)]||1}}
const xlCol=(v,M)=>{if(v==null)return "";const f=clamp(Math.abs(v)/M,0,1);return `color-mix(in oklab,var(${v>0?"--inc":"--dec"}) ${Math.round(f*100)}%,var(--mid))`};
function s7Init(){const el=q("#lxXGrid");if(!XL||!XL.articles||!Object.keys(XL.articles).length){el.innerHTML=note("The other-language data is not in this build.");return}
  el.addEventListener("click",e=>{const c=e.target.closest(".cell[data-r]");if(c&&!c.classList.contains("na")){S7.sel=[c.dataset.r,c.dataset.l];s7Draw();s7Cell();view("x:cell:"+c.dataset.r+":"+c.dataset.l);return}
    const b=e.target.closest("[data-back]");if(b){S7.cmp=null;s7Draw();return}});
  let st=null;
  el.addEventListener("pointerdown",e=>{const h=e.target.closest(".hdr");if(!h||e.button>0)return;st={h,l:h.dataset.l,x:e.clientX,y:e.clientY,id:e.pointerId,drag:false,fl:null};try{h.setPointerCapture(e.pointerId)}catch(_){}});
  el.addEventListener("pointermove",e=>{if(!st||e.pointerId!==st.id)return;if(st.l!=="en")return;if(!st.drag&&Math.hypot(e.clientX-st.x,e.clientY-st.y)>6){st.drag=true;const f=document.createElement("span");f.className="lx-pill lx-float";f.setAttribute("aria-pressed","true");f.textContent="English −";document.body.append(f);st.fl=f}
    if(st.drag){st.fl.style.left=e.clientX+"px";st.fl.style.top=e.clientY+"px";const t=hdrAt(e);qa(".hdr",el).forEach(x=>x.classList.toggle("tgt",x===t&&x.dataset.l!=="en"))}});
  const end=e=>{if(!st||e.pointerId!==st.id)return;const s=st;st=null;if(s.fl)s.fl.remove();qa(".hdr.tgt",el).forEach(x=>x.classList.remove("tgt"));if(e.type==="pointercancel")return;
    if(s.drag){const t=hdrAt(e);if(t&&t.dataset.l!=="en"){S7.cmp=t.dataset.l;s7Draw();view("x:cmp:"+S7.cmp)}return}
    if(S7.cmp&&s.l!=="en"){S7.cmp=s.l;s7Draw();view("x:cmp:"+s.l);return}
    if(S7.sort===s.l)S7.dir=-S7.dir;else{S7.sort=s.l;S7.dir=-1}s7Draw();view("x:sort:"+s.l+S7.dir)};
  el.addEventListener("pointerup",end);el.addEventListener("pointercancel",end);
  el.addEventListener("keydown",e=>{const h=e.target.closest(".hdr");if(h&&(e.key==="Enter"||e.key===" ")){e.preventDefault();if(S7.cmp&&h.dataset.l!=="en")S7.cmp=h.dataset.l;else{S7.sort=h.dataset.l;S7.dir=-1}s7Draw()}});
  s7Draw()}
function hdrAt(e){const t=document.elementFromPoint(e.clientX,e.clientY);return t&&t.closest&&t.closest("#lxXGrid .hdr")}
function s7Draw(){
  const el=q("#lxXGrid");if(!XL||!XL.articles)return;const X=xlData(),L=X.langs,cols=`minmax(84px,1.6fr) repeat(${L.length},minmax(0,1fr))`;
  const key=S7.cmp?(r=>r.ch.en!=null&&r.ch[S7.cmp]!=null?r.ch.en-r.ch[S7.cmp]:null):(r=>r.ch[S7.sort]);
  const rows=[...X.rows].sort((a,b)=>{const va=key(a),vb=key(b);if(va==null&&vb==null)return a.t.localeCompare(b.t);if(va==null)return 1;if(vb==null)return -1;return S7.dir*(va-vb)||0});
  let h=`<div class="lx-pg" style="grid-template-columns:${cols}"><span class="n" style="align-self:end;padding-bottom:6px;font-size:10.5px;line-height:1.25">${S7.cmp?"":"tap to sort<br>drag EN →"}</span>${L.map(l=>`<button type="button" class="hdr${l==="en"?" en":""}${S7.cmp===l?" tgt":""}" data-l="${l}" aria-pressed="${!S7.cmp&&S7.sort===l}" title="${E(LNG[l]||l)}${l==="en"?": drag onto another language":""}">${l.toUpperCase()}${!S7.cmp&&S7.sort===l?(S7.dir<0?"↓":"↑"):""}</button>`).join("")}</div>`;
  if(!S7.cmp){
    h+=`<div class="lx-pg" style="grid-template-columns:${cols};margin-top:2px">`+rows.map(r=>`<span class="rl rln" title="${E(r.t)}: ${r.n} of ${L.length} languages with data"><span>${E(r.t)}</span><span class="n">${r.n}</span></span>`+L.map(l=>{const v=r.ch[l],sel=S7.sel&&S7.sel[0]===r.t&&S7.sel[1]===l;return v==null?`<span class="cell na" title="${E(LNG[l]||l)}: no article, no data" aria-label="no data"></span>`:`<button type="button" class="cell${sel?" sel":""}" data-r="${E(r.t)}" data-l="${l}" style="background:${xlCol(v,X.M)}" aria-label="${E(r.t)}, ${E(LNG[l]||l)}: ${SG(v,1)}" title="${E(LNG[l]||l)}: ${SG(v,1)}"></button>`}).join("")).join("")+`</div>`;
    h+=`<div class="lx-ramp" style="margin-top:10px"><span>fell</span><i style="background:linear-gradient(90deg,var(--dec),var(--mid),var(--inc))"></i><span>rose</span><span>· change in loaded words per 10,000 words of opening paragraph, first to last snapshot</span><span><i class="lx-na" style="width:14px;height:10px;display:inline-block;vertical-align:-1px"></i> no data (no article in that language)</span><span>· the small number after each title: languages with data · ${N(X.rows.length)} articles</span></div>`;
  }else{
    const vals=rows.map(key).filter(v=>v!=null),M=Math.max(1e-9,...vals.map(Math.abs)),mm=mean(vals),few=vals.length<FEW;
    h+=`<div class="lx-row" style="margin:10px 0"><span class="lx-pill" aria-pressed="true">English minus ${E(LNG[S7.cmp]||S7.cmp)}</span><button type="button" class="lx-pill" data-back>Back to the grid</button><span class="n">tap another language to switch</span></div><div class="lx-pbars">`;
    h+=rows.map(r=>{const v=key(r);if(v==null)return `<div class="r"><span class="rl" title="${E(r.t)}">${E(r.t)}</span><span class="trk lx-na" style="height:14px"></span><span class="v">no data</span></div>`;const w=Math.abs(v)/M*50;return `<div class="r"><span class="rl" title="${E(r.t)}">${E(r.t)}</span><span class="trk"><i style="${v>=0?`left:50%`:`right:50%`};width:${w.toFixed(1)}%;background:var(${v>=0?"--inc":"--dec"})"></i><b></b></span><span class="v">${SG(v,1)}</span></div>`}).join("");
    h+=`<div class="r" style="margin-top:6px;border-top:1px solid var(--rule);padding-top:6px"><b>Average, ${vals.length} articles</b><span class="trk${few?" lx-few":""}"><i style="${mm>=0?"left:50%":"right:50%"};width:${(Math.abs(mm)/M*50).toFixed(1)}%;background:var(--ink);opacity:${few?.35:.8}"></i><b></b></span><span class="v">${SG(mm,1)}</span></div></div>`;
    h+=`<p class="n" style="margin-top:6px">Right of the line: English gained more loaded words per 10,000 words than ${E(LNG[S7.cmp]||S7.cmp)}. ${few?fewTag+" with fewer than "+FEW+" articles, so read the average as a description, not a finding.":""}</p>`;
  }
  el.innerHTML=h;
}
function s7Cell(){const el=q("#lxXCell");if(!S7.sel){el.innerHTML="";return}const [t,l]=S7.sel,r=xlData().rows.find(x=>x.t===t),d=r&&r.ld[l];if(!d){el.innerHTML="";return}
  const sm=xlSum;
  el.innerHTML=`<div class="lx-row" style="justify-content:space-between"><b>${E(d.title||t)} <span class="n">· ${E(LNG[l]||l)} · ${SG(r.ch[l],1)} per 10,000 words</span></b><button type="button" class="lx-pill" id="lxXClose">Close</button></div><div class="two"><div><small>${DL(d.a.date)} · ${F(sm(d.a),1)} per 10,000 words</small><p dir="auto" lang="${l}">${E(d.a.lead||"")}</p></div><div><small>${DL(d.b.date)} · ${F(sm(d.b),1)} per 10,000 words</small><p dir="auto" lang="${l}">${E(d.b.lead||"")}</p></div></div>`;
  q("#lxXClose").onclick=()=>{S7.sel=null;s7Cell();s7Draw()}}

/* =====================================================================
   7. GALAXY
   ===================================================================== */
const MS=D&&D.mass||null;
const S8={k:null,sel:null,anim:null,cur:null,all:false,band:{}};
let G8=null;
function gPrep(){if(G8)return G8;const t0=performance.now(),arts=MS.lab_articles,fr=MS.lab_frames||[],nd=(MS.dates||[]).length||3;
  const ci=(CRIT.length?CRIT:fr.slice(0,7)).map(k=>fr.indexOf(k)).filter(i=>i>=0);
  const n=arts.length,R_=[];for(let k=0;k<nd;k++)R_.push(new Float32Array(n).fill(NaN));
  for(let i=0;i<n;i++){const f=arts[i].f||[];for(let k=0;k<nd;k++){const s=f[k];if(!s||!s[0])continue;let c=0;for(const j of ci)c+=s[j+1]||0;R_[k][i]=c*1e4/s[0]}}
  const CH=R_.map(r=>{const o=new Float32Array(n);for(let i=0;i<n;i++)o[i]=r[i]-R_[0][i];return o});
  const projs=new Map();for(let i=0;i<n;i++){const p=arts[i].p||"(none)";if(!projs.has(p))projs.set(p,{p,g:arts[i].g,idx:[]});projs.get(p).idx.push(i)}
  const lanes=[...projs.values()].sort((a,b)=>(a.g===b.g?0:a.g==="t"?-1:1)||b.idx.length-a.idx.length);
  const ok=new Uint8Array(n);let born=0;for(let i=0;i<n;i++){ok[i]=isFinite(R_[0][i])?1:0;if(!ok[i])born++}
  const av=[];for(let k=1;k<nd;k++)for(let i=0;i<n;i++)if(ok[i]&&isFinite(CH[k][i]))av.push(Math.abs(CH[k][i]));av.sort((a,b)=>a-b);
  const Lraw=av.length?Math.max(1,av[Math.floor(av.length*.985)]):1;
  const u=new Float32Array(n);for(let i=0;i<n;i++)u[i]=hash(arts[i].t||String(i));
  const cl=lanes.filter(l=>l.g!=="t"),pooled={p:"All comparison projects",g:"c",pooled:true,nProj:cl.length,idx:cl.flatMap(l=>l.idx)};
  G8={arts,n,nd,CH,lanes,few:[...lanes.filter(l=>l.g==="t"),pooled],nComp:cl.length,ok,born,Lraw,u,prep:performance.now()-t0,lay:{}};return G8}
const gLanes=()=>S8.all?G8.lanes:G8.few;
function gLayout(w){const G=G8,ph=phone(),lanes=gLanes(),key=w+":"+ph+":"+S8.all;if(G.lay.key===key)return G.lay;const t0=performance.now();
  const laneH=ph?34:28,gut=ph?8:178,top=ph?50:50,iw=w-gut-14,st=niceStep(2*G.Lraw,ph?4:6),L=Math.ceil(G.Lraw/st-1e-9)*st,x=v=>gut+(clamp(v,-L,L)+L)/(2*L)*iw;
  let y=top;lanes.forEach(ln=>{ln.y0=y;ln.h=ln.pooled?laneH*2.4:laneH;y+=ln.h});
  const P=[];for(let k=0;k<G.nd;k++){const X=new Float32Array(G.n).fill(NaN),Y=new Float32Array(G.n);lanes.forEach(ln=>{const NB=60,hist=new Int32Array(NB),bin=new Int32Array(ln.idx.length);
      ln.idx.forEach((i,j)=>{const v=G.CH[k][i];const b=clamp(Math.floor((clamp(v,-L,L)+L)/(2*L)*NB),0,NB-1);bin[j]=b;if(G.ok[i]&&isFinite(v))hist[b]++});
      let mx=1;for(const c of hist)mx=Math.max(mx,c);const lab=ph?14:0,cy=ln.y0+lab+(ln.h-lab)/2,amp=(ln.h-lab)*.44;
      ln.idx.forEach((i,j)=>{const v=G.CH[k][i];X[i]=isFinite(v)?x(v):NaN;Y[i]=cy+(G.u[i]-.5)*2*amp*(.12+.88*Math.sqrt(hist[bin[j]]/mx))})});P.push({X,Y})}
  G.lay={key,P,lanes,gut,top,x,L,st,bot:y,h:y+(ph?38:30),ms:performance.now()-t0};return G.lay}
function gStats(ln,k){const G=G8,v=[];for(const i of ln.idx)if(G.ok[i]&&isFinite(G.CH[k][i]))v.push(G.CH[k][i]);return v}
/* chance band: shuffle the topic/comparison label 300 times, in chunks so the page stays responsive */
function gBand(k){if(S8.band[k]||k===0)return;const G=G8,vals=[],lab=[];for(let i=0;i<G.n;i++)if(G.ok[i]&&isFinite(G.CH[k][i])){vals.push(G.CH[k][i]);lab.push(G.arts[i].g==="t"?1:0)}
  const n=vals.length,nT=lab.reduce((a,b)=>a+b,0),V=Float64Array.from(vals);let tot=0,sT=0;for(let i=0;i<n;i++){tot+=V[i];if(lab[i])sT+=V[i]}
  const real=sT/nT-(tot-sT)/(n-nT),B=300,out=new Float64Array(B),r=rng(41+k),t0=performance.now();let b=0;const job={real,nT,nC:n-nT,ready:false};S8.band[k]=job;
  if(nT<2||n-nT<2){job.ready=true;job.lo=job.hi=NaN;return}
  const chunk=()=>{const end=Math.min(B,b+30);for(;b<end;b++){let s=0;for(let i=0;i<nT;i++){const j=i+((r()*(n-i))|0),t=V[i];V[i]=V[j];V[j]=t;s+=V[i]}out[b]=s/nT-(tot-s)/(n-nT)}
    if(b<B)setTimeout(chunk,0);else{out.sort();job.lo=out[Math.floor(B*.025)];job.hi=out[Math.floor(B*.975)];job.beat=out.filter(x=>Math.abs(x)>=Math.abs(real)).length;job.ready=true;job.ms=performance.now()-t0;
      window.LX_TIMING=Object.assign(window.LX_TIMING||{},{galaxy_shuffle_300_ms:+job.ms.toFixed(1)});if(S8.cur===k&&!S8.animating){gDraw(k);gSay()}}};
  setTimeout(chunk,0)}
function s8Init(){const box=q("#lxGBox");if(!MS||!MS.lab_articles||!MS.lab_articles.length){box.innerHTML=note("The ten-thousand-article sample is not in this build.");q("#lxGDates").innerHTML="";q("#lxGAll").hidden=true;return}
  gPrep();const ds=MS.dates||[];S8.k=ds.length-1;S8.cur=S8.k;
  const dseg=q("#lxGDates");dseg.innerHTML=ds.map((d,k)=>`<button type="button" data-k="${k}" aria-pressed="${k===S8.k}">${E(DL(d))}</button>`).join("");
  dseg.onclick=e=>{const b=e.target.closest("[data-k]");if(!b)return;const k=+b.dataset.k;if(k===S8.k)return;qa("[data-k]",dseg).forEach(x=>x.setAttribute("aria-pressed",String(x===b)));gBand(k);gGo(k);view("g:"+k)};
  const ab=q("#lxGAll"),abl=()=>{ab.textContent=S8.all?"Pool the comparison projects":`Show all ${G8.nComp} comparison projects`;ab.setAttribute("aria-pressed",String(S8.all))};abl();
  ab.onclick=()=>{S8.all=!S8.all;S8.sel=null;abl();gDraw(S8.cur);gSay();if(S8.all)view("g:all")};
  const cv=q("#lxGCan"),laneAt=e=>{const L=G8.lay,r=cv.getBoundingClientRect(),y=e.clientY-r.top;return L.lanes?L.lanes.findIndex(ln=>y>=ln.y0&&y<ln.y0+ln.h):-1};
  cv.addEventListener("click",e=>{if(!G8.lay.P)return;const li=laneAt(e),ln=gLanes()[li];S8.sel=ln&&S8.sel!==li?li:null;gDraw(S8.cur);gSay();if(S8.sel!=null)view("g:p:"+ln.p)});
  cv.addEventListener("pointermove",e=>{if(e.pointerType==="mouse")cv.style.cursor=laneAt(e)>=0?"pointer":"default"});
  gBand(S8.k);gDraw(S8.k);gSay();
}
function gGo(k){const from=S8.cur;S8.k=k;cancelAnimationFrame(S8.anim);
  if(still()){S8.cur=k;gDraw(k);gSay();return}
  const t0=performance.now(),D_=750,frames=[];S8.animating=true;
  const step=now=>{const t=Math.min(1,(now-t0)/D_),e=t<.5?4*t*t*t:1-(-2*t+2)**3/2;const f0=performance.now();gDraw(from,k,e);frames.push(performance.now()-f0);
    if(t<1)S8.anim=requestAnimationFrame(step);else{S8.animating=false;S8.cur=k;gDraw(k);gSay();const avg=frames.reduce((a,b)=>a+b,0)/frames.length;window.LX_TIMING=Object.assign(window.LX_TIMING||{},{galaxy_anim_frames:frames.length,galaxy_frame_avg_ms:+avg.toFixed(2),galaxy_frame_max_ms:+Math.max(...frames).toFixed(2)});console.info("[lab] galaxy animation",frames.length,"frames, avg",avg.toFixed(2),"ms, max",Math.max(...frames).toFixed(2),"ms")}};
  S8.anim=requestAnimationFrame(step)}
function gDraw(k0,k1,e){
  const G=G8,cv=q("#lxGCan");if(!G||!cv)return;const w=Math.max(260,q("#lxGBox").clientWidth);if(!w)return;const t0=performance.now();const L=gLayout(w),lanes=L.lanes,dpr=Math.min(2,devicePixelRatio||1),h=L.h;
  if(cv.width!==Math.round(w*dpr)||cv.height!==Math.round(h*dpr)){cv.width=Math.round(w*dpr);cv.height=Math.round(h*dpr);cv.style.height=h+"px"}
  const c=cv.getContext("2d");c.setTransform(dpr,0,0,dpr,0,0);c.clearRect(0,0,w,h);
  const col={t:tokv("--topic"),c:tokv("--comp"),ink:tokv("--ink"),mut:tokv("--muted"),faint:tokv("--faint"),sheet:tokv("--sheet")};
  const ph=phone(),mono=tokv("--mono")||"monospace",x0e=L.gut-4,we=w-L.gut;
  const kk=k1==null?k0:k1,pa=L.P[k0],pb=L.P[kk],ee=k1==null?1:e;
  let hp=null;
  lanes.forEach((ln,li)=>{if(li%2===0||ln.pooled){c.fillStyle=col.faint;c.globalAlpha=.55;c.fillRect(x0e,ln.y0,we,ln.h);c.globalAlpha=1}
    if(gStats(ln,0).length<FEW){if(!hp){const pc=document.createElement("canvas");pc.width=pc.height=6;const x=pc.getContext("2d");x.strokeStyle=col.mut;x.globalAlpha=.35;x.beginPath();x.moveTo(0,6);x.lineTo(6,0);x.stroke();hp=c.createPattern(pc,"repeat")}c.fillStyle=hp;c.fillRect(x0e,ln.y0,we,ln.h)}
    if(S8.sel===li){c.strokeStyle=col.ink;c.lineWidth=1.5;c.strokeRect(x0e+.5,ln.y0+.5,we-1,ln.h-1)}});
  // axis: ticks match the range; the end ticks read "or more"
  const x0=L.x(0);c.strokeStyle=col.ink;c.globalAlpha=.5;c.lineWidth=1;c.beginPath();c.moveTo(x0,L.top-4);c.lineTo(x0,L.bot);c.stroke();c.globalAlpha=1;
  c.font=`11px ${mono}`;c.fillStyle=col.mut;
  for(let v=-L.L;v<=L.L+1e-9;v+=L.st*(ph?2:1)){const vv=+v.toFixed(6),edge=Math.abs(Math.abs(vv)-L.L)<1e-9;c.textAlign=edge?(vv<0?"left":"right"):"center";c.fillText((edge?(vv<0?"≤":"≥"):"")+(vv>0?"+":vv<0?"−":"")+Math.abs(vv),L.x(vv),L.bot+14)}
  c.textAlign="right";c.fillText("change since "+DL((MS.dates||[])[0])+", per 10,000 words →",w-14,ph?h-1:12);
  // comparison mean line and chance band for the topic mean
  const pool=g=>{let s=0,n=0;for(const ln of G.lanes)if((ln.g==="t")===(g==="t")){for(const v of gStats(ln,kk)){s+=v;n++}}return n?s/n:NaN};
  const cm=pool("c"),tm=pool("t"),bd=S8.band[kk];
  if(kk>0&&isFinite(cm)){const yb=ph?20:20,hb=16;
    c.fillStyle=col.mut;c.font=`${ph?10:11}px ${mono}`;c.textAlign=ph?"left":"right";c.fillText("topic mean vs chance",ph?L.gut:L.gut-10,ph?yb-6:yb+12);
    if(bd&&bd.ready&&isFinite(bd.lo)){const a=L.x(cm+bd.lo),b=L.x(cm+bd.hi);c.fillStyle=col.c;c.globalAlpha=.28;c.fillRect(a,yb,Math.max(2,b-a),hb);c.globalAlpha=1}
    else{c.fillStyle=col.mut;c.textAlign="left";c.fillText("shuffling…",L.x(cm)+6,yb+12)}
    c.setLineDash([3,3]);c.strokeStyle=col.c;c.lineWidth=1.5;c.beginPath();c.moveTo(L.x(cm),yb-2);c.lineTo(L.x(cm),L.bot);c.stroke();c.setLineDash([]);
    if(isFinite(tm)&&k1==null){const xt=L.x(tm),ym=yb+hb/2;c.fillStyle=col.t;c.beginPath();c.moveTo(xt,ym-7);c.lineTo(xt+6,ym);c.lineTo(xt,ym+7);c.lineTo(xt-6,ym);c.closePath();c.fill()}}
  // dots, batched by colour
  const r=ph?1.15:1.35;
  for(const g of ["c","t"]){c.fillStyle=g==="t"?col.t:col.c;c.globalAlpha=g==="t"?.62:.5;c.beginPath();
    for(const ln of lanes){if(ln.g!==g)continue;for(const i of ln.idx){if(!G.ok[i])continue;const xa=pa.X[i],xb=pb.X[i];if(xa!==xa||xb!==xb)continue;const X=xa+(xb-xa)*ee,Y=pa.Y[i]+(pb.Y[i]-pa.Y[i])*ee;c.moveTo(X+r,Y);c.arc(X,Y,r,0,6.2832)}}
    c.fill()}
  c.globalAlpha=1;
  lanes.forEach(ln=>{const v=gStats(ln,kk),m=mean(v),y=ln.y0;
    if(isFinite(m)&&kk>0){const xx=L.x(m);c.fillStyle=col.ink;c.fillRect(xx-1,y+(ph?15:3),2,ln.h-(ph?18:6))}
    const nm=ln.pooled?(ph?"All comparison":"All comparison"):ln.p,lab=nm.length>(ph?26:21)?nm.slice(0,ph?25:20)+"…":nm,nT=gStats(ln,0).length,sub=N(nT)+(ln.pooled?` · ${ln.nProj} projects`:"")+(nT<FEW?" · too few to say":"");
    c.font=`${ph?600:500} ${ph?10.5:12}px ${mono}`;c.textAlign=ph?"left":"right";
    const tx=ph?L.gut:L.gut-10,ty=ph?y+11:y+ln.h/2+(ln.pooled?-2:1);
    c.fillStyle=ln.g==="t"?col.t:col.c;c.fillText(lab,tx,ty);
    c.fillStyle=col.mut;c.font=`${ph?10:10.5}px ${mono}`;
    if(ph)c.fillText(sub,tx+c.measureText(lab).width+(ph?16:0),ty);else c.fillText(sub,tx,ty+12)});
  const dt=performance.now()-t0;if(k1==null){window.LX_TIMING=Object.assign(window.LX_TIMING||{},{galaxy_prep_ms:+G.prep.toFixed(1),galaxy_layout_ms:+L.ms.toFixed(1),galaxy_static_draw_ms:+dt.toFixed(2),galaxy_dots:G.n})}
}
function gSay(){const G=G8,k=S8.cur,ds=MS.dates||[],el=q("#lxGSay"),L=G.lay;
  const pool=g=>{const v=[];G.lanes.forEach(ln=>{if((ln.g==="t")===(g==="t"))v.push(...gStats(ln,k))});return v};
  const T=pool("t"),C=pool("c"),mc=mean(C),bd=S8.band[k];
  const head=`<span class="n">${N(G.n-G.born)} articles${G.born?` (${N(G.born)} created later are left out)`:""}. Tick: row mean. Dashed: comparison mean. Beyond ±${N(L.L||G.Lraw)}: at the edge.</span> `;
  if(k===0){el.innerHTML=head+`At ${DL(ds[0])} every article starts at zero. Pick a later snapshot to watch them spread.`;return}
  if(S8.sel!=null){const ln=gLanes()[S8.sel],v=gStats(ln,k),m=mean(v),ci=bootMean(v,300,3),few=v.length<FEW;
    el.innerHTML=head+`<b>${E(ln.pooled?"All comparison projects":ln.p)}</b> (${ln.g==="t"?"topic":"comparison"}, ${N(v.length)} articles${few?", "+fewTag:""}): mean change <b>${SG(m,2)}</b> per 10,000 words (range ${SG(ci[0],2)} to ${SG(ci[1],2)})${ln.g==="t"?`, an extra change of <b>${SG(m-mc,2)}</b> over all ${N(C.length)} comparison articles`:""}. ${few||ln.g!=="t"?"":Math.abs(m-mc)<Math.max(ci[1]-ci[0],.05)?"Hard to tell apart from the comparison.":""}`;return}
  const ex=mean(T)-mc,band=bd&&bd.ready&&isFinite(bd.lo)?` 300 label shuffles give ${SG(bd.lo,2)} to ${SG(bd.hi,2)} (the band at the top); the real one is ${ex<bd.lo||ex>bd.hi?"<b>outside</b> it.":"<b>inside</b> it, so chance could do this."}`:" Shuffling labels to see what chance gives…";
  el.innerHTML=head+`By ${DL(ds[k])}: topic <b>${SG(mean(T),2)}</b> (${N(T.length)}), comparison <b>${SG(mc,2)}</b> (${N(C.length)}) per 10,000 words, an extra change of <b>${SG(ex,2)}</b>.${band}`}

/* ---------- init and redraw ---------- */
const LABS=[["shadow",s1Init,()=>{s1Strip();s1Draw()}],["shuffle",s2Init,()=>{const st=s2State(S2.id);if(st)s2Hist(st,null)}],["loud",s3Init,()=>s3Draw()],["flip",s4Init,()=>{if(S4.title)s4Draw()}],["chips",s5Init,s5Draw],["prism",s7Init,()=>{}],["galaxy",s8Init,()=>{if(G8)gDraw(S8.cur)}]];
const run=(nm,f)=>{try{f()}catch(e){console.error("[lab] "+nm,e)}};
let INIT=false,lastW=0;
function init(){if(INIT)return;INIT=true;
  const tb=document.querySelector(".tabs");if(tb)root.style.setProperty("--lx-tabs",tb.offsetHeight+"px");
  const vb=q("#lxViews");if(vb)vb.onclick=()=>{const w=q("#lxViewsWarn");w.hidden=!w.hidden;vb.setAttribute("aria-expanded",String(!w.hidden))};
  if(!D){root.querySelectorAll(".lx-sec").forEach(s=>s.insertAdjacentHTML("beforeend",note("Data not loaded. Run analyze.py, then build_page.py.")));return}
  LABS.forEach(([n,f])=>run(n,f));
  qa("#lxIndex a").forEach(a=>a.addEventListener("click",e=>{e.preventDefault();const el=document.getElementById(a.dataset.go);if(el)el.scrollIntoView({behavior:still()?"auto":"smooth",block:"start"})}));
}
function redraw(){if(!INIT)return;LABS.forEach(([n,,f])=>run(n,f))}
let rt=null;
const ro=new ResizeObserver(()=>{const w=root.clientWidth;if(!w)return;if(!INIT){lastW=w;init();return}if(Math.abs(w-lastW)<2)return;lastW=w;clearTimeout(rt);rt=setTimeout(redraw,120)});
ro.observe(root);
const themed=()=>{if(INIT&&G8)gDraw(S8.cur)};
matchMedia("(prefers-color-scheme: dark)").addEventListener("change",themed);
new MutationObserver(themed).observe(document.documentElement,{attributes:true,attributeFilter:["data-theme"]});
/* public hooks. The page calls WFD.lab.init(intent), .redraw() and .intent(intent).
   intent: {lab:"shadow"|"shuffle"|"loud"|"flip"|"chips"|"prism"|"galaxy", title?, article?, test?, measure?, part?, from?: report section id, context?} */
const LMAP={shadow:"lxShadow",shuffle:"lxShuffle",loud:"lxLoud",flip:"lxFlip",chips:"lxChips",prism:"lxPrism",galaxy:"lxGalaxy"};
const LNAME={shadow:"Shadow bars",shuffle:"Shuffle the labels",loud:"Pull the loudest out",flip:"Definition flipbook",chips:"Word chips",prism:"Language prism",galaxy:"Galaxy"};
function setTest(id){S2.id=S3.id=id;const L=PDEF[id]?`Pre-registered test ${id}: ${PDEF[id]}`:"";qa("#lxPSeg [data-p],#lxLSeg [data-p]").forEach(b=>b.setAttribute("aria-pressed",String(b.dataset.p===id)));const a=q("#lxPSegL"),b=q("#lxLSegL");if(a)a.textContent=L;if(b)b.textContent=L;run("shuffle",()=>s2Draw(true));run("loud",()=>s3Draw(true))}
function applyIntent(o){if(!o||!INIT)return;
  let go=LMAP[o.lab]?o.lab:null;const t=o.article||o.title,ctx=[];
  if(o.test&&PROWS.some(r=>r.id===o.test)){setTest(o.test);go=go||"shuffle";ctx.push(`pre-registered test ${o.test} (${PDEF[o.test]||""})`)}
  if(t&&RT&&RT[t]&&fbData(t)&&fbData(t).steps.length&&(!go||go==="flip")){S4.title=t;S4.step=fbDefault(fbData(t));qa("#lxFCards [data-t]").forEach(b=>{const on=b.dataset.t===t;b.setAttribute("aria-selected",String(on));if(on){const c=q("#lxFCards");c.scrollLeft=b.offsetLeft-c.offsetLeft-4}});run("flip",s4Draw);go=go||"flip";ctx.push(`the article “${t}”`)}
  else if(t){const a=TOP.find(x=>x.title===t);if(a){S1.open=a.subgroup||"other";go=go||"shadow"}ctx.push(`the article “${t}”`)}
  if((o.part==="lead"||o.part==="full")&&(!go||go==="shadow")&&!q("#lxSPart").hidden){S1.part=o.part;qa("#lxSPart [data-v]").forEach(b=>b.setAttribute("aria-pressed",String(b.dataset.v===o.part)))}
  const ms=o.measure;
  if(ms&&FR.includes(ms)){if(!S5.on.includes(ms))S5.on.unshift(ms);run("chips",s5Draw);go=go||"chips";ctx.push(`the word group “${frNm(ms)}”`)}
  else if(ms&&!go)go="shadow";
  if(DATES.includes(o.d0))S1.i0=DATES.indexOf(o.d0);if(DATES.includes(o.d1))S1.i1=DATES.indexOf(o.d1);
  run("shadow",()=>{s1Strip();s1Draw()});
  go=go||"shadow";
  const ban=q("#lxFrom"),sec=o.from&&document.getElementById(o.from);
  const secT=sec&&(sec.querySelector("h2,h3")||{}).textContent;
  ban.innerHTML=`<span>From the report${secT?` (“${E(secT.trim().slice(0,60))}”)`:""}: ${o.context||ctx.length?`<b>${E(o.context||ctx.join(", "))}</b>, `:""}now in <b>${E(LNAME[go])}</b>.</span><a href="#report" id="lxBack">← back to the report</a><button type="button" aria-label="Dismiss">×</button>`;ban.hidden=false;
  q("#lxBack").onclick=e=>{e.preventDefault();ban.hidden=true;const w=WF();if(sec&&typeof w.openInReport==="function")w.openInReport(o.from);else{location.hash="#report";if(sec)setTimeout(()=>sec.scrollIntoView(),40)}};
  q("button",ban).onclick=()=>{ban.hidden=true};
  const el=document.getElementById(LMAP[go]);if(el)setTimeout(()=>{el.scrollIntoView({behavior:"auto",block:"start"});ban.scrollIntoView&&0},30);
  view("intent:"+JSON.stringify(o));
  if(window.WFD)window.WFD.labIntent=null}
const W0=window.WFD=window.WFD||{};
W0.lab={init(o){if(root.clientWidth)init();applyIntent(o)},redraw,intent:applyIntent,
  open(id,o){o=Object.assign({},o||{},{lab:id});if(typeof W0.openInLab==="function")W0.openInLab(o);else{W0.labIntent=o;location.hash="#lab";setTimeout(()=>{init();applyIntent(o)},60)}}};
if(root.clientWidth)init();
})();
