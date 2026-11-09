# Hebrew flash page: blind back-translation

Source: `scratchpad/flash/he1/index.html` (Hebrew build, `lang="he" dir="rtl"`), rendered in Playwright (Chromium headless shell 1243) with the iPhone 13 device profile, 9 Nov 2026.
Method: I extracted visible text in reading order (`innerText`), then tapped the grid tiles, chart marks, matrix cells and period chips. I toggled the "key words / every word" control, opened all `<details>`, opened all seven "play" sheets, and read the Hebrew aria-labels and titles. For the share images I read `shSpec()` and downloaded the four PNGs.
This step was blind: I opened no English page, string table or translation notes before finishing it.

Conventions: each item is the Hebrew text translated literally into English. Quoted English, Arabic or Spanish source text on the page is not translated; it is marked `[EN quote]`. Hebrew ״…״ quotes are rendered as "…". `[UI-EN]` marks interface text that the Hebrew page leaves in English.

---

## Page title and masthead

- `<title>`: "In brief: this is how English Wikipedia tells Israel's story today, 2021–2026"
- Skip link: "Skip to the cards"
- Masthead: "Framing drift on Wikipedia · The short edition"
- Link: "The full study (in English) ↖"
- Scope line: "Israel on Wikipedia, 2021–2026"
- Link: "All the evidence ←"

## Hero (opening lines)

- H1: "Before the war, no leading article accused Israel of genocide. Today the article on Israel accuses it of this."
- Deck: "Open these articles today. Their opening lines, then and now:"
- Buttons: "▶ Again" · "Save as image" (aria: "Replay the rewrite"; "Save the six lines as an image")
- Stamp: "Copy from 5 November 2026"
- Row 1 label: "Israel · the article's lead" · "July 2023 ← "genocide" (`“genocide”`) since 4 May 2025"
  - struck segment: "No accusation" → `[EN quote]` “began committing genocide”
  - "Our translation: No accusation of genocide ← "began to commit genocide""
- Row 2 label: "Zionism · the first sentence" · "1 January 2021 ← since 27 August 2026"
  - "Our translation: "re-establishment" ← "a Jewish homeland by means of colonization""
- Row 3 label: "Nakba · the first sentence" · "24 December 2021 ← since 6 July 2026"
  - "Our translation: "the destruction of Palestinian society" ← "the ethnic cleansing of Palestinian Arabs at the hands of Zionists""
- Row 4 label: "7 October · the first sentence" · "23 October 2023 ← since 9 December 2023"
  - "Our translation: "coordinated attacks" ← "coordinated armed incursions""
- Row 5 label: "Hamas · the first sentence" · "1 January 2021 ← since 29 November 2025"
  - "Our translation: "armed [man/militant]" ← "a political organisation possessing a military wing""
- Row 6 label: "Gaza genocide · the first sentence" · "1 January 2024 ← since 26 September 2025"
  - "Our translation: "accusations were raised" ← "that is being carried out at the hands of Israel""
- After the rows: "In the article on Israel, the next sentence:" `[EN quote]` → "Our translation: "Israel denied that its actions constitute genocide.""
- Grid caption: "150 leads of the most-read articles that existed in 2021. In January 2021 and in July 2023: not one accused Israel of genocide. Today seven accuse, two of them as fact."
- Grid aria-label: "150 squares, one for each lead of the most-read articles. In January 2021 and July 2023 not one of them accused Israel of genocide. Today seven accuse; two of them state it as fact."
- Tile aria: "Israel: stated as fact" · "Benjamin Netanyahu: stated as fact"
- Tile tap tooltip: "Israel · the article's lead / Stated as fact, in Wikipedia's voice / ×" (and "Benjamin Netanyahu · the article's lead")
- Legend: "No accusation" · "Accusation, attributed to others" · "Stated as fact"
- Glossary pop ("leading article"): "150 leads of the most-read articles on the topic that existed in 2021, checked in January 2021 and in July 2023."
- Scope disclaimer: "The report measures how the wording of the core articles people read has changed, and not whether the wording is correct, and it does not assess the conduct of the war or the conduct of any government."

## Card 1: Zionism

- Eyebrow: "1 Zionism" · "All the evidence ←"
- H2: "Zionism was the "re-establishment" of a Jewish state. Today it is "a Jewish homeland by means of colonization"."
- Interactive heading: "The same sentence, on any day you choose"
- Slider aria: "Movement in time: the first sentence as it read on that day"; pause aria: "Pause the passage through time"
- Version stamp (example): "12 July 2023 · version 31 of 169, in force until 24 October 2023 · 30 words removed and 23 added since January 2021"; at rest: "Today · version 168 of 169, in force now · 32 words removed and 23 added since January 2021"
- Drag hint: "◀ Drag along time ▶"
- Toggle: "Key words only" / "Every word that changed"; "❚❚ Pause"
- Caption (every word): "Every word removed since January 2021 is struck through; every word added is in blue. The key words are emphasised: "re-establishment" (re-establishment), "state" (state) and "colonization" (colonization)."
- Caption (key words only): "Key words only: "re-establishment" and "state" (left), "colonial" or "colonization" (entered). Other words also changed."
- Details: "Our translation: the sentence in 2021 and today"
  - "January 2021: "Zionism (Tsiyyonut, named after Zion) is both an ideology and a national movement among the Jewish people, which advocates the re-establishment of a Jewish state and support for it, in the territory defined as the historic Land of Israel (roughly overlapping Canaan, the Holy Land or the region of Palestine).""
  - "Today: "Zionism is an ethnic national movement that grew in Europe at the end of the nineteenth century in order to establish a Jewish homeland and to support it, by means of colonization in the region of Palestine, roughly overlapping the Land of Israel in Judaism, which is itself central to Jewish history.""
