"""Article corpus: treatment group (Judaism / Israel / Zionism) and control group.

The control group matters: after 7 Oct 2023 the whole encyclopedia covering
conflicts, nationalisms and religions changed. A shift is only meaningful if
it is larger in the treatment group than in comparable articles.
"""

# Hand-picked core articles (always included).
TREATMENT_SEED = {
    "zionism": [
        "Zionism", "History of Zionism", "Theodor Herzl", "Balfour Declaration",
        "Religious Zionism", "Labor Zionism", "Revisionist Zionism",
        "Christian Zionism", "Anti-Zionism", "Post-Zionism", "Cultural Zionism",
        "World Zionist Organization", "Jewish National Fund", "Aliyah",
        "First Aliyah", "Second Aliyah", "Zionist Congress", "Ahad Ha'am",
        "Chaim Weizmann", "Ze'ev Jabotinsky", "Uganda Scheme",
        "Zionism as settler colonialism", "Mandatory Palestine",
        "Yishuv", "Haganah", "Irgun", "Lehi (militant group)",
    ],
    "israel": [
        "Israel", "History of Israel", "Israeli Declaration of Independence",
        "David Ben-Gurion", "Golda Meir", "Benjamin Netanyahu",
        "1948 Arab–Israeli War", "Six-Day War", "Yom Kippur War",
        "Israel Defense Forces", "Law of Return", "Jerusalem",
        "Tel Aviv", "Basic Law: Israel as the Nation-State of the Jewish People",
        "Politics of Israel", "Demographics of Israel", "Arab citizens of Israel",
        "Israeli settlement", "West Bank", "Gaza Strip", "Golan Heights",
        "Israeli-occupied territories", "Israeli West Bank barrier",
        "Mossad", "Knesset", "Kibbutz", "Hebrew language", "Modern Hebrew",
        "Israel and apartheid", "Israel and state-sponsored terrorism",
        "Human rights in Israel", "Foreign relations of Israel",
        "Abraham Accords", "Oslo Accords", "Camp David Accords",
    ],
    "conflict": [
        "Israeli–Palestinian conflict", "Arab–Israeli conflict", "Nakba",
        "1948 Palestinian expulsion and flight", "Deir Yassin massacre",
        "First Intifada", "Second Intifada", "Hamas", "Hezbollah",
        "Palestine Liberation Organization", "October 7 attacks",
        "Gaza war", "Gaza genocide", "Blockade of the Gaza Strip",
        "Palestinian right of return", "Two-state solution",
        "One-state solution", "From the river to the sea",
        "Boycott, Divestment and Sanctions", "Palestinian refugees",
        "Jewish exodus from the Muslim world", "Farhud",
        "Hebron massacre", "1929 Palestine riots", "Munich massacre",
        "Entebbe raid", "Sabra and Shatila massacre",
    ],
    "judaism": [
        "Judaism", "Jews", "Jewish history", "Israelites", "Hebrews",
        "Land of Israel", "Jewish diaspora", "Ashkenazi Jews", "Sephardic Jews",
        "Mizrahi Jews", "Beta Israel", "Jewish identity", "Who is a Jew?",
        "Halakha", "Talmud", "Torah", "Temple Mount", "Western Wall",
        "Second Temple", "Siege of Jerusalem (70 CE)", "Bar Kokhba revolt",
        "Rabbinic Judaism", "Orthodox Judaism", "Reform Judaism",
        "Hasidic Judaism", "Haredi Judaism", "Jewish Autonomous Oblast",
        "Genetic studies of Jews", "Khazar hypothesis of Ashkenazi ancestry",
        "Jewish population by country", "Jewish peoplehood",
    ],
    "narrative": [
        "Palestinians", "History of Palestine", "Palestinian nationalism", "Palestinian identity", "Palestine (region)",
        "State of Palestine", "Palestinian refugees", "Palestinian refugee camps", "UNRWA", "Palestinian right of return",
        "1948 Arab–Israeli War", "Deir Yassin massacre", "Lydda and Ramle expulsions", "Plan Dalet", "Tantura massacre",
        "Jewish exodus from the Muslim world", "Jewish exodus from Arab and Muslim countries", "Farhud", "Mizrahi Jews",
        "Canaan", "Canaanites", "Philistines", "Ancient Israel and Judah", "Kingdom of Israel (Samaria)", "Kingdom of Judah",
        "Judea", "Samaria", "Judea and Samaria Area", "Hasmonean dynasty", "Herodian kingdom", "Judaea (Roman province)",
        "Syria Palaestina", "Jewish–Roman wars", "Bar Kokhba revolt", "Jewish diaspora", "Old Yishuv", "Palestinian Jews",
        "Temple Mount", "Al-Aqsa", "Al-Aqsa Mosque", "Dome of the Rock", "Western Wall", "Cave of the Patriarchs",
        "Hebron", "Rachel's Tomb", "City of David", "Shiloh (biblical city)", "Jericho", "Nablus", "Joseph's Tomb",
        "Bethlehem", "East Jerusalem", "Old City of Jerusalem", "Silwan", "Sheikh Jarrah", "Masada",
        "Genetic studies of Jews", "Genetic history of the Middle East", "Origin of the Palestinians", "Israeli Arabs",
    ],
    "antisemitism": [
        "Antisemitism", "History of antisemitism", "New antisemitism",
        "Antisemitism in the 21st century", "Holocaust", "The Holocaust",
        "Holocaust denial", "Pogrom", "Kishinev pogrom", "Kristallnacht",
        "Blood libel", "The Protocols of the Elders of Zion",
        "Antisemitic canard", "Zionist Occupation Government conspiracy theory",
        "Working Definition of Antisemitism", "Jerusalem Declaration on Antisemitism",
        "Antisemitism and the New Testament", "Islamic views on Jews",
        "Antisemitism in Europe", "Antisemitism in the United States",
        "Anti-Zionism and antisemitism", "Weaponization of antisemitism",
        "Antisemitic anti-Zionism", "Nakba denial", "Israeli apartheid",
        "Occupied Palestinian territories", "List of genocides",
        "Genocide of indigenous peoples", "Sexual and gender-based violence in the October 7 attacks",
        "Al-Ahli Arab Hospital explosion", "Wikipedia and the Israeli–Palestinian conflict",
        "Dreyfus affair", "Anti-Defamation League", "Jewish Voice for Peace",
    ],
}

