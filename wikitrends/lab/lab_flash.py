"""The flash edition's Data lab tab: a slim, flash-only fork of the research edition's lab (lab.html, lab.js, lab.css).

The research files are read, never written, so the research edition (build_page.py inlines them as they are) stays byte-identical.
The fork is a list of exact replacements: each English target must occur in the research file (the build fails if lab.js changes
under it), so a fix in the research lab reaches the flash lab, and a change that breaks a patch is caught.

Slim data (`data()`): only the articles the flash uses (the six hero articles and the treemap's 150 openings) and only the two views
the flash links to: the definition flipbook (ratchet first-sentence histories, with the research edition's per-wording views) and
the language prism (crosslang, first and last snapshot only). The other five views need the full data set (about 10 MB); they show
"not in this edition" and link to the research edition's lab.

Hebrew (`lang="he"`): the lab's chrome is Hebrew; the data (article titles, the Wikipedia sentences) stays in the original.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = {k: open(os.path.join(HERE, f"lab.{k}")).read() for k in ("html", "js", "css")}
VIEWS_KEPT = ("flip", "prism")
LAB_URL = "@@R@@#lab"   # the research edition's Data lab tab (build_flash.py fills in the research edition's address)


def data(res, titles):
    """the slim lab data: flipbook (ratchet + exposure) and prism (crosslang) for `titles` only"""
    T = set(titles)
    rt = {t: {"fs_variants": [{"s": v["s"], "id": v["id"], "live_days": v.get("live_days")} for v in a.get("fs_variants") or []],
              "fs_n_variants": a.get("fs_n_variants"), "fs_timeline": a.get("fs_timeline")}
          for t, a in res["ratchet"]["articles"].items() if t in T}
    ex = {t: {"variants": [{"s": v["s"][:300], "views": v["views"]} for v in e.get("variants") or []]}
          for t, e in res["exposure"].items() if t in T and isinstance(e, dict)}
    xl = res["crosslang"]
    xa = {}
    for t, L in xl["articles"].items():
        if t not in T:
            continue
        xa[t] = {}
        for l, v in L.items():
            s = (v or {}).get("series") or []
            xa[t][l] = {"title": v.get("title"), "series": [{k: x.get(k) for k in ("date", "lead", "rates")} for x in (s[:1] + s[-1:] if len(s) >= 2 else s)]} if v else None
    D = {"dates": res["dates"], "first": res["first"], "last": res["last"], "pre_war": res["pre_war"], "critical": res["critical"],
         "frames": [], "did": [], "articles": [], "mass": None,
         "ratchet": {"articles": rt}, "exposure": ex, "crosslang": {"langs": xl["langs"], "articles": xa}}
    assert {"Israel", "Zionism", "Nakba", "October 7 attacks", "Hamas", "Gaza genocide"} <= set(rt), "slim lab: the six hero articles' first-sentence histories"
    assert set(rt) <= T and set(xa) <= T and set(ex) <= T, "slim lab: only the flash's articles"
    return D


# ---------------------------------------------------------------- the fork, both languages
def _sub(s, pairs, where):
    for a, b in pairs:
        n = s.count(a)
        assert n >= 1, f"lab_flash: patch target not found in {where} (the research lab changed?): {a[:90]!r}"
        s = s.replace(a, b)
    return s


MISS_EN = ('Not in this edition: this view needs the full data set. <a href="' + LAB_URL + '" target="_blank" rel="noopener">See the full lab ↗</a>')
MISS_HE = ('לא במהדורה הזאת: התצוגה הזאת דורשת את מערך הנתונים המלא. <a href="' + LAB_URL + '" target="_blank" rel="noopener">למעבדה המלאה (באנגלית) ↖</a>')

JS_SLIM = [
    # one lab per language page: the flash page passes its own FLX object (the bilingual page runs two labs side by side)
    ('const WF=()=>window.WFD||{};', 'const WF=()=>FLX;'),
    ('const W0=window.WFD=window.WFD||{};', 'const W0=FLX;'),
    ('if(window.WFD)window.WFD.labIntent=null', 'FLX.labIntent=null'),
    # the flash tabs are not sticky
    ('const tb=document.querySelector(".tabs");if(tb)root.style.setProperty("--lx-tabs",tb.offsetHeight+"px");', 'root.style.setProperty("--lx-tabs","0px");'),
    # the views whose data the slim set does not carry: "not in this edition", with a link to the full lab; never redrawn
    ('const note=msg=>`<p class="lx-note">${msg}</p>`;',
     'const note=msg=>`<p class="lx-note">${msg}</p>`;\nconst MISSED=new Set();\n'
     'function miss(id,nm){MISSED.add(nm);const s=document.getElementById(id);if(!s||s.classList.contains("lx-miss"))return;s.classList.add("lx-miss");'
     's.insertAdjacentHTML("beforeend",`<p class="lx-note lx-missn">${MISS}</p>`)}'),
    ('q("#lxSBars").innerHTML=note("The article time series are missing from this build, so the shadow bars cannot be drawn.");q("#lxSStrip").hidden=true;return',
     'miss("lxShadow","shadow");return'),
    ('q("#lxShuffle .lx-shuf").innerHTML=note("The pre-registered test results are missing from this build.");return', 'miss("lxShuffle","shuffle");return'),
    ('function s3Init(){\n', 'function s3Init(){if(!PROWS.length){miss("lxLoud","loud");return}\n'),
    ('pal.innerHTML="";q("#lxCChart").innerHTML=note("The word-group counts are missing from this build.");return', 'miss("lxChips","chips");return'),
    ('box.innerHTML=note("The ten-thousand-article sample is not in this build.");q("#lxGDates").innerHTML="";q("#lxGAll").hidden=true;return',
     'miss("lxGalaxy","galaxy");return'),
    ('function redraw(){if(!INIT)return;LABS.forEach(([n,,f])=>run(n,f))}', 'function redraw(){if(!INIT)return;LABS.forEach(([n,,f])=>{if(!MISSED.has(n))run(n,f)})}'),
    ('  run("shadow",()=>{s1Strip();s1Draw()});\n  go=go||"shadow";', '  if(!MISSED.has("shadow"))run("shadow",()=>{s1Strip();s1Draw()});\n  go=go||"flip";'),
    # the banner names the flash edition
    # (the section heading is not quoted: the flash headings carry quotes of their own, and a 60-character cut splits them)
    ('From the report${secT?` (“${E(secT.trim().slice(0,60))}”)`:""}:', 'From the flash edition:'),
    ('← back to the report</a>', '← back to the flash edition</a>'),
    ('location.hash="#report";if(sec)setTimeout(()=>sec.scrollIntoView(),40)', 'location.hash="#flash";if(sec)setTimeout(()=>sec.scrollIntoView(),40)'),
    # phone: the flipbook's "days live" axis label moves to the top line, clear of the bottom counts (they overlapped at 390 px)
    ('<text x="${w}" y="${H+top+16}" text-anchor="end">days live →</text>', '<text x="${w}" y="10" text-anchor="end">days live →</text>'),
]

HTML_SLIM = [
    ('<p class="lx-deck">Six hands-on views of the data behind the report. Drag, tap and shuffle the data itself. The pre-registered result stays on screen as a dashed outline.</p>',
     '<p class="lx-deck">Hands-on views of the data behind the report, in a slim version: this edition carries the data for two of the seven, '
     'the definition flipbook and the language prism, for the articles in the flash edition. The other five need the full data set; they are in the '
     '<a href="' + LAB_URL + '" target="_blank" rel="noopener">full lab ↗</a>.</p>'),
]

CSS_FLASH = """
/* flash: the slim lab */
.lx-miss>:not(.lx-h):not(.lx-missn){display:none!important}
.lx-miss{gap:8px;padding:12px 16px;margin-top:18px}.lx-miss .lx-note{padding:8px 10px;font-size:13px}
.lx-missn a{font-weight:600}
.lx-deck a{font-weight:600}
"""
CSS_RTL = """
/* flash, Hebrew: the lab's chrome right to left; time axes, scrubbers and charts stay left to right (earlier on the left) */
[dir=rtl] .lx svg,[dir=rtl] .lx-fnav,[dir=rtl] .lx-cards,[dir=rtl] .lx-mari,[dir=rtl] .lx-fs[dir=ltr]{direction:ltr}
[dir=rtl] .lx-card{direction:rtl;text-align:right}
[dir=rtl] .lx-card b{direction:ltr;unicode-bidi:isolate}
[dir=rtl] .lx-from button{margin-left:0;margin-right:auto}
[dir=rtl] .lx-pbars .rl,[dir=rtl] .lx-pg .rl{direction:ltr;text-align:right;unicode-bidi:isolate}
"""

# ---------------------------------------------------------------- Hebrew chrome
MON_HE = '["ינואר","פברואר","מרץ","אפריל","מאי","יוני","יולי","אוגוסט","ספטמבר","אוקטובר","נובמבר","דצמבר"]'
JS_HE = [
    ('const MON=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];', 'const MON=' + MON_HE + ';'),
    ('const DLL=s=>/^\\d{4}-\\d{2}-\\d{2}/.test(s||"")?(+s.slice(8,10))+" "+DL(s):DL(s);', 'const DLL=s=>/^\\d{4}-\\d{2}-\\d{2}/.test(s||"")?(+s.slice(8,10))+"\\u00a0ב"+DL(s):DL(s);'),
    ('const LNG={en:"English",de:"German",fr:"French",es:"Spanish",it:"Italian",nl:"Dutch",ru:"Russian",he:"Hebrew",ar:"Arabic",pl:"Polish",pt:"Portuguese"};',
     'const LNG={en:"אנגלית",de:"גרמנית",fr:"צרפתית",es:"ספרדית",it:"איטלקית",nl:"הולנדית",ru:"רוסית",he:"עברית",ar:"ערבית",pl:"פולנית",pt:"פורטוגזית"};'),
    ('w.textContent=SEEN.size===1?"view":"views"', 'w.textContent=""'),
    ('const fewTag=\'<span class="lx-fewtag">too few to say</span>\';', 'const fewTag=\'<span class="lx-fewtag">מעט מדי כדי לקבוע</span>\';'),
    # 4. definition flipbook
    ('"The revision-by-revision history of first sentences is not in this build."', '"ההיסטוריה של המשפטים הראשונים, גרסה אחר גרסה, אינה בגרסה הזאת."'),
    ('"No first-sentence versions were recorded."', '"לא נרשמו נוסחים של המשפט הראשון."'),
    ('<small>${N(d.total)} wordings · ${N(d.changes)} changes</small>', '<small>נוסחים: ${N(d.total)} · שינויים: ${N(d.changes)}</small>'),
    ('aria-label="Earlier version"', 'aria-label="הנוסח הקודם"'),
    ('aria-label="Later version"', 'aria-label="הנוסח הבא"'),
    ('`change ${N(S4.step)} of ${N(d.changes)}`:`starting wording · ${N(d.changes)} changes follow`',
     '`שינוי ${N(S4.step)} מתוך ${N(d.changes)}`:`הנוסח ההתחלתי · אחריו שינויים: ${N(d.changes)}`'),
    ('<span>wording ${N(st.vid+1)} of ${N(d.total)}${stored?` · live ${N(d.live.get(st.vid)||0)} days in all`:""}${views?` · about ${N(views)} reader views`:""}${st.rv?` · <span class="lx-rev">this edit was reverted</span>`:""}</span>',
     '<span>נוסח ${N(st.vid+1)} מתוך ${N(d.total)}${stored?` · ימים בתוקף בסך הכול: ${N(d.live.get(st.vid)||0)}`:""}${views?` · צפיות של קוראים: כ־${N(views)}`:""}${st.rv?` · <span class="lx-rev">העריכה הזאת בוטלה</span>`:""}</span>'),
    ('<span class="lx-nost">wording not stored (short-lived)</span>', '<span class="lx-nost">הנוסח לא נשמר (היה בתוקף זמן קצר)</span>'),
    ('<span>only spacing or formatting changed</span>', '<span>השתנו רק רווחים או עיצוב</span>'),
    ('<span>the previous wording was not stored, so changes are not highlighted</span>', '<span>הנוסח הקודם לא נשמר, ולכן השינויים אינם מסומנים</span>'),
    ('aria-label="Each wording as a block: width days live, height readers"', 'aria-label="כל נוסח כמלבן: הרוחב לפי הימים בתוקף, הגובה לפי הקוראים"'),
    ('<title>${E(v.s.slice(0,140))} · ${N(LV(v))} days${vw?" · "+N(vw)+" views":""}</title>', '<title>${E(v.s.slice(0,140))} · ימים: ${N(LV(v))}${vw?" · צפיות: "+N(vw):""}</title>'),
    ('↑ ${d.hasViews?"readers who saw it":"(reader counts not available)"}', '↑ ${d.hasViews?"קוראים שראו אותו":"(אין נתוני קוראים)"}'),
    ('text-anchor="end">days live →</text>', 'text-anchor="end">ימים בתוקף →</text>'),
    ('${N(vs.length)} stored wordings${d.unstored?` (+${N(d.unstored)} short-lived, not stored)`:""} · ${N(tot)} days</text>',
     'נוסחים שמורים: ${N(vs.length)}${d.unstored?` (ועוד ${N(d.unstored)} שהיו בתוקף זמן קצר ולא נשמרו)`:""} · ימים: ${N(tot)}</text>'),
    ('One block per wording, oldest first. Wider: live longer${d.hasViews?". Taller: more reader views":""}. <span style="color:var(--del-ink)">Amber notch</span>: a reverted edit. Tap a block to jump.',
     'מלבן לכל נוסח, מהישן (משמאל) לחדש. רחב יותר: בתוקף זמן רב יותר${d.hasViews?". גבוה יותר: יותר צפיות":""}. <span style="color:var(--del-ink)">חריץ כתום</span>: עריכה שבוטלה. הקישו על מלבן כדי לעבור אליו.'),
    # 6. language prism
    ('"The other-language data is not in this build."', '"הנתונים בשפות האחרות אינם בגרסה הזאת."'),
    ('${S7.cmp?"":"tap to sort<br>drag EN →"}', '${S7.cmp?"":"הקישו למיון<br>גררו את EN ←"}'),
    ('${l==="en"?": drag onto another language":""}', '${l==="en"?": גררו אל שפה אחרת":""}'),
    ('title="${E(r.t)}: ${r.n} of ${L.length} languages with data"', 'title="${E(r.t)}: יש נתונים ב־${r.n} מתוך ${L.length} שפות"'),
    ('title="${E(LNG[l]||l)}: no article, no data" aria-label="no data"', 'title="${E(LNG[l]||l)}: אין ערך, אין נתונים" aria-label="אין נתונים"'),
    ('<span>fell</span><i style="background:linear-gradient(90deg,var(--dec),var(--mid),var(--inc))"></i><span>rose</span><span>· change in loaded words per 10,000 words of opening paragraph, first to last snapshot</span>',
     '<span>ירד</span><i style="background:linear-gradient(270deg,var(--dec),var(--mid),var(--inc))"></i><span>עלה</span><span>· השינוי במונחים ביקורתיים לכל 10,000 מילים של פסקת הפתיחה, מהתמונה הראשונה לאחרונה</span>'),
    ('</i> no data (no article in that language)</span>', '</i> אין נתונים (אין ערך בשפה הזאת)</span>'),
    ('<span>· the small number after each title: languages with data · ${N(X.rows.length)} articles</span>', '<span>· המספר הקטן ליד כל שם ערך: השפות שיש בהן נתונים · ערכים: ${N(X.rows.length)}</span>'),
    ('aria-pressed="true">English minus ${E(LNG[S7.cmp]||S7.cmp)}</span>', 'aria-pressed="true">אנגלית פחות ${E(LNG[S7.cmp]||S7.cmp)}</span>'),
    ('data-back>Back to the grid</button><span class="n">tap another language to switch</span>', 'data-back>חזרה לטבלה</button><span class="n">הקישו על שפה אחרת כדי להחליף</span>'),
    ('<span class="v">no data</span>', '<span class="v">אין נתונים</span>'),
    ('<b>Average, ${vals.length} articles</b>', '<b>ממוצע, ערכים: ${vals.length}</b>'),
    ('Right of the line: English gained more loaded words per 10,000 words than ${E(LNG[S7.cmp]||S7.cmp)}. ${few?fewTag+" with fewer than "+FEW+" articles, so read the average as a description, not a finding.":""}',
     'מימין לקו: שיעור המונחים הביקורתיים (לכל 10,000 מילים) עלה באנגלית יותר מאשר ב${E(LNG[S7.cmp]||S7.cmp)}. ${few?fewTag+": פחות מ־"+FEW+" ערכים, ולכן הממוצע הוא תיאור ולא ממצא.":""}'),
    ('${SG(r.ch[l],1)} per 10,000 words</span></b><button type="button" class="lx-pill" id="lxXClose">Close</button>',
     '${SG(r.ch[l],1)} לכל 10,000 מילים</span></b><button type="button" class="lx-pill" id="lxXClose">סגירה</button>'),
    ('${F(sm(d.a),1)} per 10,000 words</small>', '${F(sm(d.a),1)} לכל 10,000 מילים</small>'),
    ('${F(sm(d.b),1)} per 10,000 words</small>', '${F(sm(d.b),1)} לכל 10,000 מילים</small>'),
    ('f.textContent="English −"', 'f.textContent="אנגלית −"'),
    # the banner and the hooks
    ('const LNAME={shadow:"Shadow bars",shuffle:"Shuffle the labels",loud:"Pull the loudest out",flip:"Definition flipbook",chips:"Word chips",prism:"Language prism",galaxy:"Galaxy"};',
     'const LNAME={shadow:"עמודות הצל",shuffle:"ערבוב התוויות",loud:"הוצאת הקיצוניים",flip:"דפדפת ההגדרות",chips:"אסימוני המילים",prism:"מנסרת השפות",galaxy:"הגלקסיה"};'),
    ('ctx.push(`the article “${t}”`)}\n', 'ctx.push(`הערך ${t}`)}\n'),
    ('`<span>From the flash edition: ${o.context||ctx.length?`<b>${E(o.context||ctx.join(", "))}</b>, `:""}now in <b>${E(LNAME[go])}</b>.</span><a href="#report" id="lxBack">← back to the flash edition</a><button type="button" aria-label="Dismiss">×</button>`',
     '`<span>מהמהדורה המקוצרת: ${o.context||ctx.length?`<b>${E(o.context||ctx.join(", "))}</b>, `:""}עכשיו ב<b>${E(LNAME[go])}</b>.</span><a href="#report" id="lxBack">→ חזרה למהדורה המקוצרת</a><button type="button" aria-label="סגירה">×</button>`'),
    ('note("Data not loaded. Run analyze.py, then build_page.py.")', 'note("הנתונים לא נטענו.")'),
]

HTML_HE = [
    ('<b>Data lab</b> · <span id="lxViewsN">0</span> <span id="lxViewsW">views</span> explored',
     '<b>מעבדת נתונים</b> · תצוגות שנבדקו: <span id="lxViewsN">0</span><span id="lxViewsW"></span>'),
    ('The more you slice, the more chance patterns you’ll find.', 'ככל שפורסים את הנתונים ליותר פרוסות, כך מוצאים יותר דפוסים מקריים.'),
    ('<div class="lx-eye">Data lab <span class="lx-x">Exploratory</span></div>', '<div class="lx-eye">מעבדת נתונים <span class="lx-x">גישוש</span></div>'),
    ('<span class="lx-x">Exploratory</span>', '<span class="lx-x">גישוש</span>'),
    ('<h1>Play with the evidence</h1>', '<h1>שחקו עם הראיות</h1>'),
    ('<p class="lx-deck">Hands-on views of the data behind the report, in a slim version: this edition carries the data for two of the seven, '
     'the definition flipbook and the language prism, for the articles in the flash edition. The other five need the full data set; they are in the '
     '<a href="' + LAB_URL + '" target="_blank" rel="noopener">full lab ↗</a>.</p>',
     '<p class="lx-deck">תצוגות מעשיות של הנתונים שמאחורי הדוח, בגרסה מצומצמת: המהדורה הזאת כוללת את הנתונים לשתיים משבע התצוגות, '
     'דפדפת ההגדרות ומנסרת השפות, לערכים שבמהדורה המקוצרת. חמש האחרות דורשות את מערך הנתונים המלא, והן ב'
     '<a href="' + LAB_URL + '" target="_blank" rel="noopener">מעבדה המלאה (באנגלית) ↖</a>.</p>'),
    ('<nav class="lx-index" aria-label="Labs" id="lxIndex">', '<nav class="lx-index" aria-label="התצוגות" id="lxIndex">'),
    ('<i>1</i>Shadow bars</a>', '<i>1</i>עמודות הצל</a>'), ('<i>2</i>Shuffle the labels</a>', '<i>2</i>ערבוב התוויות</a>'),
    ('<i>3</i>Pull the loudest out</a>', '<i>3</i>הוצאת הקיצוניים</a>'), ('<i>4</i>Definition flipbook</a>', '<i>4</i>דפדפת ההגדרות</a>'),
    ('<i>5</i>Word chips</a>', '<i>5</i>אסימוני המילים</a>'), ('<i>6</i>Language prism</a>', '<i>6</i>מנסרת השפות</a>'), ('<i>7</i>Galaxy</a>', '<i>7</i>הגלקסיה</a>'),
    ('<h2 id="lxShadowH">Shadow bars</h2>', '<h2 id="lxShadowH">עמודות הצל</h2>'), ('<h2 id="lxShufH">Shuffle the labels</h2>', '<h2 id="lxShufH">ערבוב התוויות</h2>'),
    ('<h2 id="lxLoudH">Pull the loudest out</h2>', '<h2 id="lxLoudH">הוצאת הקיצוניים</h2>'), ('<h2 id="lxFlipH">Definition flipbook</h2>', '<h2 id="lxFlipH">דפדפת ההגדרות</h2>'),
    ('<h2 id="lxChipsH">Word chips</h2>', '<h2 id="lxChipsH">אסימוני המילים</h2>'), ('<h2 id="lxPrismH">Language prism</h2>', '<h2 id="lxPrismH">מנסרת השפות</h2>'),
    ('<h2 id="lxGalH">Galaxy</h2>', '<h2 id="lxGalH">הגלקסיה</h2>'),
    ('<p class="lx-q">The first sentence is the definition most readers see. Pick an article, then swipe the sentence to flip through its versions.</p>',
     '<p class="lx-q">המשפט הראשון הוא ההגדרה שרוב הקוראים רואים. בחרו ערך, ואז החליקו את המשפט כדי לדפדף בין הנוסחים שלו.</p>'),
    ('aria-label="Articles"', 'aria-label="ערכים"'),
    ('<p class="lx-q">The same articles in other language Wikipedias. Each cell shows the change in loaded words in the opening paragraph, per 10,000 words. Tap a language to sort. Drag EN onto another language to subtract.</p>',
     '<p class="lx-q">אותם ערכים בוויקיפדיה בשפות אחרות. כל תא מראה את השינוי במונחים ביקורתיים בפסקת הפתיחה, לכל 10,000 מילים. הקישו על שפה כדי למיין. גררו את EN אל שפה אחרת כדי לחסר.</p>'),
]


def _sections_out(html):
    """the five views without data keep only their heading in the flash lab; their controls and texts are dropped from the markup"""
    for sid in ("lxShadow", "lxShuffle", "lxLoud", "lxChips", "lxGalaxy"):
        i = html.index(f'<section class="lx-sec" id="{sid}"')
        j = html.index("</section>", i)
        h0 = html.index('<div class="lx-h">', i)
        h1 = html.index("</div>", h0) + len("</div>")
        html = html[:i] + html[i:h0].rstrip() + "\n    " + html[h0:h1] + "\n  " + html[j:]
    return html


def html(lang):
    h = _sections_out(_sub(SRC["html"], HTML_SLIM, "lab.html"))
    if lang == "he":
        h = _sub(h, HTML_HE, "lab.html (Hebrew)")
    return h


def js(lang):
    s = _sub(SRC["js"], JS_SLIM, "lab.js")
    s = s.replace("const note=msg=>", "const MISS=" + json.dumps(MISS_HE if lang == "he" else MISS_EN, ensure_ascii=False) + ";\nconst note=msg=>", 1)
    if lang == "he":
        s = _sub(s, JS_HE, "lab.js (Hebrew)")
    return s


def css(lang):
    return SRC["css"] + CSS_FLASH + (CSS_RTL if lang == "he" else "")


HE_LAB_NO_EN = re.compile(r"[A-Za-z]{3,}")


def check_he(veto):
    """Hebrew chrome: every Hebrew run (between quotes, backticks and tags) has no English word (bar the EN language code) and no
    vetoed wording; dates get their no-break space in DLL"""
    strings = [b for _, b in JS_HE + HTML_HE] + [MISS_HE]
    n = 0
    for b in strings:
        for seg in re.findall(r'[^"`<>]*[\u05d0-\u05ea][^"`<>]*', b):
            t = re.sub(r"\$\{[^{}]*\}", " ", seg)
            t = re.sub(r"\$\{.*$|^[^{]*\}", " ", t)
            n += 1
            en = [w for w in HE_LAB_NO_EN.findall(t) if w != "EN"]
            assert not en, f"lab (Hebrew): English words in the chrome: {en} in {seg[:80]!r}"
            hit = [v for v in veto if v in t]
            assert not hit, f"lab (Hebrew): vetoed wording {hit} in {seg[:80]!r}"
    assert '"\\u00a0ב"+DL(s)' in js("he"), "lab (Hebrew): day and month joined by a no-break space"
    return n