- Body: "Of the 41 removals of "colonization" (colonization) that can be checked, 37 were reverted."
- Button: "Every change, step by step"
- Bridge: "A change of the same kind reached 1948 as well."

## Card 2: 1948 and the Nakba

- Eyebrow: "2 1948 and the Nakba" · "All the evidence ←"
- H2: "The Nakba was "the destruction of Palestinian society". Today it is "the ethnic cleansing of Palestinian Arabs at the hands of Zionists"."
- Strip label: "Nakba · the first sentence · 2021 ← today · tap a mark"
- Lane labels: ""the destruction of Palestinian society"" · ""ethnic cleansing"" · ""at the hands of Zionists"" · "Changes to these words (15)"
- Strip aria: "The first sentence in the article Nakba: when it contained the destruction of Palestinian society, ethnic cleansing and at the hands of Zionists, and every change to these words"
- Mark aria: "A change to the first sentence in the article Nakba, [date]" (31 Aug 2022, 2 Nov 2022, 14 Jan 2023, 13 Oct 2023, 5 Mar 2024, 7 Apr 2024, 8 Apr 2024, 6 Jul 2026, 17 Jul 2026)
- Mark tooltip: "Nakba, the first sentence · [date]" · `[UI-EN]` "added"/"removed" · "The sentence after the edit (in the original, in English)"
- Body: "Three articles on 1948 name today, in Wikipedia's voice, who expelled the Palestinians: "Zionists" or "Zionist forces". Regarding the Jews who "fled or were expelled from Arab states", no agent is mentioned."
- Details "The two full sentences": "Nakba · December 2021 and since 6 July 2026 · the 2021 wording also took a position"
  - Then: "Our translation: "The Nakba, also known as the Palestinian Catastrophe, was the destruction of Palestinian society and homeland in 1948, and the permanent uprooting of most of the Palestinian Arabs.""
  - Today: "Our translation: "The Nakba (النَّكْبَة) is the ethnic cleansing of Palestinian Arabs at the hands of Zionists, by means of their violent uprooting and their dispossession of land, property and belongings …""
- Bridge: "And the change reached 7 October as well."

## Card 3: 7 October and the hostages

- Eyebrow: "3 7 October and the hostages" · "All the evidence ←"
- H2: "Wikipedia's first line on 7 October speaks today of "coordinated armed incursions". In 107 versions it has never mentioned the hostages."
- Block label: "What changed · October 2023 / January 2024 ← today"
  - "Our translation: "a series of coordinated attacks" ← "a series of coordinated armed incursions""
  - "Our translation: "rape and sexual assault at the hands of Hamas fighters" ← "dozens of cases of rape and sexual assault.""
- Strip label: "7 October · the first sentence · October 2023 ← today"
- Lanes: ""armed incursions" (armed incursions)" · ""massacre" (massacre) added: a dot for every day on which it entered" · "The hostages (hostages)" · "Never in the first sentence, in 107 wordings"
- Strip aria: "The first sentence in the article 7 October attacks: armed incursions, the days on which the word massacre entered, and the empty hostages row"
- Mark tooltips: ""massacre" (massacre) entered · 23 January 2024" · "… · 25 November 2025"
- Body: "The leads of the articles on Israel and on Hamas: no mention of the hostages, in any copy we hold since 2021. Sentence 9 in the lead on 7 October:" → "Our translation: "251 civilians and soldiers, Israelis and non-Israelis, were taken as hostages to the Gaza Strip""
- Body: "The lead still says "while massacring civilians in 21 communities", and the first sentence names Hamas, further on in it."
- Buttons: "Play the sentence on 7 October" · "Save as image" (aria "Save the card as an image")
- Bridge: "The organisation that carried out the attack also received a new definition."

## Card 4: Hamas, in English and in Hebrew

- Eyebrow: "4 Hamas, in English and in Hebrew" · "Evidence ←" · "Languages ←"
- H2: "In 2021 Wikipedia defined Hamas as an "armed" organisation. Today it is "a political organisation possessing a military wing"."
- "English" · "Hamas · the first sentence · since 29 November 2025" → "Our translation: "… is a Sunni Islamist Palestinian national political organisation possessing a military wing known as the al-Qassam Brigades.""
- "Hebrew" · "Preliminary" · "Hebrew Wikipedia · today (October 2026)" · [Hebrew Wikipedia quote, back-translated for reference: "Hamas (in Arabic: حماس) is a Palestinian Sunni-Islamist terror organisation that also operates as a political movement."]
- "The designation of it as a terror organisation moved from sentence 5 to sentence 22"
  - "1 January 2021 · sentence 5 of 20" (aria: "…the designation in sentence 5 of 20, 16% of the length of the lead")
  - "1 October 2026 · sentence 22 of 23" (aria: "…sentence 22 of 23, 96% of the length of the lead")
  - "Our translation: "Australia, Canada, … and the European Union declared Hamas a terror organisation.""
