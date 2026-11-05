# Study 2 lexicon + attribution precision (hand-coded by agent)

Source: `wikitrends/data/narrative.json` -> `validation_samples` (topic:N1, N2, N5, N6; 30 each; fields = article, label, sentence[:300]).
Sample counted correct only if (a) the frame is really present and (b) the attribution/label is correct. Gate: <60% is dropped.

| Measure | Correct / total | Precision | Gate (>=60%) |
|---|---|---|---|
| N1 indigeneity | 12/30 | 40% | DROP |
| N2 ancient-land naming | 18/30 | 60% | pass (at threshold, fragile) |
| N5 1948 forced vs flight | 16/30 | 53% | DROP |
| N6 terror/massacre by perpetrator | 16/30 | 53% | DROP |

Not judged: the 23 samples for Kosovo/Kashmir/Karabakh/Cyprus/N. Ireland (N1, comparison disputes).

## N1 (40%)
- Generic "native/indigenous/autochthonous" for non-group things (13 of 18 errors): "his native Georgia" (Stalin article); "native silk"; "native Philadelphia"; "foods native to Palestine"; "Aboriginal Australian"; "indigenous to the Horn of Africa" (Beta Israel genetics).
- Wrong side: the indigenous population is the Palestinians but it is labelled J because a Zionist/Jewish term is nearer: "transfer of the indigenous population" (Ben-Gurion, Pappe); Said's "native inhabitants of Palestine".
- Other: Samaritan "descendants of tribes of Ephraim" labelled J; "native Arab Christians"; "native government" (Palestine Arab Congress).

## N2 (60%)
- Modern Palestinian usage swept in by a BCE date or period word: "Italian-Palestinian Expedition" (Jericho); "Palestinian people descend from Bronze Age inhabitants"; "occupied Palestinian territory" (Old City).
- Post-135 or unrelated period: "613 Jewish revolt ... Palestine in antiquity"; Byzantine "Palestine became a center of Christianity".
- Three samples (Lehi, Doron Mendels, Golan) are cut at 300 chars before any Palestine term; counted wrong as unverifiable. If they were all right N2 would be 21/30 (70%). The result sits on the threshold.
- Note: the label is always "P" by construction (only sentences with a Palestine term are sampled), so (b) tests only "Palestine used as the ancient land name".

## N5 (53%)
- Mixed sentences labelled one way (10 errors in all kinds): "fled or were expelled" (x3), "driven from or left"; ties go to "forced" (f >= l).
- The event's own title matches both classes: "1948 Palestinian expulsion and flight" (Mandatory Palestine, Deir Yassin, UNRWA, Nakba denial); this adds a forced+flight tie in sentences that say nothing about agency. Same for the book title "The Ethnic Cleansing of Palestine".
- Wrong population: Jewish communities "depopulated" in Transjordan; Jewish exodus table (left/fled).
- Truncated or tabular text with no 1948 Palestinian departure visible (Arab-Israeli conflict table).
- If mixed/title cases were accepted, the score would be 26/30; the measure's problem is verb class, not topic.

## N6 (53%)
- Label points at the target or victim, not the perpetrator: "Deir Yassin massacre of Palestinian villagers" and "Tantura massacre ... surviving Palestinians" labelled P; "Israel defended against terrorist acts", "no terrorist will have immunity" (Ya'alon), "terrorists attack Israel" labelled I.
- Non-Palestinian actors in the ACT_P list: Hezbollah designated a terrorist group (x3).
- Not an attribution of the label: Arafat "denounced all forms of terrorism"; PLO "renounced terrorism"; Srebrenica massacre; Sabra and Shatila (Phalangist massacre, Israeli complicity) labelled I.
- Correct examples show the pattern works for named incidents: Lehi/Irgun "terrorist organization"; Deir Yassin; Nova festival massacre by Hamas.

## Notes
Judgments are by one agent reading the (truncated) sentence only; borderline calls (e.g., Karaim, Samaritans, Hezbollah) were made against the measure definition in SPEC_NARRATIVE.md. Not committed.