# Comparable articles about other nations / national movements / religions /
# contested territories. Chosen to share structure (nationalism, state founding,
# religion, diaspora, territorial dispute) but not the Israel topic area.
CONTROL_SEED = {
    "nationalism": [
        "Irish nationalism", "Kurdish nationalism", "Armenian nationalism",
        "Hindu nationalism", "Arab nationalism", "Pan-Africanism",
        "Basque nationalism", "Catalan independence movement",
        "Ukrainian nationalism", "Polish nationalism", "Greek nationalism",
        "Turkish nationalism", "Palestinian nationalism", "Taiwanese nationalism",
        "Scottish independence", "Quebec sovereignty movement",
    ],
    "states": [
        "India", "Pakistan", "Partition of India", "Turkey", "Armenia",
        "Ireland", "Ukraine", "Taiwan", "Poland", "Greece", "Egypt", "Jordan",
        "Saudi Arabia", "Iran", "Lebanon", "Syria", "Cyprus", "Kosovo",
        "History of India", "History of Pakistan", "History of Turkey",
        "Republic of Ireland", "Northern Ireland", "The Troubles",
    ],
    "conflicts": [
        "Kashmir conflict", "Cyprus problem", "Nagorno-Karabakh conflict",
        "Russo-Ukrainian War", "Kurdish–Turkish conflict (1978–present)",
        "Western Sahara conflict", "Tibet", "Annexation of Tibet by the People's Republic of China",
        "Turkish invasion of Cyprus", "Population exchange between Greece and Turkey",
        "Armenian genocide", "Bangladesh Liberation War", "Rwandan genocide",
        "Bosnian genocide", "Uyghur genocide", "Darfur genocide",
        "Rohingya genocide", "Sudanese civil war (2023–present)", "Tigray war",
    ],
    "settler_colonial_framings": [
        "History of Australia", "Aboriginal Australians", "French Algeria",
        "Algerian War", "Indigenous peoples in Canada", "Native Americans in the United States",
        "History of South Africa", "Apartheid", "Māori people", "Rhodesia",
    ],
    "armed_groups": [
        "Provisional Irish Republican Army", "Kurdistan Workers' Party", "Islamic State", "Al-Qaeda",
        "Taliban", "ETA (separatist group)", "Liberation Tigers of Tamil Eelam", "Boko Haram", "Al-Shabaab (militant group)",
        "Revolutionary Armed Forces of Colombia", "Ulster Volunteer Force", "Wagner Group",
    ],
    "two_narrative_disputes": [
        "Kosovo", "History of Kosovo", "Kosovo War", "Kosovo Serbs", "Albanians in Kosovo", "Serbian Orthodox Church in Kosovo",
        "Nagorno-Karabakh", "Republic of Artsakh", "First Nagorno-Karabakh War", "2023 Azerbaijani offensive in Nagorno-Karabakh", "Shusha",
        "History of Cyprus", "Turkish invasion of Cyprus", "Northern Cyprus", "Greek Cypriots", "Turkish Cypriots",
        "History of Kashmir", "Kashmiri Pandits", "Exodus of Kashmiri Hindus", "Kashmiri Muslims", "Insurgency in Jammu and Kashmir",
        "Partition of Ireland", "Bloody Sunday (1972)", "Ulster loyalism", "Irish republicanism", "Plantation of Ulster",
    ],
    "religion": [
        "Christianity", "Catholic Church", "Islam", "Hinduism", "Sikhism",
        "Buddhism", "Eastern Orthodox Church", "Druze", "Zoroastrianism",
        "Armenian Apostolic Church", "Coptic Orthodox Church", "Sunni Islam",
        "Shia Islam", "Protestantism", "Anti-Catholicism", "Islamophobia",
        "Hinduphobia", "Anti-Armenian sentiment", "Romani people",
        "Armenian diaspora", "Indian diaspora", "Greek diaspora",
    ],
}