- Body: "Hebrew Wikipedia phrases it the other way round, as it already did in 2021. In English, "armed" left on 12 October 2023, five days after the attack. It returned three times, most recently in February 2025."
- Context: "Context: in line with Wikipedia's site-wide style rule regarding contested labels, the word "terrorist" left the first sentences of the articles on the Islamic State, al-Shabaab and Boko Haram. The first sentence on Hamas did not include it in 2021."
- Buttons: "Play the sentence on Hamas" · "Save as image" (aria "Save the definitions in English and in Hebrew as an image")
- Bridge: "And how do other Wikipedias phrase it?"

## Matrix: other languages

- Heading: "Other languages" · "Preliminary"
- Deck: "Eleven Wikipedias, five claims: our first copy, and after it today · tap a square" · "▶ Again"
- Short legend: "● In Wikipedia's voice" · "“ Attributed" · "? Disputed" · "– Not in the text we hold" · "… Further on in the lead" · "≈ A term in use, or "captives"" · "n/a No article (×)"
- Ring legend: "A ring marks a cell that changed: ▲ towards Wikipedia's voice, ▼ away from it. A ring alone marks a change that is not in voice."
- Modes: "Then ← now" · "Now only" · "Then only"
- Table caption: "How each language edition phrases 5 claims, the first copy and today"
- Columns: "Language · Genocide · Colonization · Apartheid · 7 Oct: terror · Hamas: terror" (titles: "Genocide", "Zionism as colonization", "Apartheid", "7 October as terror or massacre", "Hamas as terrorist")
- Footer row: "Stated as fact: then 0 / today 4 · then 0 / today 5 · then 0 / today 4 · then 4 / today 5 · then 2 / today 2"
- Full legend (details "Full legend · every square and mark"): "● Full, dot: stated as fact, in Wikipedia's voice" · "“ Striped, quotation marks: attributed to someone" · "? Dashed, ?: disputed in the same sentence" · "– Empty: not in the text we hold" · "… : further on in the lead, beyond the 1,200 characters we hold" · "≈ : in other words (Arabic: "took captive", not "hostages"; genocide in Italian and in Polish: presented as a name or as a term)" · "n/a Grey, no frame: no article in this language (× in the small square of the first copy)" · "Ring with ▲: moved closer to Wikipedia's voice; ▼: moved away" · "Ring alone: changed, but not in voice (for example, moved further on in the lead)"
- Details "Our coding · every column": `[UI-EN]` the note is in English ("Our coding. Genocide, colonization, apartheid and the Hamas label use the voice codes in our language file…").
- Cell aria pattern: "[Language], [claim]: in the first copy [state]; today [state][, moved closer to / away from Wikipedia's voice | , changed, but not in voice]. Enter shows the sentence here." English cells add "today (copy from 1 October 2026)".
- Cell tooltips (Hebrew parts):
  - "Hebrew · genocide · GAZA WAR": "Not in the text we hold ← attributed to others · changed, but not in voice"; Hebrew WP quote [back-translated for reference: "On 29 December 2023, against the backdrop of the fighting in the Gaza Strip, South Africa filed a suit against Israel at the International Court of Justice (ICJ) for genocide."]; "«רצח עם» = “genocide (lit. 'murder of a people')”"; "Hebrew Wikipedia · Gaza war · October 2026 · revision 43992663"; "To the full sentence, in the reading tool (in English) ←"
  - "Hebrew · colonization · ZIONISM": "Not in the text we hold, then and now"; "To the full sentence, then and now, in the reading tool (in English) ←"
  - "Hebrew · apartheid": "Attributed to others, then and now"
  - "Hebrew · 7 October: terror": "Terror or massacre, in Wikipedia's voice, then and now"; «טבח» = “massacre”
  - "Hebrew · Hamas: terror": "Stated as fact, then and now"; «ארגון טרור» = “terror organisation”
  - Arabic, genocide: "Attributed to others ← stated as fact · moved closer to Wikipedia's voice"; label "Our translation into English:" followed by English text `[UI-EN content]`; "Then · July 2024"
  - Arabic, 7 Oct: "None of the words in the first sentence, then and now"; ""a prolonged military operation" by "the Palestinian resistance factions"; today aimed "against the Israeli occupation"."
  - Arabic, Hamas: "No terror word in the text we hold; Hamas is "a Palestinian movement, of resistance, popular, Islamic, national"."
  - English cells: "today = our copy from 1 Oct 2026"; "English Wikipedia · … · our copy from 1 Oct 2026 · revision …"; "The English article leads have changed since this copy; the cards above quote the wording of 5 November 2026."
  - English, Zionism: "Further on in the lead ← stated as fact · changed, but not in voice"
  - English, 7 Oct: ""a series of coordinated armed incursions" by "Palestinian militant groups". A later sentence says "while massacring civilians"."
  - English, Hamas: "Attributed to others ← not in the text we hold · changed, but not in voice"; "English Wikipedia · Hamas · January 2021"
  - German, genocide: "Further on in the lead, then and now"; "No article linked to the English article Gaza genocide. In the article on the Gaza war there are 3 mentions of genocide, all beyond the text we hold."
  - German, Hamas: "Stated as fact ← attributed to others · moved away from Wikipedia's voice"
  - Italian, genocide: "A term in use, then and now"
  - Italian, Zionism: "Not in the text we hold ← stated as fact · changed, but not in voice"
  - Spanish, 7 Oct: ""the name used by the Palestinian armed Islamist group Hamas"; today "a series of coordinated attacks". A later sentence says that the militiamen "massacred civilians"."
  - Portuguese, 7 Oct: ""a series of coordinated attacks"; today "coordinated attacks [atentados]", a sharper noun."
  - Dutch, genocide: "Disputed in the same sentence, then and now"
  - Dutch, 7 Oct: "None of the words in the first sentence ← terror or massacre, in Wikipedia's voice · changed, but not in voice"
  - Russian, genocide: "No article linked to the English article Gaza genocide. The article on the Gaza war mentions genocide only beyond the text we hold."
  - Russian, 7 Oct: ""the invasion of Israel". A later sentence calls it "the largest Palestinian act of terror in history"."
