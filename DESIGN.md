# HRIS report, design system

The living design reference for everything published from this repo. Update it when a decision changes; the page must match this file.

## Intent
An editorial, magazine-like reading experience for a long Hebrew research report. Feels like a serious newspaper feature, not a dashboard and not a SaaS landing page. Calm, white, generous whitespace, one strong accent.

## Language and direction
- Hebrew, RTL (`<html lang="he" dir="rtl">`). Numbers and Latin terms sit inline with `unicode-bidi: plaintext` on table cells.
- Arrows that mean "next" point left in running RTL layouts and down in stacked (mobile) layouts. Never a right-pointing arrow for "leads to".
- No serif fonts anywhere. Display and body are both **Heebo** (300, 400, 500, 700, 800, 900).

## Color
| Token | Light | Dark | Use |
|---|---|---|---|
| `--bg` / `--paper` | `#ffffff` | `#0f1012` / `#141518` | page and surfaces |
| `--ink` | `#111111` | `#ededea` | headings, hairline rules, active text |
| `--ink-2` | `#333333` | `#c9c9c4` | body text in cards and tables |
| `--muted` | `#6f7379` | `#9a9ea6` | captions, eyebrows, menu items |
| `--line` | `#ebebeb` | `#26282d` | hairlines |
| `--accent` | `#e5322d` | `#ff6b64` | the one accent: eyebrows, big numbers, active tab underline, progress bar, arrows |
| `--accent-soft` | `#fdeeed` | `#3a1616` | hover fills only |
| `--code` | `#f6f6f6` | `#1c1e23` | code and range tracks |

Rules. One accent, used sparingly and always for meaning (a number to notice, the active state, a transition). Never colored text for body copy. Never a second accent. Status colors are not used in this report.

## Type scale
- H1 display: `clamp(2.2rem, 5.4vw, 4.4rem)`, weight 900, tight leading (1.08), max 22ch.
- H2: `clamp(1.7rem, 3vw, 2.3rem)`, weight 900, a 56px red rule above it (the section eyebrow).
- H3: 1.28rem, weight 800.
- Body: 18px / 1.8 (17px on phones). Measure 46rem for running text; tables and components break out to the full 74rem column.
- Eyebrows and table headers: 0.7 to 0.8rem, uppercase, letter-spacing 0.12 to 0.18em, muted.

## Layout
- Two columns on desktop: content (flex) and a 17rem floating menu on the reading side. Single column under 980px.
- Floating menu: a glass card (`backdrop-filter: blur(16px)`), hairline border, soft shadow, radius 14px. **It never scrolls inside itself**: only H2 entries are listed so it always fits the viewport. Active item is red bold text, no bars or brackets. On phones it collapses to a red pill button that opens the list.
- A 3px red reading-progress bar at the top.
- Hero: kicker with a short red dash, display H1, a light-weight lede, three stat tiles with a black top rule, then a hairline meta row.

## Boxes are the exception
Prefer hairlines and whitespace over cards. The only bordered surfaces are the floating menu and the two intro callouts (top rule in ink, bottom rule in line). Tables have a 2px ink top rule, a 1px line bottom rule, and no side borders. Cards inside components (value map, pre-mortem, stepper) are separated by rules, not by boxes.

## Components (all built in `components.py`, styled in `template.html`)
| Component | Where | Behavior |
|---|---|---|
| Stat tiles | hero | three headline numbers, source in the caption |
| Stepper | section 5 | three stages with transition conditions between them; click opens the matching option tab and scrolls to it |
| Team-size calculator | section 2 | range slider 1,000 to 100,000 employees; outputs the Insight222 ratios |
| Option tabs | section 5 | three panels, underline tabs; all panels print |
| Data-weight bars | section 4 | one hue, three bars, labeled in words |
| AI value map | section 6 | three columns from the source table, one card per use case |
| KPI tabs + stage filter | section 9.9 | five goal panels; the filter dims rows whose stage column does not include the chosen stage |
| Success timeline | section 9.9 | four points on a hairline |
| Pre-mortem cards | section 9.7 | three stories with big red numerals |

Every component is generated from the source note. Content is never hand-edited in HTML.

## Illustrations
Style: hand-drawn notebook doodles on cream lined paper, black marker line art, simple black blob characters with white eyes, small icons (clock, tangle, warning sign), with the accent in **red** (`#e5322d`) instead of green. Short English labels only (image models render Hebrew unreliably). Generated with `gpt_image_2_5` via Higgsfield; the style reference is `assets/style-reference.png`. Every illustration gets an `alt` in Hebrew and sits full-width inside the 46rem measure with a muted caption.

Current set (`assets/`): `og.png` (1200x630 cover), `stages.jpg` (three stages staircase, section 5), `payroll-anchor.jpg` (global core, interface, local payroll, section 3), `treadmill.jpg` (no launch, maintenance forever, section 7), `headcount.jpg` (HR vs Finance headcount and the data dictionary, section 4), `queue.jpg` (protect the team from the queue, section 9.2). Placement and captions live in `components.ILL`; a figure is inserted right after the heading whose text contains the needle.

OG image: 1200x630, same style, title in English, red accent, saved as `assets/og.png` and declared in `<meta property="og:image">`. Favicon: `assets/favicon.svg` (black rounded square, red dot).

## Build
`python3 build.py` reads the vault note, converts with marked, applies `components.py`, injects into `template.html`, writes `index.html`. Commit and push; GitHub Pages serves `/`.

## Do not
- No serif fonts. No second accent color. No cards with drop shadows around text. No emoji in headings. No colons or em dashes as punctuation in prose (Avi's writing rule). No inner scrolling in the menu. No content that is only in the HTML and not in the note.
