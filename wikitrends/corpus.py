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
