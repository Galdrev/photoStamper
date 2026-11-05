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

## Amendment 1 (2026-11-05, before any study-2 result was seen): coherence, cleaning, standard models

**C1 Coherence: do the two narratives move together?**
- For each article, compute the change (2021-01 → latest) on every measure that is defined at both ends: N1, N2, N4 share, N5, N6, N7, plus study 1's critical-rate change.
- Report the pairwise Spearman correlations (topic and comparison separately) and a PCA on the standardised change matrix.
- **H2-coherence:** in topic articles, the measures load on one shared component, oriented so that the J-share falls and the P-share rises. That component explains more variance than in the comparison articles.
- Repeat on the mass tier's opening paragraphs.

**C2 Cleaning: relevance fixed in advance, outcome-blind.** Two standard filters, applied before outcomes are looked at:
- (a) **Wikidata type** (P31 "instance of", via the public Wikidata API). Keep events, conflicts, wars, massacres, ethnic/religious/national groups, ideologies, movements, organisations, states, territories, historical periods and regions, religious sites and cities. Drop humans, sports teams, companies, films, books, songs, buildings with no religious or historic designation, species and disambiguation pages.
- (b) **Baseline relevance:** the 2021-01 snapshot mentions both topic groups (J and P terms), or at least 2 land/conflict terms per 1,000 words.
- Every result is reported **unfiltered and filtered**, side by side. The filter is never chosen or altered after seeing results.

**C3 Standard model.** Article-level change on each primary outcome (study 1: critical rate in lead and full text; study 2: N1–N7):
- Model: OLS `change ~ group + log(words_2021) + log(1+edits) + log(1+views) + created_in_window`, plus importance and project fixed effects where available (mass tier).
- Standard errors clustered by subgroup or WikiProject (statsmodels).
- Report the group coefficient with its 95% CI, unfiltered and filtered.

**C4 Mass-tier narrative.** The opening paragraph of every mass-frame article at 2021-01 and now (API section 0). N1, N2, N4, N5, N6 and N7 computed per article; the C1–C3 analyses repeated at this scale.
