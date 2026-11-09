"""The bilingual flash page: build_flash.py --bilingual OUT.html

One HTML file, two languages, a עברית / English switch in the masthead. The English page and the Hebrew page are built exactly as
`build_flash.py OUT.html` and `build_flash.py --lang he OUT.html` build them, with every English and Hebrew assertion; this module only
packs the two into one document:

  * the data (R) is in the file once; each language gets it at start-up (the Hebrew overlay relabels a few data strings, so Hebrew
    works on a structured clone, and the English data is never touched);
  * each language's markup and CSS sit in a <template>; its script (the research library plus the flash script, plus the Hebrew overlay
    for Hebrew) is wrapped in a function, so the two languages never share a variable;
  * the switch mounts a language on first use, keeps the other one's DOM and state in memory (detached), and swaps them without a
    reload. Window- and document-level listeners of the language that is not showing are muted; its queries go to its own detached
    nodes, so a timer of the hidden language can never touch the visible page;
  * the language is chosen in this order: ?lang=he|en, #lang=he|en, the reader's last choice (localStorage), the browser language
    (he* opens Hebrew, anything else English). The scroll position is kept across a switch (same element, same fraction).

In English mode the page's text is the English build's, in Hebrew mode the Hebrew build's; the only addition is the switch.
"""
import json, re

SWITCH = {
    "en": '<span class="lsw" role="group" aria-label="Language"><button type="button" data-lang="he" lang="he" dir="rtl" aria-pressed="false">עברית</button>'
          '<button type="button" data-lang="en" lang="en" aria-pressed="true">English</button></span>',
    "he": '<span class="lsw" role="group" aria-label="שפה"><button type="button" data-lang="he" aria-pressed="true">עברית</button>'
          '<button type="button" data-lang="en" lang="en" dir="ltr" aria-pressed="false">English</button></span>',
}
CSS = """.lsw{display:inline-flex;border:1px solid var(--rule);border-radius:999px;overflow:hidden;vertical-align:middle;margin-inline-end:10px;background:var(--paper)}
.lsw button{font:600 11.5px/1 var(--body);letter-spacing:0;text-transform:none;color:var(--ink-2);background:transparent;border:0;padding:5px 10px;min-height:26px;cursor:pointer}
.lsw button[lang="he"],.lsw button:not([lang]){font-family:Heebo,"Libre Franklin",Arial,sans-serif}
.lsw button[lang="en"]{font-family:"Libre Franklin","Helvetica Neue",Arial,sans-serif}
.lsw button[aria-pressed="true"]{background:var(--ink);color:var(--paper);cursor:default}
.lsw button:focus-visible{outline:2px solid var(--add-bd);outline-offset:-2px}
/* the same switch, floating, once the masthead has scrolled away (so the reader can switch mid-page) */
.lsw-f{position:fixed;z-index:30;bottom:calc(12px + env(safe-area-inset-bottom,0px));inset-inline-end:12px;margin:0;box-shadow:0 2px 10px rgb(0 0 0/.18);transition:opacity .2s,transform .2s}
.lsw-f.off{opacity:0;transform:translateY(8px);pointer-events:none;visibility:hidden}
@media (prefers-reduced-motion:reduce){.lsw-f{transition:none}}
@media print{.lsw-f{display:none}}
.mast>span:last-child{display:inline-flex;align-items:center;flex-wrap:wrap;gap:4px 0}"""

BOOT = r"""(function(){var l=null,q=/[?&]lang=(he|en)(?:&|$)/.exec(location.search),h=/[#&]lang=(he|en)(?:&|$)/.exec(location.hash),s=null;
try{s=localStorage.getItem("wfd-flash-lang")}catch(e){}
l=(q&&q[1])||(h&&h[1])||(s==="he"||s==="en"?s:null)||(/^(he|iw)(-|$)/i.test(navigator.language||"")?"he":"en");
window.__BI={want:l,act:null,roots:{},api:{},exp:[],T:/*TITLES*/null};var d=document.documentElement;d.lang=l;d.dir=l==="he"?"rtl":"ltr";document.title=__BI.T[l][0]})();"""

