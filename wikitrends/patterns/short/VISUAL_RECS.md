# Visual recommendations: summary section (#short) and page header

Scope: CSS and text emphasis only, in `/home/user/photoStamper/wikitrends/page_template.html`. No chart changes. The design system itself (Newsreader / Libre Franklin / mono, paper and ink, teal = topic, grey-violet = comparison) is restrained and stays as it is.

## What reads as loud now

The summary section has very little gold or amber. In light mode the amber (`--del-bd`, `--s1`) shows up only in the hero edit-stream chart (undone edits) and in `.xchip` badges further down, so that is not the main problem. The "tabloid" impression comes from **scale and typographic emphasis stacked at the top of the page**:

- a 68px two-line slogan headline (`.short-h`), its second line in teal italics, followed immediately by
- an 84px hero question (`.hero h1`), its key phrase also in teal italics;
- a 22px lead paragraph that opens with a bold label (`.short-a b`);
- a bolded one-line verdict (`.short-coda`, "Lopsided, not one-sided.");
- an italic pull-quote of the authors' own line (`.short-q`, "We can say the front door changed.").

Two display headlines in a row, coloured emphasis on rhetoric, a bold kicker and a pull-quote: those are the magazine-cover cues.

## Recommendations, in priority order

### 1. Bring the summary headline down to the page's own h2 scale, and remove the teal italic line
```css
.short-h{font-size:clamp(26px,3.4vw,38px);line-height:1.12;letter-spacing:-.012em;max-width:30ch}
.short-h em{font-style:normal;color:inherit;font-weight:inherit}   /* or simply drop the <em> */
```
*Why.* At 68px it competes with the 84px hero title directly below it, so the page opens with two headlines shouting at each other. 38px matches the section h2s (`h2` tops out at 44px), so it reads as the first section rather than a cover line. The new headline is a descriptive sentence and needs room for about 15 words, hence `max-width:30ch` and a looser line-height. Teal means "topic articles" in every chart. Spending it on a headline phrase blurs data encoding with rhetoric (Muth, Datawrapper: keep colour for what you want readers to see in the data).

### 2. Calm the lead paragraph: no bold label, deck size
```css
.short-a{font:400 clamp(17px,1.8vw,19px)/1.55 var(--body);color:var(--ink-2);max-width:66ch}
.short-a b{font-weight:600;color:var(--ink)}
```
Text change: replace `<b>The short answer.</b>` with the label `Summary.` (or leave the label out, since the eyebrow already names the section).
*Why.* 22px body text with a bold opener is a newspaper standfirst device. 19px and `--ink-2` match the existing `.deck` style, so the summary reads like an abstract. The new opening runs to four sentences, which needs a slightly smaller size to stay comfortable.

### 3. Remove the bold one-liner and the pull-quote (text only; CSS can stay unused)
Delete the `<p class="short-coda">Lopsided, not one-sided.</p>` and `<p class="short-q">We can't say who is right. We can say the front door changed.</p>` elements. If a closing line is wanted, use plain `.cap` text.
*Why.* Pull-quoting your own aphorism is a sales device, and both test readers flagged these lines as editorial verdicts (reader_2: "an editorial judgment"). With them gone, the counter-direction numbers have to carry the point themselves.

### 4. Neutralise the year chips on the Nakba quote pair
Change the inline styles on the two `.news-q .w i` swatches from `var(--comp)` / `var(--topic)` to a single neutral, for example `var(--muted)` for 2021 and `var(--ink-2)` for 2026, or drop the swatches.
*Why.* Elsewhere on the page those two colours mean comparison articles vs topic articles. Here they mean 2021 vs 2026, so a careful reader may infer that the 2021 text is a "comparison" baseline. One colour meaning per page.

### 5. Eyebrow and disclosure labels: descriptive rather than promotional (text only)
- `Start here` → `Summary`
- `Why you can trust this` → `How we checked this`
- `What this does not mean` → `Limitations`
- `Questions people ask` can stay.
*Why.* "Why you can trust this" asks for trust instead of showing the checks. Pew and OWID label these sections plainly ("Methodology", "How we did this").

### 6. Header: keep the design, soften two details (optional)
```css
.hero h1{font-size:clamp(34px,5.4vw,68px)}
.hero h1 em{font-style:italic;font-weight:400;color:inherit}   /* keep italics, drop the teal */
```
*Why.* Once the summary sits above it, the hero title is the second headline on screen, and 84px dwarfs it. 68px still reads as the cover title. The teal on "anti-colonial framing" puts the data colour on the contested phrase itself, which reads as emphasis by the authors. Italic alone keeps the typographic rhythm.
Text (optional): the hero question uses "anti-colonial framing", a term the summary never uses. To keep one term per concept, consider "...drift toward more critical vocabulary?". Leave it if the owner prefers the current wording; it is a question, and the summary answers it.

### 7. Leave as they are
- `.short` bottom rule (`3px double var(--ink)`): a quiet newspaper rule, fine.
- `.card` styling and the five numbered cards: restrained; the 3px ink top border matches the rest of the page.
- All charts, the hero edit-stream and its amber marks (amber means "undone edit" there, which is a data meaning).
- Optional, outside the summary: the amber `.xchip` badges ("Full crawl · 10,320 articles") reuse the "removed/undone" colour as a label background. A neutral outline (`background:none;border:1px solid var(--rule);color:var(--muted)`) would keep amber for its data meaning. The eyebrow "The twist" could become a descriptive label for the same reason.

## Net effect
One display headline at the top (the hero), a section headline at h2 scale, no colour on rhetoric, no bolded verdicts. The charts and palette are unchanged.
