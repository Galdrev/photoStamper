"""The Hebrew flash edition: build_flash.py --lang he OUT.html

Called by build_flash.py after the English page has been built and every English assertion has passed. Nothing here touches
data logic or chart code: the English template, the research library (as the English build patched it) and the sliced research
markup are taken as they are, and only their words change, from wikitrends/flash_i18n_he.json. Each pair there is
[exact English text, Hebrew text]; a pair whose English text is missing fails the build, so a change to the English page cannot
slip through untranslated. wikitrends/flash_he_overlay.html adds the Hebrew type, the right-to-left mirroring, Hebrew dates, the
Hebrew share images and the Hebrew labels for data-driven strings.

Quotes are evidence. Every quoted Wikipedia sentence stays in its original language (English and Spanish left to right, Arabic and
Hebrew right to left) with our Hebrew translation directly under it; Hebrew translations use ״…״, so the curly quotes left on the
Hebrew page are exactly the original quotes, and the build checks them against the English page and the stored texts.
Notes, glossary and the full string map: patterns/flash/HE_TRANSLATION.md.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
HE_SCOPE = "הדוח מודד איך השתנה הנוסח של ערכי הליבה שאנשים קוראים, ולא אם מה שכתוב בו נכון, ואינו שופט את ניהול המלחמה או את התנהלותה של ממשלה כלשהי."
# Hebrew equivalents of the vetoed English wordings (messaging_check.md, spin_review.md, build_flash.py VETO and SPIN)
HE_VETO = ["מחשבה מאוחרת", "הערת אגב", "הערת שוליים", "העולם קורא", "שהעולם קורא", "64 מתוך", "47 מתוך", "שני הצדדים", "משני הצדדים",
           "ב־2021 / לפני המלחמה", "לפני המלחמה, שורות הפתיחה האלה", "לפני המלחמה שורות הפתיחה", "מתועד", "מתועדים", "תיעד", "תועד",
           "לטובת ישראל", "בכיוון של ישראל", "למה זה חשוב", "מדוע זה חשוב", "התוצאה.", "הערך של ישראל עצמה", "הערך של ישראל עצמו",
           "הערך ״ישראל״ עצמו", "רק חמאס", "אף ארגון אחר", "אף קבוצה אחרת", "מצא את ישראל אשמה", "קבע שישראל אשמה", "נמצאה אשמה",
           "רק כתביעה", "רק כתיק", "תיק משפטי בלבד",
           # v2 (three proofs, HE_FIXLOG.md): the sharpened, softened or ambiguous v1 renderings stay out
           "השמדה", "אינו מעריך", "יש שטענו", "מצד ישראל", "משקיעים רבות", "הצבעה במחנות", "לכלל הסגנון", "אך לא בקול",
           "פיגועים", "עובדה מוכחת", "והפגיעה", "מתקפות 7 באוקטובר",
           # final round (HE_FIXLOG2.md): "met" is passive (הוצג), not the views displaying; "abuses" of rights are הפרות
           "הציגו את הנוסח", "הציגה את הנוסח", "הצפיות הציגו", "ובפגיעה שיטתית", "וחוקרים רבים מאשימים", "שבהן נהרגו 1195", "גררו מאז ועד היום",
           # fix log 3 (HE_FIXLOG3.md): "armed incursions" is ״פשיטות חמושות״ (sudden, limited armed raids), not ״חדירות״ (penetration);
           # ״פלישות״ (invasion) would sharpen the English. Incursion = פשיטה everywhere on the page, the Jenin event included.
           "חדירות", "החדירה הישראלית", "פלישות חמושות"]
# English UI leftovers that must not reach the Hebrew page (data-driven strings, checked in the Hebrew sides of the string map)
HE_NO_EN = ["court case", '"n/a"', 'icj:"icj"', '<span class="pw">removed', '<span class="pw">added', "Our coding."]
# dates: a no-break space between the day and the month ("7 באוקטובר" never splits across lines)
MONTHS = "ינואר|פברואר|מרץ|אפריל|מאי|יוני|יולי|אוגוסט|ספטמבר|אוקטובר|נובמבר|דצמבר|ינו׳|פבר׳|אפר׳|אוג׳|ספט׳|אוק׳|נוב׳|דצמ׳"
DAY_MONTH = re.compile(r"(?<![\d.,])(\d{1,2}) (ב(?:%s))" % MONTHS)
nb = lambda x: DAY_MONTH.sub("\\1\u00a0\\2", x)
NUM = r"(?<![\w.])\d[\d,]*(?:\.\d+)?"
nums = lambda x: {n.rstrip(",") for n in re.findall(NUM, x)}


def apply(text, pairs, where, exact_once=False):
    for en, he in pairs:
        n = text.count(en)
        assert n >= 1, f"Hebrew build: English text not found in {where} (the English page changed?): {en[:90]!r}"
        assert not exact_once or n == 1, f"Hebrew build: English text occurs {n} times in {where}: {en[:90]!r}"
        text = text.replace(en, he)
    return text


def build(C, out_path):
    """C: the English build's context (template, library, CSS, slots, data, checkers, the English page)."""
    I = json.load(open(os.path.join(HERE, "flash_i18n_he.json")))
    for sec in ("template", "lib", "slots"):
        I[sec] = [[en, nb(he)] for en, he in I[sec]]
    for sec in ("events", "coding_notes", "columns"):
        I[sec] = {k: nb(v) for k, v in I[sec].items()}
    ov = open(os.path.join(HERE, "flash_he_overlay.html")).read()
    hcss = ov[ov.index('<style id="he-css">') + len('<style id="he-css">'):ov.index("</style>", ov.index('<style id="he-css">'))]
    hjs = ov[ov.index('<script id="he-js">') + len('<script id="he-js">'):ov.index("</script>", ov.index('<script id="he-js">'))]
    hjs_raw = hjs
    hjs = (hjs.replace("/*HE_EV*/{}", json.dumps(I["events"], ensure_ascii=False))
              .replace("/*HE_X*/{}", json.dumps(I["coding_notes"], ensure_ascii=False))
              .replace("/*HE_COL*/{}", json.dumps(I["columns"], ensure_ascii=False)))

    tpl = apply(C["tpl"], I["template"], "page_flash_template.html")
    lib = apply(C["lib"], I["lib"], "the research library", exact_once=True)
    slots = dict(C["SLOTS"])
    for en, he in I["slots"]:
        hit = [k for k, v in slots.items() if en in v]
        assert len(hit) == 1, f"Hebrew build: slot text must occur in exactly one sliced figure: {en[:80]!r} {hit}"
        slots[hit[0]] = apply(slots[hit[0]], [[en, he]], "#" + hit[0])
    # every event and coding note the page can show has a Hebrew label
    ev = {e["l"] for e in C["R"]["v3"].get("events", []) if e.get("t") in ("military_escalation", "ceasefire_deal")}
    assert ev <= set(I["events"]), f"Hebrew build: battles or ceasefires without a Hebrew label: {sorted(ev - set(I['events']))}"
    xs = {c["x"] for v in C["R"]["langs"]["cells"].values() for c in v.values() if c and c.get("x")}
    assert xs <= set(I["coding_notes"]), f"Hebrew build: grid notes without Hebrew: {sorted(xs - set(I['coding_notes']))}"
    assert set(I["columns"]) == {c[0] for c in C["R"]["langs"]["cols"]}, "Hebrew build: grid column names"

    # ---------------------------------------------------------------- checks on the Hebrew page text
    _Text, norm, quotes, corpus, all_corpus = C["_Text"], C["norm"], C["quotes"], C["corpus"], C["all_corpus"]
    page = _Text()
    page.feed(re.sub(r"<!--.*?-->", "", tpl, flags=re.S))
    text = {k: "".join(v) for k, v in page.buckets.items()}
    vis = " ".join(text.values())
    low = vis.lower()
    en_text, en_vis = C["text"], C["vis"]

    # (1) quotes are evidence: every curly-quoted string on the Hebrew page is stored text (the English build's check, unchanged),
    #     and the set of original quotes is the English page's: none dropped, none added, none altered
    bad = []
    for src, t in text.items():
        Cq = corpus(src) if src else None
        for q in quotes(t):
            for part in re.split(r"…|\.\.\.", q):
                part = norm(part).strip(" ,.;:")
                if len(part) < 3:
                    continue
                ok = any(part in c for c in Cq) if Cq is not None else part in all_corpus()
                if not ok:
                    bad.append((src or "any", part))
    assert not bad, f"Hebrew page: quotes not found in the stored text: {bad}"
    is_rtl = lambda q: len(re.findall(r"[֐-׿؀-ۿ]", q)) > len(re.findall(r"[A-Za-z]", q))
    qn = lambda q: norm(q).strip(" ,.;:")
    QE = {qn(q) for src, t in en_text.items() for q in quotes(t)}
    QE_orig = {qn(q) for src, t in en_text.items() for q in quotes(t)
               if src == "" or src == "arb" or src.startswith("en:") or is_rtl(q)}
    QH = {qn(q) for t in text.values() for q in quotes(t)}
    # final round (Hebrew length): an originals line under a heading may go when the very next block shows the same words in the
    # original, inside a longer quote; so every English original is on the Hebrew page, as a quote or inside a quoted original
    _inside = {q for q in QE_orig - QH if any(q in x for x in QH)}
    assert QE_orig - QH <= _inside, f"Hebrew page: original quotes missing or altered: {sorted(QE_orig - QH - _inside)}"
    assert len(_inside) <= 6, f"Hebrew page: originals shown only inside longer quotes: {sorted(_inside)}"
    assert QH <= QE, f"Hebrew page: quotes that the English page does not carry: {sorted(QH - QE)}"
    # the English translations of Hebrew, Arabic and Spanish quotes are the only quotes dropped (they are replaced by our Hebrew)
    dropped = QE - QH - _inside
    assert all(not src.startswith("en:") and src not in ("", "arb") for src, t in en_text.items() for q in quotes(t) if qn(q) in dropped), \
        "Hebrew page: only translations of non-English quotes may be dropped"
    # the hero stack: the same English then/now phrases, row by row (Israel's "then" is our own words, so it is Hebrew)
    rw = lambda s: re.findall(r'<li data-q="en:([^"]+)">.*?<span class="p"[^>]*><del>(.*?)</del>.*?<ins>(.*?)</ins>', s[s.index('id="flRw"'):s.index("</figure>", s.index('id="flRw"'))], flags=re.S)
    RE_, RH = rw(C["tpl"]), rw(tpl)
    assert [r[0] for r in RE_] == [r[0] for r in RH] and [r[2] for r in RE_] == [r[2] for r in RH] and RE_[1:] and [r[1] for r in RE_[1:]] == [r[1] for r in RH[1:]], f"hero stack: {RH}"
    # every original-language quote block is followed by our Hebrew translation (Hebrew Wikipedia quotes need none)
    blocks = [m.start() for m in re.finditer(r'<(?:span|p) class="(?:s|s then|he-q|q|p)"[^>]*dir="ltr" lang="en"', tpl)]
    for i, b in enumerate(blocks):
        nxt = blocks[i + 1] if i + 1 < len(blocks) else len(tpl)
        assert 'class="he-tr' in tpl[b:nxt], f"Hebrew page: an English quote without our translation under it: {tpl[b:b+160]!r}"
    nmo = tpl.count('class="he-tr he-mo"')
    assert len(blocks) >= 18 and nmo == 4, f"Hebrew page: translation blocks ({len(blocks)}, morph {nmo})"
    assert tpl.count("תרגום שלנו") >= 20, "Hebrew page: every translation is marked as ours"

    # (2) numbers: no new numbers. Static page text against the English page; every translated string against its English source
    en_nums = nums(en_vis) | set(C["COMPUTED"])
    new = sorted(nums(vis) - en_nums)
    assert not new, f"Hebrew page: numbers the English page does not print: {new}"
    def num_ok(pairs, where):
        for en, he in pairs:
            strip = lambda x: re.sub(r"<[^>]*>|\$\{[^}]*\}|style=\"[^\"]*\"|\d{4}-\d\d-\d\d", " ", x)
            extra = nums(strip(he)) - nums(en) - en_nums
            assert not extra, f"Hebrew build: {where}: numbers not in the English source: {sorted(extra)} in {he[:80]!r}"
    num_ok(I["lib"], "lib"); num_ok(I["slots"], "slots"); num_ok([[e, h] for e, h in I["template"]], "template")
    num_ok(list(I["events"].items()), "events"); num_ok(list(I["coding_notes"].items()), "coding notes")
    for lit in re.findall(r'"([^"\n]*)"|`([^`]*)`', hjs_raw):
        lit = "".join(lit)
        if re.search("[\u05d0-\u05ea]", lit):
            extra = nums(re.sub(r"\$\{[^}]*\}", " ", lit)) - en_nums
            assert not extra, f"overlay: numbers in a Hebrew string that the English page does not print: {extra} {lit[:60]!r}"

    # (3) the vetoed wordings, in English and in Hebrew
    he_all = vis + " " + " ".join(h for _, h in I["lib"] + I["slots"]) + " " + hjs + " " + " ".join(I["events"].values()) + " " + " ".join(I["coding_notes"].values())
    hit = [v for v in C["VETO"] if v in low] + [v for v in HE_VETO if v in he_all] + [v for v in C["SPIN"] if v in low]
    assert not hit, f"Hebrew page: vetoed wording: {hit}"
    he_sides = " ".join(h for _, h in I["template"] + I["lib"] + I["slots"])
    left = [v for v in HE_NO_EN if v in he_sides] + [v for v in HE_NO_EN if "pw" not in v and v in hjs]
    assert not left, f"Hebrew page: English UI strings left in the Hebrew string map: {left}"
    assert not DAY_MONTH.search(vis + " " + he_sides), f"Hebrew page: a date without a no-break space: {DAY_MONTH.search(vis + ' ' + he_sides).group(0)!r}"
    # "undone within a day" (בוטלה בתוך יום) is a Zionism result and stays in the Zionism slide
    assert he_all.count("בוטלה בתוך יום") == 1 and "המילה ״קולוניאלי״ הוצאה והוחזרה 10 פעמים מנובמבר 2024 עד אוגוסט 2026; כל הסרה בוטלה בתוך יום." in vis, "undone-within-a-day scope (Hebrew)"
    # the ten Gaza genocide attempts were "gone", not "undone"
    assert "כל אחת מהן נעלמה בתוך 45 דקות" in vis and "כל אחת נעלמה בתוך 45 דקות" in vis, "gone, not undone (Hebrew)"
    for who in ("Smallangryplanet", "Aquillion", "Zero0000", "Nableezy", "CaptainEek", "Elli", "AndreJustAndre"):
        assert not re.search(r"\b%s\b" % who, tpl), f"Hebrew page names an account: {who}"
    assert vis.count("Ïvana") == 1, "the Hebrew page names exactly one sanctioned account, once"

    # fix log 3: the owner's correction of "armed incursions" reaches every place it is shown (H2, the what-changed pair, the hero
    # stack row, the lanes, the reach key, the event labels, the grid's coding note)
    for must in ("כתוב היום ״פשיטות חמושות מתואמות״", "<ins>״פשיטות חמושות מתואמות״</ins>", "…פשיטות חמושות מתואמות</span>", "(פשיטות חמושות)"):
        assert nb(must) in tpl, f"Hebrew page: the incursions translation is missing: {must}"
    assert "״פשיטות חמושות״ (armed incursions)" in tpl and "״מתקפות״ ← ״פשיטות״" in lib, "Hebrew lanes and event labels: פשיטות"
    assert "״סדרה של פשיטות חמושות מתואמות״" in " ".join(I["coding_notes"].values()), "Hebrew grid note: פשיטות"
    # (4) the lines whose strength must not change
    assert HE_SCOPE in vis, "the scope line (Hebrew)"
    for must in ("הקשר: בהתאם להנחיות הסגנון של ויקיפדיה כולה לגבי תוויות שנויות במחלוקת, המילה ״טרוריסטי״ יצאה מהמשפטים הראשונים של הערכים על המדינה האסלאמית (דאעש), אל־שבאב ובוקו חראם. המשפט הראשון על חמאס לא כלל אותה ב־2021.",
                 "הערך על 7 באוקטובר מתאר את ההרג בקולה של ויקיפדיה: ״תוך טבח באזרחים ב־21 יישובים״; ״לפחות 1,195 בני אדם נהרגו כתוצאה מהמתקפות״",
                 "“Israel has denied that its actions constitute genocide.”", "״ישראל הכחישה שמעשיה מהווים רצח עם.״",
                 "המשפט הבא: תרגום שלנו״ישראל הכחישה שמעשיה מהווים רצח עם.״", "אין הכחשה",
                 "השינוי מרוכז בערכי הליבה שאנשים קוראים, בעוד הזנב הארוך של הדפים הקצרים כמעט לא השתנה.",
                 "זו הצבעה לפי מחנות, לא הוכחה לתיאום", "התזמון מלמד על מועד, לא על סיבה.", "הם לא נקבו בשמו של צד או של מדינה כלשהם.",
                 "המילים ״תנועת התנגדות״ נכנסו פעם אחת", "היא חזרה שלוש פעמים, לאחרונה בפברואר 2025.",
                 "ההסרה טרייה, וייתכן שתבוטל.", "פתיח הערך על ישראל: אין אזכור לחטופים, בכל עותק שבידינו מאז 2021.",
                 # v2: "destruction" is הרס, "Some have alleged" keeps its strength, the agent of "killed by" is kept
                 "״רצח העם בעזה הוא ההרס המתמשך, המכוון והשיטתי של העם הפלסטיני ברצועת עזה, שמבוצע בידי ישראל במהלך מלחמת עזה.״",
                 "על רצח עם ב־7 באוקטובר היא כותבת ״יש הטוענים״.", "״יש הטוענים שהמתקפה הייתה מעשה של רצח עם",
                 "שישראל מבצעת במהלך מלחמת עזה.״", "הבוררים של ויקיפדיה מצאו שלגורמים חיצוניים ״יש עניין רב בהשפעה״",
                 "בערך על ישראל, המשפט הבא:"):
        assert nb(must) in vis, f"Hebrew page: a line that must keep its strength is missing: {must[:60]}"
    # every translation is marked as ours, including the Israel and Netanyahu slide and both sides of the two morph slides
    for lab in ('<span class="he-tr"><b class="he-k">תרגום שלנו</b>״ישראל <ins>החלה', '<span class="he-tr"><b class="he-k">תרגום שלנו</b>״ממשלת נתניהו',
                '<span class="dn y">המשפט הבא: <b class="he-k">תרגום שלנו</b>״ישראל הכחישה'):
        assert lab in tpl, f"Hebrew page: a translation without its label: {lab[:60]}"
    assert tpl.count('<b class="he-k">תרגום שלנו · אז</b>') == 2 and tpl.count('<b class="he-k">תרגום שלנו · היום</b>') == 3, "morph slides: both sentences translated"
    assert '<b class="mk">ארגון טרור</b>' in tpl and 'class="tnm"' not in tpl, "Hebrew mirror: neutral mark only"
    assert "only hamas" not in low and not re.search(r"no other (group|armed group)", low)
    for _id in ("flRw", "c3", "c4vs", "c5vs", "c3m"):
        assert f'data-share="{_id}"' in tpl and f'id==="{_id}"' in hjs, f"Hebrew share card {_id}"
    # fix log 3: the hostages moment, in Hebrew. The scope lines keep their exact strength; each non-Hebrew first sentence has our
    # translation under it; the old Israel-and-Hamas line ("in every copy we hold", which our 2024 Hamas copies contradict) is gone
    # v3 fix (HE_FIXLOG4.md): the block leads with one plain headline; each slot says what it holds; the scope line is short and exact
    for must in ("<p class=\"vo-hl\">ב־7 באוקטובר נחטפו 251 בני אדם. ב־9&nbsp;מתוך 10 ויקיפדיות, המשפט הראשון של הערך אינו מזכיר אותם.</p>",
                 "<span class=\"vo-fu\">בתשע האחרות הם מוזכרים בהמשך פתיח הערך; באנגלית, רק במשפט&nbsp;9.</span>",
                 "<span class=\"vo-sc\">לפי העותקים האחרונים שלנו (אוקטובר–נובמבר 2026) של עשר הוויקיפדיות שיש בהן ערך על המתקפה. בעברית, המשפט הראשון הזכיר אותם בעותקים שלנו מאוקטובר 2024 עד אוקטובר 2025.</span>",
                 "אנגלית · רק כאן: משפט 9 בפתיח הערך", "פתיח הערך על חמאס: אין אזכור כיום; בעותקים שלנו מאפריל ומיולי 2024 נכתב בו",
                 "ובעותקים האחרונים שבידינו, פתיחי הערכים על ישראל ועל חמאס אינם מזכירים את החטופים."):
        assert nb(must) in tpl, f"Hebrew page: a hostages-moment line is missing or changed: {must[:60]}"
    assert "ובכל עותק שבידינו, פתיחי הערכים על ישראל ועל חמאס" not in tpl and "<b>פתיחי הערכים על ישראל ועל חמאס:</b>" not in tpl, "the old Israel-and-Hamas scope"
    _vo = tpl[tpl.index('id="c3m"'):tpl.index("</figure>", tpl.index('id="c3m"'))]
    assert _vo.count('class="vo-p"') == 10 and _vo.count('class="he-tr vo-tr"') == 9 and 'data-l="he" data-q="he:October 7 attacks" hidden><p class="vo-ph">ויקיפדיה בעברית' in _vo, "Hebrew moment panels: nine translations, Hebrew needs none"
    assert _vo.count('class="vo-gap"') == 9 and _vo.count('aria-label="אין חטופים במשפט הזה"') == 9, "Hebrew moment: nine empty slots in the panels"
    assert _vo.count('<span class="vo-h" aria-hidden="true">אין חטופים</span>') == 9 and '<span class="vo-hk">מזכיר אותם:</span> <span lang="it">rapimento</span>' in _vo, "Hebrew moment: the words in the slots"
    # v3 fix: the reach bar and the fight lanes, in Hebrew (numbers come from the same computed values as the English page)
    for must in ("<b>היום 7 מתוך 150 פתיחי הערכים הנקראים ביותר מאשימים את ישראל ברצח עם</b>, שניים מהם כעובדה, והם קיבלו <b>12.4%</b> מהצפיות בכל ה־150.",
                 'tag:["אין האשמה","מיוחסת לאחרים","נקבע כעובדה"]', "now:(n,p)=>`${n} פתיחים: ${p}% מהצפיות`", "rest:n=>`${n} פתיחים אחרים`",
                 "hd:w=>`<b>המאבק על המילים:</b> מאז ינואר 2021 הוכנסו למשפט הזה והוצאו ממנו ${w} מילים, חלקן שוב ושוב.`", 'st:["בחוץ","בפנים"],gl:l=>fbHe(l.lab)',
                 "כל שורה היא ביטוי אחד לאורך זמן: כחול = במשפט, ריק = מחוץ למשפט; כל סימון הוא עריכה אחת."):
        assert nb(must) in tpl, f"Hebrew page: a v3-fix line is missing or changed: {must[:60]}"
    assert 'window.claude.use("downloads")' in tpl and "window.claude.downloads" not in tpl + hjs, "downloads capability via use() only"
    assert "scope" in hjs[hjs.index("function shSpec"):] and "foot:[" in hjs, "Hebrew share cards carry the scope line"
    # the flash script quotes no English words that the English script did not (the English build checked those against the stored text)
    fjs_en, fjs_he = C["tpl"][C["tpl"].index("/* ---------- flash edition ---------- */"):], tpl[tpl.index("/* ---------- flash edition ---------- */"):]
    jq = lambda s: {q for q in re.findall(r"“([^”]+)”", s) if not re.search(r'[$"|+]', q)}
    assert jq(fjs_he) <= jq(fjs_en), f"Hebrew script quotes: {jq(fjs_he) - jq(fjs_en)}"
    # no English words left in the visible Hebrew page outside the original quotes and their English-language blocks
    from html.parser import HTMLParser
    # fix log 3: the hostages moment quotes the October 7 first sentence of ten editions in their own languages (lang-marked)
    QUOTE_LANGS = ("en", "es", "ar", "de", "fr", "it", "pt", "nl", "ru")
    class _NoEn(HTMLParser):
        """visible text outside every lang="en" / lang="es" / lang="ar" element and outside script, style and template"""
        VOID = ("br", "meta", "link", "input", "img")
        def __init__(self):
            super().__init__(convert_charrefs=True); self.st, self.out = [], []
        def handle_starttag(self, tag, a):
            if tag in self.VOID: return
            a = dict(a); self.st.append((tag, a.get("lang") in QUOTE_LANGS or tag in ("script", "style", "template")))
        def handle_endtag(self, tag):
            while self.st:
                if self.st.pop()[0] == tag: break
        def handle_data(self, d):
            if not any(x[1] for x in self.st) and d.strip(): self.out.append(d.strip())
    ne = _NoEn(); ne.feed(re.sub(r"<!--.*?-->", "", tpl, flags=re.S))
    allowed = re.compile(r"^(Ïvana|PIA5|PIA|ICJ|Español|o7)$")
    stray = [w for t in ne.out for w in re.findall(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ'’-]{2,}", t) if not allowed.match(w)]
    assert not stray, f"Hebrew page: English text outside a quote: {stray[:12]}"

    # ---------------------------------------------------------------- assemble (the English build's own steps)
    body = tpl
    for k, v in slots.items():
        body = body.replace(f"<!--R:{k}-->", v)
    body = C["lab_fill"](body, "he")  # the Data lab tab, Hebrew chrome (lab/lab_flash.py)
    n_lab = C["lab_check"](C["VETO"] + HE_VETO + C["SPIN"])
    i = body.index("</style>")
    body = body[:i] + hcss + body[i:]
    j = body.rindex("flInit();\n</script>")
    body = body[:j] + hjs + "\n" + body[j:]
    out = (body.replace("/*RESEARCH_CSS*/", C["css"])
               .replace("/*RESEARCH_JS*/", lib.replace("const R=/*DATA*/null;", "const R=" + C["data"] + ";", 1))
               .replace("@@R@@", C["RESEARCH_URL"]))
    assert "@@R@@" not in out and "/*RESEARCH_" not in out and "<!--R:" not in out and "/*HE_" not in out
    for k in slots:
        assert out.count(f'id="{k}"') == 1, f"#{k} must appear exactly once"
    out = re.sub(r"<!--VERIFY:[^>]*?-->", "", out)
    out = ('<!DOCTYPE html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n'
           '<html lang="he" dir="rtl">\n' + out)
    assert out.startswith('<!DOCTYPE html><meta charset="utf-8"><meta name="viewport"') and '<html lang="he" dir="rtl">' in out[:200]
    if out_path:
        open(out_path, "w").write(out)
    print(f"flash he: {len(I['template'])} template, {len(I['lib'])} library and {len(I['slots'])} figure strings; "
          f"{len(QH)} original quotes identical to the English page; {len(blocks)} quote blocks with our translation; "
          f"{len(nums(vis))} numbers, all on the English page; vetoes and scope line checked")
    if out_path:
        print(f"wrote {out_path} ({len(out)/1e6:.2f} MB)")
    return out