# Categories crawled to widen the treatment group (depth-limited).
TREATMENT_CATEGORIES = [
    "Category:Zionism",
    "Category:Antisemitism",
    "Category:Israeli–Palestinian conflict",
    "Category:History of Israel",
    "Category:Jewish history",
    "Category:Jewish ethnic groups",
]

# Window of study.
START = "2021-01-01T00:00:00Z"
SNAPSHOT_DATES = [f"{y}-{m:02d}-01T00:00:00Z" for y in range(2021, 2027)
                  for m in (1, 4, 7, 10)]


# Comparison articles directly hit by the 2023– Israel/Gaza/Lebanon/Iran war or
# entangled with the topic: excluded from the primary comparison group.
CONTROL_CONTAMINATED = {
    "Palestinian nationalism", "Arab nationalism", "Jordan", "Lebanon", "Syria",
    "Egypt", "Iran", "Saudi Arabia", "Druze", "Islamophobia",
}
# Comparison articles with their own large 2021–2026 shock. Kept, reported as a
# subgroup: they test H0 ("framing just follows real-world events").
CONTROL_SHOCKED = {
    "Russo-Ukrainian War", "Ukraine", "Ukrainian nationalism", "Nagorno-Karabakh conflict",
    "Darfur genocide", "Sudanese civil war (2023–present)", "Tigray war", "Uyghur genocide",
    "Rohingya genocide", "Armenia",
}

# Known, dated changes documented by press coverage (see research notes).
# The pipeline should find pattern absent at `before` and present at `after`.
# A miss means either the pipeline or the press claim is wrong; both are reported.
VALIDATION = [
    {"title": "Zionism", "pattern": r"coloni[sz]", "before": "2024-07", "after": "2024-10", "part": "lead",
     "claim": "Lead reworded to describe Zionism as pursuing a state through colonization (Jul–Oct 2024)"},
    {"title": "Zionism", "pattern": r"coloni[sz]", "before": "2024-04", "after": "2024-07", "part": "lead", "post_hoc": True,
     "claim": "POST-HOC (added after the sample showed the press timing was off): wording entered the lead between Apr and Jul 2024"},
    {"title": "Israel", "pattern": r"(?:began|is|has been) committing genocide|committed genocide", "before": "2025-10", "after": "2026-01",
     "part": "lead", "claim": "Lead changed from 'accusations of genocide' to stating genocide (Dec 2025)"},
    {"title": "List of genocides", "pattern": r"\bgaza\b", "before": "2024-07", "after": "2025-01", "part": "full",
     "claim": "Gaza entry added after RfC (reported Nov 2024)"},
    {"title": "Gaza genocide", "pattern": r"^(?!.*\ballegations?\b).*", "before": "2024-04", "after": "2024-10", "part": "lead",
     "claim": "Article retitled from 'Allegations of genocide…' (Jul 2024); lead should drop 'allegations' framing"},
    {"title": "Occupied Palestinian territories", "pattern": r"^.{0,120}occupied palestinian territor", "before": "2024-04", "after": "2024-10",
     "part": "lead", "claim": "Renamed from 'Palestinian territories' (mid-2024)"},
]