- Bridge: "And then came the accusation itself."

## Card 5: The accusation, in two voices

- Eyebrow: "5 The accusation, in two voices" · "Evidence ←" · "Languages ←"
- H2: "Wikipedia writes that the genocide in Gaza "is being carried out at the hands of Israel". About genocide on 7 October it writes "some have claimed"."
- "What changed · Gaza genocide, 2024 ← since 26 September 2025" → "Our translation: "accusations were raised" ← "that is being carried out at the hands of Israel""
- "In Wikipedia's voice" · "Gaza genocide · the first sentence · since 26 September 2025" → "Our translation: "The Gaza genocide is the ongoing, deliberate and systematic annihilation of the Palestinian people in the Gaza Strip, being carried out at the hands of Israel during the Gaza war.""
- "Attributed to others" · "7 October attacks · the article's lead · today" → "Our translation: "Some have claimed that the attack was an act of genocide or a massacre of a genocidal character against Israelis.""
- Button: "Save as image" (aria "Save the two sentences as an image")

### Carousel 1: "The accusation, everywhere" ("Swipe ← 1 of 5")

- Slide 1, "Headings": "The title of the genocide article, by language" · "Preliminary"
  - Rows: "Hebrew · he: None" · "Arabic: +110 days, new name +180" · "English: first, new name +187" · "German: none" · "French: +4 days, new name +315" · "Spanish: +300 days" · "Italian: +321 days" · "Portuguese: +124 days, new name +198" · "Dutch: +499 days, new name +720" · "Polish: +379 days, new name +849" · "Russian: none" · axis "0 / 500 / 1000 days"
  - Titles: "Title without "allegations": [date]"
  - Body: "English removed "allegations" from the title on 3 July 2024 (+187 days); Polish on 26 April 2026 (+849 days)."
  - aria: "The article on the genocide: when it was opened and when its name was changed: English 29 December 2023; title without "allegations" 3 July 2024 (+187 days); … Hebrew, German and Russian: no linked article."
- Slide 2, "Arabic": "Arabic · Gaza genocide · the first sentence" · "Preliminary" · "To the reading tool" · "Then · July 2024" · "▶ Again" · [Arabic quote skipped]
  - "Our translation: "Israel was accused of committing crimes of genocide against the Palestinian people in the Gaza Strip during the war between Israel and Hamas.""
  - ""Israel was accused of committing crimes of genocide" ← "The genocide of Gaza is the destruction and targeting, systematic, deliberate and ongoing""
- Slide 3, "Spanish": "Spanish · Gaza war · the first sentence" · "Preliminary" · "Then · January 2024" · [Spanish quote skipped]
  - "Our translation: "The Israel–Gaza war of 2023 is an ongoing armed conflict that began on 7 October 2023, while the Israelis were celebrating the Sukkot holiday, when armed groups of Palestinian militiamen, mainly from Hamas and Palestinian Islamic Jihad, launched a large attack against Israel from the Gaza Strip, with a barrage of rockets and a commando raid in trucks, on motorcycles and on motorised paragliders.""
  - ""launched a large attack against Israel" ← "a retaliatory attack … which unleashed a genocide in Gaza on the part of Israel""
- Slide 4, "Israel and Netanyahu": "The leads of the articles · today · in Wikipedia's voice"
  - "Israel": "Israel began to commit genocide against Palestinians in Gaza." · "The next sentence: "Israel denied that its actions constitute genocide.""
  - "Benjamin Netanyahu": "Netanyahu's government is orchestrating the genocide in Gaza, a process that reached its peak in the case South Africa v. Israel at the International Court of Justice (ICJ) in December 2023." · "No denial"
  - Body: "The article on Israel brings the denial in the next sentence; the article on Netanyahu does not bring a denial."
- Slide 5, "Hebrew, the exception": "Hebrew · the exception" · "Preliminary" · "To the reading tool" · [Hebrew WP quote: "South Africa filed a suit against Israel at the International Court of Justice (ICJ) for genocide."]
  - Body: "The Hebrew article on the Gaza war does not state the accusation. It reports only the suit by South Africa."
- After the carousel: "The article on 7 October describes the killing in Wikipedia's voice: "while massacring civilians in 21 communities"; "at least 1,195 people were killed in the attacks" (copy from 2 November 2026)."
- Bridge: "How did these lines get there? In four first sentences, the history shows which wording remained and which was removed."