SWITCHER = r"""(function(){const B=window.__BI,D=document;
/* the per-language window and document: listeners are muted while the language is not showing; queries go to its own nodes */
function api(l){const act=()=>B.act===l,wm=new WeakMap();
  const wrap=f=>{if(!f||(typeof f!=="function"&&typeof f.handleEvent!=="function"))return f;let w=wm.get(f);if(!w){w=function(e){if(act())return typeof f==="function"?f.call(this,e):f.handleEvent(e)};wm.set(f,w)}return w};
  const on=T=>(t,f,o)=>T.addEventListener(t,wrap(f),o),off=T=>(t,f,o)=>T.removeEventListener(t,wm.get(f)||f,o);
  const root=()=>act()?D:B.roots[l].frag;
  const doc=new Proxy(D,{get(t,k){if(k==="addEventListener")return on(D);if(k==="removeEventListener")return off(D);
      if(k==="querySelector"||k==="querySelectorAll")return s=>root()[k](s);
      if(k==="getElementById")return id=>act()?D.getElementById(id):B.roots[l].frag.querySelector("#"+CSS.escape(id));
      const v=Reflect.get(t,k);return typeof v==="function"?v.bind(t):v},set(t,k,v){t[k]=v;return true}});
  const win=new Proxy(window,{get(t,k){if(k==="addEventListener")return on(window);if(k==="removeEventListener")return off(window);if(k==="document")return doc;
      const v=Reflect.get(t,k);return typeof v==="function"&&/^[a-z]/.test(String(k))?v.bind(t):v},set(t,k,v){t[k]=v;return true}});
  return {document:doc,window:win,add:on(window),rem:off(window)}}
/* the active language's top-level names on window (for the console and the smoke tests); never shadows a built-in */
function expose(G){B.exp.forEach(n=>{try{delete window[n]}catch(e){}});B.exp=[];
  Object.keys(G).forEach(n=>{if(n in window&&!Object.prototype.hasOwnProperty.call(window,n)&&D.getElementById(n)){}else if(n in window)return;try{void G[n]}catch(e){return}try{Object.defineProperty(window,n,{configurable:true,get(){return G[n]}});B.exp.push(n)}catch(e){}})}
/* scroll anchor: the smallest element with an id that spans the top of the viewport, and how far into it the top is */
function anchor(){let best=null;D.querySelectorAll("body [id]").forEach(e=>{if(!e.offsetParent||e.closest("dialog,template"))return;const r=e.getBoundingClientRect();
    if(r.height>0&&r.top<=1&&r.bottom>1&&(!best||r.height<best.h))best={id:e.id,h:r.height,f:-r.top/r.height}});return best}
function restore(a){if(!a)return;const e=D.getElementById(a.id);if(!e)return;const r=e.getBoundingClientRect();scrollTo({top:Math.round(scrollY+r.top+a.f*r.height),behavior:"instant"})}
const FL=D.createElement("div");FL.className="lsw lsw-f off";FL.setAttribute("role","group");
FL.innerHTML='<button type="button" data-lang="he" lang="he" dir="rtl">עברית</button><button type="button" data-lang="en" lang="en" dir="ltr">English</button>';
let IO=null;
function sync(){if(!FL.isConnected)D.body.append(FL);D.querySelectorAll(".lsw button").forEach(b=>b.setAttribute("aria-pressed",String(b.dataset.lang===B.act)));FL.setAttribute("aria-label",B.act==="he"?"שפה":"Language");
  const m=D.querySelector(".mast .lsw");if(IO)IO.disconnect();
  if(m&&"IntersectionObserver" in window){IO=new IntersectionObserver(E=>{const v=E.at(-1).isIntersecting;FL.classList.toggle("off",v);FL.inert=v});IO.observe(m)}}
function mount(l,opt){if(B.act===l)return;opt=opt||{};const prev=B.act,a=prev&&scrollY>2?anchor():null,top=prev&&scrollY<=2;
  if(prev){const P=B.roots[prev];try{B.api[prev].leave()}catch(e){console.error(e)}P.frag.append(...P.nodes)}
  B.act=l;const d=D.documentElement;d.lang=l;d.dir=l==="he"?"rtl":"ltr";document.title=B.T[l][0];const md=D.querySelector('meta[name="description"]');if(md)md.content=B.T[l][1];
  let P=B.roots[l];const first=!P;
  if(first){const f=D.getElementById("bi-"+l).content.cloneNode(true);P=B.roots[l]={frag:document.createDocumentFragment(),nodes:[...f.childNodes]};D.body.append(f)}
  else D.body.append(...P.nodes);
  if(first){B.api[l]=window["__L_"+l](api(l))}else{try{B.api[l].redraw()}catch(e){console.error(e)}}
  expose(B.api[l].names);sync();
  if(a){restore(a);const y0=scrollY;let moved=false;const mv=()=>{moved=true};addEventListener("wheel",mv,{once:true,passive:true});addEventListener("touchstart",mv,{once:true,passive:true});
    requestAnimationFrame(()=>requestAnimationFrame(()=>{if(!moved)restore(a)}));setTimeout(()=>{if(!moved)restore(a)},350);setTimeout(()=>{if(!moved)restore(a)},900)}
  else if(top)scrollTo({top:0,behavior:"instant"});
  if(opt.focus){const b=(opt.focus==="f"?FL:D.querySelector(".mast .lsw")||FL).querySelector(`button[data-lang="${l}"]`);if(b)b.focus({preventScroll:true})}
  window.dispatchEvent(new CustomEvent("flashlang",{detail:l}))}
B.mount=mount;
D.addEventListener("click",e=>{const b=e.target.closest&&e.target.closest(".lsw button[data-lang]");if(!b)return;e.preventDefault();const l=b.dataset.lang;if(l===B.act)return;
  try{localStorage.setItem("wfd-flash-lang",l)}catch(x){}mount(l,{focus:b.closest(".lsw-f")?"f":"m"})});
mount(B.want)})();"""


