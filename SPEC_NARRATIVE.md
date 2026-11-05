# Study 2: competing narratives. Pre-registered spec (written 2026-11-05, before any of these measures was computed)

Study 1 measured one direction: critical vocabulary. This study measures **two narratives against each other** over the same land:
- a Jewish/Israeli narrative: indigeneity, historical continuity, ancient names of the land, Jewish displacement;
- a Palestinian narrative: indigeneity, continuity, Palestine naming, the Nakba and refugees.

The question is whether English Wikipedia's *baseline story* shifted between 2021 and 2026, and in which direction, compared with other two-narrative land disputes measured the same way.

## Unit and method
- **Unit:** a sentence in an article snapshot. A frame is **attributed** to a group when the frame term and a group term occur in the same sentence and no other group's term is closer.
- **Measures:** for each paired frame, the share for group J (Jewish/Israeli) out of J + P (Palestinian/Arab). Also each side's rate per 10k words.
- **Data:** the deep panel (quarterly snapshots, 2021-01 → 2026-10). Plus about 60 new articles on Palestinian history, refugees, and shared land and sites. Plus, for a scale check, the opening paragraphs of mass-tier Israel/Palestine/Judaism/Jewish-history articles at 2021-01 and now.
- **Comparison disputes**, same paired frames with their own group terms:
  - Kosovo (Serbs vs Albanians)
  - Nagorno-Karabakh (Armenians vs Azerbaijanis)
  - Cyprus (Greek vs Turkish Cypriots)
  - Kashmir (Kashmiri Hindus/Pandits vs Kashmiri Muslims)
  - Northern Ireland (unionist vs nationalist)

## Pre-registered measures (each: change from 2021-01 to the latest snapshot, article-level bootstrap CI)
- **N1 Indigeneity share.** Among sentences calling a group indigenous / native / original inhabitants / descendants of the ancient inhabitants: the share attributed to Jews. H2: falls.
- **N2 Ancient-land naming.** In sentences about periods before 135 CE (Bronze/Iron Age, First/Second Temple, Hasmonean, Roman Judaea), the share of land names that are Israel/Judah/Judea/Land of Israel/Canaan, against Palestine/Palestinian. H2: the Palestine share rises.
- **N3 Holy-site naming order.** In articles mentioning both, the share of snapshots where "Temple Mount" appears before "Haram al-Sharif" / "Al-Aqsa compound" / "Noble Sanctuary". H2: falls.
- **N4 Two displacements.**
  - Rate per 10k words of Palestinian displacement terms (Nakba, Palestinian refugees, Palestinian exodus/expulsion) and of Jewish displacement terms (Jewish exodus from Arab/Muslim countries, Jewish refugees, expulsion of Jews from Arab lands, Farhud).
  - The ratio P/(P+J) in the topic articles.
  - H2: the P share rises.
- **N5 Agency of 1948.** Among sentences about 1948 Palestinian departure, the share using passive or forced verbs (expelled, forced out, driven out, ethnically cleansed, depopulated) against flight verbs (fled, left, evacuated, abandoned). H2: the forced share rises.
- **N6 Violence labels by perpetrator.** "Terrorist/terrorism" and "massacre" attributed to Palestinian actors against Israeli actors (sentence attribution). H2: the share for Israeli actors rises.
- **N7 Legitimacy.** "Occupied/occupation" against "disputed" for the West Bank, East Jerusalem and Gaza. "State of Palestine" phrased as "is a country/state" against "claimed/proclaimed/de jure". H2: occupied and country-phrasing rise.
- **N8 Jewish history in shared-site leads.** For Jerusalem, Hebron, the Temple Mount, the Cave of the Patriarchs, the Western Wall, Rachel's Tomb, the City of David, Shiloh, Jericho and Nablus/Shechem: does the opening paragraph mention Jewish/Israelite/Hebrew history? H2: mentions fall.

## Inference and honesty rules
- **Exploratory study** (written after study 1's data was seen, before these measures were). Benjamini–Hochberg correction across N1–N8 at q = 0.10.
- **Comparison disputes:** report each dispute's analogous share change next to the topic's. A topic change counts as "specific" only if it lies outside the range of the comparison disputes.
- **Lexicon validation before interpretation:** a 30-hit KWIC precision check per measure; drop a measure below 60% precision.
- **Attribution validation:** 60 attributed sentences hand-coded by an agent for "is this frame really about this group?"; report the attribution precision.
- **Narrative coding (qualitative):** reuse the masked coder on opening-paragraph changes of the new Palestinian-history and shared-site articles, adding the codes `origins` and `whose_history`.
- **Reporting:** a shift is described as a change in *which narrative the encyclopedia states as baseline*, never as true or false.