## Card 6: How it happened

- Eyebrow: "6 How it happened" · "Evidence ←" · "Timing ←"
- H2: "Since September 2025, 10 edits tried to return attributed wording to the sentence on the Gaza genocide. Each one of them disappeared within 45 minutes."

### Carousel 2: "How long a word holds" ("Swipe ← 1 of 3")

- Slide 1 "Gaza genocide": "Gaza genocide · the first sentence · December 2023 ← today" · "Every change" · lanes "In Wikipedia's voice" · "Attributed: allegedly, accused, according to" · "Attempts to restore attribution since 26 Sept 2025 (10)"
  - Caption: "In Wikipedia's voice since 26 September 2025. 10 edits tried to restore the attribution ("allegedly", "described by most scholars as"); each one disappeared within 45 minutes."
  - Mark aria/tooltip: "Attempt [n] to restore the attribution, [date]" / "Attempt to restore the attribution · [date]"
- Slide 2 "Hamas": "Hamas · the first sentence · 2021 ← today" · lanes: ""armed" (militant) in the definition" · ""political organisation possessing a (military) wing"" · ""terrorist" added: a dot for every day on which it entered"
  - Caption: "The word "terrorist" entered five times; the longest stay lasted about 2.4 hours. The words "resistance movement" entered once, on 1 August 2024, and disappeared the next day."
  - Mark: ""terrorist" (terrorist) entered, [date]"
- Slide 3 "Zionism": "Zionism · the first sentence · 2021 ← today" · lanes ""colonial" or "colonization"" · ""re-establishment" (re-establishment)" · ""colonial" removed, November 2024 to August 2026"
  - Caption: "The word "colonial" was removed and returned 10 times from November 2024 to August 2026; every removal was reverted within a day."
  - Mark: ""colonial" (colonial) removed · [date]"
- Body: "These are four first sentences (7 October in card 3), not the whole topic. Across all 254 core articles and articles of top and high importance on the topic, reverts of edits that removed critical terms did not come faster than reverts of edits that added them."

### Weekly chart

- Chips: "The whole period" · "7 October 2023" · "The ground war and the pause" · "2024: Rafah and Lebanon" · "May–June 2025" · "2025–2026: the definitions stabilise"
- Chart title: "New critical terms per week, 2021–2026"; legend "New terms" · "Held a week" · "Battle" · "Ceasefire"
- Figure aria: "When: new critical terms per week, after every battle"; chart aria: "New critical terms per week in the opening paragraphs of 4,642 topic articles, 2021 to 2026, with a marking of 7 October 2023, and other battles and ceasefires as markings on the timeline"; "Weekly chart; hover or tap on a week"
- Tooltip: "The week beginning on [date]" · "New critical terms" · "Still there a week later"; event e.g. "The Gaza ceasefire and the hostage deal come into force (agreed on 15 January)"
- Period views: "[period] · by week"; events e.g. "7 Oct · the 7 October attack", "9 Oct · Hamas: "political" added", "12 Oct · Hamas: "armed" ← "military"", "27 Oct · the ground invasion", "24 Nov · pause", "27 Nov · 7 Oct: "attacks" ← "incursions"", "1 Dec · fighting resumes", "9 Dec · 7 Oct: "armed incursions"", "6 May · the Rafah offensive", "6 June · Nakba: "it is the ethnic cleansing"", "27 Sept · Nasrallah killed", "1 Oct · the invasion of Lebanon", "16 Oct · Hezbollah: "paramilitary"", "16 May · the offensive in Gaza", "26 May · Gaza war: Hamas left sentence 1", "13 June · the war with Iran", "22 June · Zionism: "Jewish homeland"", "26 Sept · Gaza genocide: today", "10 Oct · the ceasefire", "29 Nov · Hamas: today", "28 Feb · the war with Iran", "6 July · Nakba: "at the hands of Zionists"", "27 Aug · Zionism: today", "8 Oct · 7 Oct: today"; legend "Wording change"
  - Period stat: "Three weeks from the attack (7 October 2023): [13.7] new terms per week, compared with 3.8 in the six weeks that preceded; 17 of them in total held a week." Other periods: ground invasion "8.7 … compared with 8.3 … (no clear rise); 14 of them…"; Rafah "7.3 … compared with 4.7 …; 13 …"; Gaza offensive May 2025 "2.0 … compared with 2.2 … (less); 4 …"; ceasefire Oct 2025 "3.0 … compared with 2.7 … (no clear rise); 7 …"
- Body: "In the three weeks after 7 October, 13.7 new critical terms were added per week, compared with 3.8 in the six weeks before. The timing gives a date, not a cause."
- Bridge: "Wikipedia's arbitrators ruled on questions of conduct in this topic."

## Card 7: From Wikipedia's arbitrators

- Eyebrow: "7 From the mouth of Wikipedia's arbitrators" · "All the evidence ←"
- H2: "Wikipedia's arbitrators determined that outside actors "are investing heavily in trying to influence" its coverage of this topic. They named no side and no country."
- Source: "Wikipedia's Arbitration Committee · PIA5 · finding 10 · passed by a majority of 15 to 0 · 23 January 2025"
  - "Our translation: "Outside actors are investing heavily in trying to influence Wikipedia's coverage of the topic area""