def split_page(page):
    """(style css, body markup, script) of one built language page"""
    assert page.startswith('<!DOCTYPE html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n')
    s0, s1 = page.index("<style>"), page.index("</style>")
    css = page[s0 + len("<style>"):s1]
    j0, j1 = page.index("<script>", s1), page.rindex("</script>")
    assert page.count("<script>") == 1 and page.count("<style>") == 1, "one style and one script per language page"
    head = page[:s0]
    body = page[s1 + len("</style>"):j0]
    js = page[j0 + len("<script>"):j1]
    assert not page[j1 + len("</script>"):].strip(), "nothing after the script"
    title = re.search(r"<title>(.*?)</title>", head).group(1)
    desc = re.search(r'<meta name="description" content="([^"]*)">', head).group(1)
    fonts = re.findall(r'<link rel="stylesheet" href="([^"]+)">', head)
    return dict(css=css, body=body, js=js, title=title, desc=desc, fonts=fonts, head=head)


def top_names(js):
    """declared names of a language script: candidates for the window getters. Names declared only in an inner scope fail the page's
    probe (a ReferenceError), so only the wrapper's own top-level names are exposed"""
    N = re.findall(r"(?<![\w$.])(?:function\*?|const|let|var|class)\s+([A-Za-z_$][\w$]*)", js)
    reserved = {"document", "window", "addEventListener", "removeEventListener", "__A"}
    return sorted(set(N) - reserved)