ARMED_GROUPS_TOPIC = ["Hamas", "Hezbollah", "Palestinian Islamic Jihad", "Popular Front for the Liberation of Palestine",
                      "Al-Qassam Brigades", "Irgun", "Lehi (militant group)", "Kach (party)", "Haganah"]
ARMED_GROUPS_CONTROL = ["Provisional Irish Republican Army", "Kurdistan Workers' Party", "Islamic State", "Al-Qaeda",
                        "Taliban", "ETA (separatist group)", "Liberation Tigers of Tamil Eelam", "Boko Haram",
                        "Al-Shabaab (militant group)", "Revolutionary Armed Forces of Colombia", "Ulster Volunteer Force",
                        "Wagner Group"]

# Articles whose first-sentence changes are traced to the exact revision (bisect.py).
KEY_ARTICLES = ["Zionism", "Israel", "Hamas", "October 7 attacks", "Gaza genocide", "Gaza war", "Israeli apartheid",
                "Nakba", "Antisemitism", "Anti-Zionism", "Jews", "Judaism", "History of Israel",
                "Israeli–Palestinian conflict", "Jerusalem", "West Bank", "Israeli settlement", "Balfour Declaration",
                "Theodor Herzl", "Mandatory Palestine", "Hezbollah", "Israel Defense Forces", "Land of Israel",
                "1948 Palestinian expulsion and flight", "Zionism as settler colonialism"]
KEY_ARTICLES_CONTROL = ["Kurdish nationalism", "Hindu nationalism", "Armenian genocide", "Russo-Ukrainian War", "Islamic State",
                        "Catholic Church", "India", "Taiwan", "Kashmir conflict", "Uyghur genocide", "Irish nationalism",
                        "Islam", "Turkey", "Ukraine", "Tibet"]

# Study 2 (SPEC_NARRATIVE.md): comparison disputes with two rival narratives over one land; group A vs group B terms.
NARRATIVE_DISPUTES = {
    "Kosovo": {"A": r"\b(?:serbs?|serbian)\b", "B": r"\b(?:albanians?|kosovars?|kosovo albanians?)\b", "A_label": "Serbs", "B_label": "Albanians",
               "articles": ["Kosovo", "History of Kosovo", "Kosovo War", "Kosovo Serbs", "Albanians in Kosovo", "Serbian Orthodox Church in Kosovo"]},
    "Karabakh": {"A": r"\b(?:armenians?)\b", "B": r"\b(?:azerbaijanis?|azeris?)\b", "A_label": "Armenians", "B_label": "Azerbaijanis",
                 "articles": ["Nagorno-Karabakh", "Republic of Artsakh", "First Nagorno-Karabakh War", "2023 Azerbaijani offensive in Nagorno-Karabakh",
                              "Shusha", "Nagorno-Karabakh conflict"]},
    "Cyprus": {"A": r"\b(?:greek cypriots?|greeks?)\b", "B": r"\b(?:turkish cypriots?|turks?|turkish)\b", "A_label": "Greek Cypriots", "B_label": "Turkish Cypriots",
               "articles": ["History of Cyprus", "Turkish invasion of Cyprus", "Northern Cyprus", "Greek Cypriots", "Turkish Cypriots", "Cyprus problem"]},
    "Kashmir": {"A": r"\b(?:kashmiri (?:hindus|pandits)|pandits?|hindus?)\b", "B": r"\b(?:kashmiri muslims|muslims?)\b", "A_label": "Kashmiri Hindus", "B_label": "Kashmiri Muslims",
                "articles": ["History of Kashmir", "Kashmiri Pandits", "Exodus of Kashmiri Hindus", "Kashmiri Muslims", "Insurgency in Jammu and Kashmir", "Kashmir conflict"]},
    "Northern Ireland": {"A": r"\b(?:unionists?|loyalists?|protestants?)\b", "B": r"\b(?:nationalists?|republicans?|catholics?)\b", "A_label": "Unionists", "B_label": "Nationalists",
                         "articles": ["Partition of Ireland", "Bloody Sunday (1972)", "Ulster loyalism", "Irish republicanism", "Plantation of Ulster",
                                      "Northern Ireland", "The Troubles"]},
}
SHARED_SITES = ["Jerusalem", "Hebron", "Temple Mount", "Cave of the Patriarchs", "Western Wall", "Rachel's Tomb", "City of David",
                "Shiloh (biblical city)", "Jericho", "Nablus", "Joseph's Tomb", "Bethlehem", "Old City of Jerusalem", "Al-Aqsa", "Dome of the Rock"]