- "The committee also recorded that the account Ïvana was banned "for improper conduct outside Wikipedia related to the PIA area" (finding 16, 9 December 2024)."
- Bar labels: "0%" · "about half by chance" · "89%–100%"; figure aria: "Four groups of 3 to 6 accounts voted together in 89% to 100% of cases; chance gives about half."
- Body: "Our count: in 217 formal discussions on talk pages, four groups of 3 to 6 accounts voted together in 89% to 100% of cases, compared with about half by chance."
- Body: "This is voting in camps, not proof of coordination; we did not code which side each group leaned towards, and we did not link any of the findings to the edits above."
- Bridge: "And finally: how many people read these pages, and the overall count."

## Close: Reach and count

- Heading: "Reach and count"
- "The most-read pages in whose lead critical language was added"
- "Views, in the last 12 months:" · "Benjamin Netanyahu 7.0 million · Israel 4.6 million · Palestine 2.4 million · Zionism 1.8 million · Hamas 1.3 million"
- "The count. For every critical term taken out of these opening paragraphs, almost four went in."
- "These opening paragraphs · critical terms: 223 went in · 61 went out" · "Comparison pages (other countries, conflicts and religions): 125 went in · 73 went out"
- "A few lines moved in the opposite direction"
  - "The expulsion and flight of the Palestinians in 1948. The phrase "by Zionist militias" left the first sentence on 30 May 2025; the next sentence names "the Zionist paramilitary organisations Haganah, Etzel and Lehi"."
  - "October 7 attacks. On 1 October 2026 the second sentence called Israel's response "actions that scholars have reached the conclusion constitute genocide"; by 2 November the clause disappeared. The removal is fresh, and may be reverted."
- "The change is concentrated in the core articles that people read, while the long tail of short pages hardly changed."
- "In brief": "Before the war, none of the most-read article leads on Wikipedia on the topic accused Israel of genocide; today the article on Israel says, in Wikipedia's voice, that Israel "began to commit genocide", Zionism is "a Jewish homeland by means of colonization", and in every copy we hold, the leads of the articles on Israel and on Hamas do not mention the hostages."
- Links: "To the full research edition (in English) ←" · "Every quote, with a date ←"
- Colophon: "The short edition · published on 9 November 2026 · Wikipedia wording correct as of 5 November 2026 · every quote exact, dated and in the source language, and beside it our translation; the evidence, the method and the limitations in the research edition (in English)."

## Sheets (dialogs from the play buttons)

- Titles: "Zionism: every change to the first sentence" · "Hamas, 7 October, Gaza genocide: every change" · "In their own words: the sentence, then and now"
- Shared note: "This is the full tool of the research edition, in its source language (English): every version, every date and every quote as they were saved."
- Close: "Close ✕"; footer link: "Opening in the research edition ↖"
- The tool content is in English `[UI-EN]`, including the Hebrew tool's own explanation: "The native Hebrew word, used for the Holocaust; maximal moral weight. The loanword … is not used." Mixed labels: "Genocide: not in the lead → stated as fact"; "… in this sentence: no loaded term → stated as fact"; "Genocide: not in the lead → attributed to others"; "ORIGINAL · Hebrew"; heading "The Gaza Strip arena in the Swords of Iron war".

## Share images (downloaded PNGs and `shSpec()`)

- `wikipedia-first-lines-he.png`: kicker "English Wikipedia · the opening lines, then and now · the lines in Hebrew: our translation". Title "Open these articles today. Their opening lines, then and now." The six rows are as in the hero. Foot: "Israel denied that its actions constitute genocide." + EN quote + the scope disclaimer + "Wikipedia wording correct as of 5 November 2026 · The short edition, Framing drift on Wikipedia · [URL]".
- `wikipedia-october-7-he.png`: kicker "English Wikipedia · 7 October and the hostages". Title = card 3 H2. Rows: "7 October · the first sentence · October 2023 ← today"; "7 October · the article's lead · January 2024 ← today"; "The hostages". Foot: "The lead still says "while massacring civilians in 21 communities", and the first sentence names Hamas, further on in it." + disclaimer + stamp.
- `wikipedia-hamas-english-hebrew-he.png`: kicker "Wikipedia · Hamas, in English and in Hebrew · the lines in Hebrew: our translation". Title = card 4 H2. Rows: "English Wikipedia · Hamas · the first sentence · since 29 November 2025"; "Hebrew Wikipedia · today (October 2026) · preliminary". Foot: card 4 body + context + disclaimer + stamp.
- `wikipedia-two-voices-he.png`: kicker "English Wikipedia · the genocide accusation, in two voices". Title = card 5 H2. Rows: "In Wikipedia's voice · Gaza genocide · the first sentence · since 26 September 2025"; "Attributed to others · 7 October attacks · the article's lead · today". Foot: "The article "Gaza genocide" brings Israel's denial in the last paragraph of its lead." + "The article on 7 October describes the killing in Wikipedia's voice: …" + disclaimer + stamp.
- Save feedback: "Saved ✓" / "Not saved".

---

# Step 2: comparison with the English page