def wrap(lang, P, data):
    js = P["js"]
    stamp = "const R=" + data + ";"
    assert js.count(stamp) == 1, f"{lang}: the data line is not where the build put it"
    js = js.replace(stamp, "const R=__FLR;" if lang == "en" else "const R=structuredClone(__FLR);")
    assert "flInit();\n" in js and "function flRedraw(" in js and "function flLeave(" in js
    names = top_names(js)
    for must in ("BR", "BRS", "brText", "brLive", "brPP", "brRun", "brMove", "FB", "ZI", "XM", "flDraw", "flRedraw"):
        assert must in names, f"{lang}: top-level name {must} not found"
    getters = ",".join(f"get {n}(){{return {n}}}" for n in names)
    return (f"function __L_{lang}(__A){{const document=__A.document,window=__A.window,addEventListener=__A.add,removeEventListener=__A.rem;\n"
            f"{js}\nreturn {{redraw:flRedraw,leave:flLeave,names:{{{getters}}}}}}}")


def build(en_page, he_page, data, out_path):
    E, H = split_page(en_page), split_page(he_page)
    # the slim Data lab data (an inert JSON block) is the same in both languages: once, outside the templates
    lab = re.search(r'<script type="application/json" id="flLabData">.*?</script>', E["body"], flags=re.S).group(0)
    assert E["body"].count(lab) == 1 and H["body"].count(lab) == 1, "the lab data is the same in both language pages"
    E["body"], H["body"] = E["body"].replace(lab, ""), H["body"].replace(lab, "")
    lab += "\n"
    # the switch goes into each masthead, before the research link
    for lang, P in (("en", E), ("he", H)):
        m = re.search(r'(<div class="mast"><span>.*?</span><span>)(<a href=)', P["body"])
        assert m and P["body"].count('<div class="mast">') == 1, f"{lang}: masthead not found"
        P["body"] = P["body"][:m.end(1)] + SWITCH[lang] + P["body"][m.end(1):]
    # fonts: the Hebrew link loads the English faces too (a face downloads only when used)
    fam = lambda u: set(re.findall(r"family=([^:&]+)", u))
    assert set().union(*map(fam, E["fonts"])) <= set().union(*map(fam, H["fonts"])), "the Hebrew font link must carry the English faces"
    fonts = "".join(f'<link rel="stylesheet" href="{f}">' for f in H["fonts"])
    titles = json.dumps({"en": [_unesc(E["title"]), _unesc(E["desc"])], "he": [_unesc(H["title"]), _unesc(H["desc"])]}, ensure_ascii=False)
    head = (E["head"].split("\n", 1)[1])  # after the doctype line: title, meta, preconnects, font link, build comment
    head = re.sub(r'<link rel="stylesheet" href="[^"]+">', fonts, head, count=1)
    out = ('<!DOCTYPE html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n'
           '<html lang="en" dir="ltr">\n' + head +
           "<style>" + CSS + "</style>\n"
           "<script>" + BOOT.replace("/*TITLES*/null", titles) + "</script>\n"
           '<template id="bi-en"><style>' + E["css"] + "</style>" + E["body"] + "</template>\n"
           '<template id="bi-he"><style>' + H["css"] + "</style>" + H["body"] + "</template>\n"
           "<script>const __FLR=" + data + ";</script>\n" + lab +
           "<script>" + wrap("en", E, data) + "</script>\n"
           "<script>" + wrap("he", H, data) + "</script>\n"
           "<body>\n<script>" + SWITCHER + "</script>\n")
    assert out.count(data) == 1, "the data is in the file once"
    assert out.count('id="flLabData"') == 1, "the lab data is in the file once"
    assert out.startswith('<!DOCTYPE html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">')
    for lang, P in (("en", E), ("he", H)):
        assert P["body"].count('class="lsw"') == 1
    open(out_path, "w").write(out)
    print(f"bilingual: English and Hebrew in one page; data once ({len(data)/1e6:.2f} MB); wrote {out_path} ({len(out)/1e6:.2f} MB)")
    return out


def _unesc(s):
    import html
    return html.unescape(s)