Compared against `scratchpad/flash/impact2e/index.html`, rendered the same way (iPhone 13, details opened, chips toggled, `shSpec()` read), and against the original quotes as the English page shows them. The numbers and dates match in every aligned string: 150, 7 and 2, 41 and 37, 15, 107, 251, 21, 1,195, 5 to 22 of 20 and 23, 16% and 96%, 10 attempts and 45 minutes, 2.4 hours, 254, 13.7 and 3.8, all five period stats, 217, 3 to 6, 89–100%, 15–0, the views, 223/61 and 125/73, and every title-delay day count. I found **no number or date divergence**. Most divergences are in word choice (strength), in the scope of article names, and in untranslated or omitted chrome.

Severity: 3 = changes what a reader would take the page to claim. 2 = a noticeable shift in strength, attribution or meaning, or an omission a reader would miss. 1 = a nuance, a register difference or a localisation gap.

| # | Location | English original | Back-translation | Divergence type | Sev | Suggested Hebrew fix |
|---|---|---|---|---|---|---|
| 1 | Card 5, own-voice quote, our translation (also c5vs share image) | “…the ongoing, intentional, and systematic **destruction** of the Palestinian people…” | "…the ongoing, deliberate and systematic **annihilation/extermination** (השמדה) of the Palestinian people…" | Strength (sharper). השמדה is extermination vocabulary (השמדת עם, מחנות השמדה). The page renders the same word as הרס in the Nakba and Arabic slides. | 2 | ״…ההרס המתמשך, המכוון והשיטתי של העם הפלסטיני…״ |
| 2 | Card 7 H2 and the finding-10 translation | found outside actors “heavily invested in influencing” its coverage | determined that outside actors "are investing heavily in trying to influence" its coverage | Meaning and strength. The idiom "invested in" means having a strong stake. The Hebrew literalises it as spending resources on influence campaigns, and "found" becomes "determined". | 2 | ״יש להם עניין רב בהשפעה על הסיקור״ / ״מעורבים מאוד בניסיונות להשפיע״; קבעו → מצאו |
| 3 | Share image `wikipedia-first-lines-he.png`, foot | "In the Israel article, the next sentence: “Israel has denied…”" | (lead-in dropped) "Israel denied that its actions constitute genocide." + EN quote | Omission and attribution. Without the lead-in, the denial sits directly under the Gaza genocide row and loses its source article. The on-page hero keeps the lead-in. | 2 | Restore the first foot line: ״בערך על ישראל, המשפט הבא: ״ישראל הכחישה…״״ |
| 4 | Matrix, ring legend and about 15 cell aria-labels and tooltips | "changed, **not a change of voice**" | "changed, **but not in voice**" (השתנה, אך לא בקול) | Meaning (ambiguous). It reads as "not in Wikipedia's voice", which contradicts cells such as "today stated as fact, changed, but not in voice" (EN Zionism, IT Zionism, NL 7 Oct). | 2 | ״השתנה, בלי שינוי בקול״ |
| 5 | Hero row 5, card 4 H2, c4vs share, card 6 Hamas lane, chip 12 Oct | Hamas “militant” | "חמוש" = "armed", and in the H2 "Wikipedia **defined** Hamas as an '**armed**' organisation" | Strength and meaning. "Militant" is softened to plain "armed", and "called … 'militant'" becomes "defined … as an armed organisation" (stronger verb, and "organisation" added inside the quote). | 2 | Keep חמוש but add a gloss where it is first quoted: ״חמוש״ (militant). H2: ״ב־2021 ויקיפדיה כינתה את חמאס ״חמוש״…״ |
| 6 | Carousel 1, slide 2 (Arabic) | English shows the full sentence morphing from then to now, including “…which Israel is carrying out…” | Hebrew "our translation" gives only the THEN sentence ("Israel was accused…"). The now-sentence and its agent "carried out by Israel" are not translated. | Omission, including agency | 2 | Add the now-sentence: ״…שישראל מבצעת במהלך מלחמת עזה״ (or mirror the morph) |
| 7 | Card 5 H2 and the attributed quote (c5vs share) | “Some **have alleged**” | "some **have claimed/argued**" (יש שטענו) | Strength (softer). "Alleged" carries an accusation; טענו is neutral. This weakens the contrast the card draws. | 1 | ״יש שהאשימו״ / ״יש שטענו בהאשמה״ (or keep it and gloss "alleged") |
| 8 | Card 5 carousel close, c5vs share foot | “at least 1,195 people were killed **by** the attacks” | "were killed **in** the attacks" (במתקפות) | Agency (weakened) | 1 | ״לפחות 1,195 בני אדם נהרגו כתוצאה מהמתקפות״ / ״המתקפות הרגו לפחות 1,195 בני אדם״ |
| 9 | Hero row 4, card 3 labels, c3 share labels | "OCTOBER 7 **ATTACKS** · FIRST SENTENCE" / "…· OPENING SECTION" | "7 October · the first sentence" | Scope (the article name is shortened to the date) | 1 | ״מתקפות 7 באוקטובר · המשפט הראשון״ (as card 5 already does) |
| 10 | Masthead, colophon, share-image stamp | "Flash edition" | "The **abridged** edition" (המהדורה המקוצרת) | Scope. It presents the page as a shortened copy of the study, not a stand-alone flash piece. | 1 | ״מהדורת הבזק״ or keep it with a note |
| 11 | `<title>` | "Flash: how English Wikipedia now tells Israel's story" | "In brief: …" | Meaning (label) | 1 | ״מבזק: …״ |
| 12 | Scope disclaimer (hero and every share image) | "not whether **it is true**" | "and not whether **the wording is correct**" | Meaning (truth of claims vs correctness of wording) | 1 | ״ולא אם הוא אמת״ / ״ולא אם הנוסח משקף את האמת״ |
| 13 | Card 4 and matrix chips | "Exploratory" | "**Preliminary**" (ראשוני) | Meaning. Preliminary implies confirmation is coming; exploratory implies a non-rigorous probe. | 1 | ״גישוש״ / ״בדיקה גישושית״ |
| 14 | Card 4 context (and c4vs share) | "in line with Wikipedia-wide **style** on contentious labels" | "in line with Wikipedia's site-wide **style rule**" | Strength (a guideline becomes a rule) | 1 | ״בהתאם להנחיית הסגנון של ויקיפדיה…״ |
| 15 | Matrix table caption | "How each language edition **voices** five claims" | "…**phrases** 5 claims" | Meaning. It drops the analytic term "voice". | 1 | ״באיזה קול מנסחת כל מהדורת שפה 5 טענות״ |
| 16 | Card 7 caveat | "we did not code which side each group **took**" | "…which side each group **leaned towards**" | Strength (softer) | 1 | ״לאיזה צד צידדה כל קבוצה״ |
| 17 | Card 2 full-sentence translations | "permanent **displacement**" / "violent **displacement**" | "permanent **uprooting**" (עקירה) | Strength (slightly sharper) | 1 | ״ההגליה/ההעתקה הקבועה״ — or keep עקירה, which is the standard term |
| 18 | Carousel 1, slide 3, arrow line (Spanish) | "a retaliatory attack … that has unleashed a genocide in Gaza by Israel" | "a retaliatory attack … **that (m.) brought about** genocide in Gaza on Israel's part" (מתקפת תגמול … שחולל) | Agency. The masculine verb does not agree with מתקפה, so the subject is unclear. "Unleashed" becomes "caused". | 1 | ״עימות … שהחל במתקפת תגמול … ו״שחולל רצח עם בעזה מצד ישראל״״ |
| 19 | Carousel 1, slide 2, arrow line (Arabic) | "→ “The genocide of Gaza is the systematic, deliberate and ongoing destruction”" | "…is the destruction **and the harming**, systematic, deliberate and ongoing" | Addition ("targeting", from the Arabic, rendered softly as "harming") | 1 | ״ההרס והסימון כמטרה״, or drop it to match EN |
| 20 | Matrix "Our coding" details (#xmNote) | Our coding. Genocide, colonization… (EN) | Left in English | Omission (untranslated) | 1 | Translate the note |
| 21 | Matrix cell tooltips, all non-Hebrew languages (about 30 cells) | "Our translation: …" (EN) | "Our translation **into English**:" followed by English text, with no Hebrew rendering | Omission (localisation gap: a Hebrew reader gets the foreign quotes only in English) | 1 | Add Hebrew translations, or label clearly that they are in English only |
| 22 | Nakba and 7 Oct mark tooltips | "added" / "removed" | Left in English (`added`, `removed`) inside the Hebrew tooltip | Omission (untranslated chrome) | 1 | ״נוסף״ / ״הוסר״ |
| 23 | Play sheets (zi, o7, xr) | Full EN tool | Hebrew title and note, English body. Note added: "This is the full tool … in its source language (English)" | Addition (accurate disclosure); body untranslated | 1 | Acceptable as is. The xr Hebrew-cell gloss ("The native Hebrew word, used for the Holocaust…") could be translated |
| 24 | Colophon | "every quote is exact and dated; the evidence, method and limits are in the research edition." | adds "in the source language, and beside it our translation", and "(in English)" | Addition (accurate) | 1 | None needed |
| 25 | Card 5 H2 | "Wikipedia **says** genocide in Gaza is…" | "Wikipedia **writes** that the genocide in Gaza…" | Attribution nuance (the definite article "the genocide" in the reported clause) | 1 | None needed. Optionally ״ויקיפדיה כותבת שרצח עם בעזה…״ |
| 26 | Card 6 eyebrow | "HOW IT GOT THERE" | "How it happened" | Scope (the process of the lines reaching their state becomes events in general) | 1 | ״איך זה הגיע לשם״ |
| 27 | Card 6 body and period stats | "13.7 new critical terms a week" (verbless) | "13.7 new critical terms **were added** per week" | Addition (explicit verb; neutral) | 1 | None needed |
| 28 | Matrix English cells tooltip | "the story above quotes the 5 November 2026 text" | "the **cards** above quote…" | Scope (minor) | 1 | None needed |

## Counts

- Severity 3: **0**
- Severity 2: **6** (#1–#6)
- Severity 1: **22** (#7–#28)
- Total: **28**. Numbers and dates: 0 divergences.

Agency, strength and attribution notes: the Hebrew keeps every own-voice / attributed distinction the English draws ("בקולה של ויקיפדיה" vs "מיוחס לאחרים"). It keeps the attribution of the scope disclaimer and the arbitration quotes, and every count and date. The only places where it moves strength in a consistent direction are #1 and #2, both sharper, and #7, which is softer.
