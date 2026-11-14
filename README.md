# Yitao Hu’s homepage

A responsive, English-only academic homepage for GitHub Pages / `flashserve.org`.
The deployed page is ordinary static HTML, CSS, and JavaScript. No package
installation, JavaScript framework, external font, or runtime API is required.

## Edit and build

- `templates/index.html`: biography, sidebar, navigation, service, honors,
  teaching, students, and alumni.
- `data/publications.json`: the existing selected papers, authors, venue/year,
  CCF labels, abstracts, citation metadata, resource links, and source provenance.
- `data/news.json`: recent news, displayed six items at a time with earlier items
  behind an inline disclosure. `html` is trusted, author-edited HTML.
- `assets/css/home.css` and `assets/js/home.js`: responsive presentation and
  progressively enhanced interactions.

After editing the template or data, run from this repository:

```sh
python3 scripts/build.py
```

`index.html` is the generated, checked-in delivery. It includes all content and
native Abstract/BibTeX disclosures, so reading does not depend on JavaScript.
JavaScript enhances the mobile menu, active navigation, inline disclosure buttons, and citation copying. The fixed action row and the disclosure panels are separate elements, so Abstract/BibTeX panels open below all the buttons; one panel is open at a time per paper. External Paper/Code/Slides/Dataset links still open their resources directly.
Open `index.html` directly, or preview locally:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

`zh.html` redirects old Chinese-homepage links to the English page. Original
HTML was preserved outside this public repository before the redesign.
Existing `archive/`, historical CSS/JS, original images, Git history, slides,
and the custom-domain `CNAME` remain intact.

## Content provenance and date conventions

The November 2026 redesign retains the original publication selection, except
TopoServe, removed at the owner’s request. Published/accepted work is grouped by year, newest first. Within each year, conference papers precede journal papers, followed by preprints; conference venue groups are ordered CCF-A before CCF-B, and papers in the same venue stay adjacent. The 2025 Nature paper is the explicit first entry for that year. Verified dates and original order break remaining ties. `publication_type` explicitly records conference, journal, or preprint. Preprints retain the original homepage’s year labels and appear at the end of their respective year, with no separate Preprints section. BibTeX describes the verified source: where only an arXiv record is
available, it cites that record rather than inventing conference proceedings.

Authors/citations were checked against publisher metadata, Crossref, and arXiv.
Abstracts use public records and author manuscripts; sources accompany each
paper in the data. TightLLM, SLOpt, Lark, and the IWQoS 2023 HRL paper use indexed
abstract mirrors because publisher access was restricted; the data identifies
these four for comparison against final author PDFs. PDF word spacing and basic
TeX symbols were normalized for readability. Resource buttons appear only when
a resource URL is available. Only Yitao Hu receives a corresponding-author asterisk, as requested by the owner. Corresponding-author roles are backed by explicit paper evidence or the owner’s confirmation; equal-contribution marks are not inferred. SLOpt, FlexKV, and Mosaic were confirmed by the owner on 2026-11-14; TightLLM was confirmed not to have Yitao Hu as corresponding author.

News dates and event wording were updated from the owner's explicit chronology
on 2026-11-14. The 20 entries are ordered newest first; six are initially visible,
with the remainder in Earlier news. Invitation months are separate from the
conference years (ISCA, HPCA, and INFOCOM 2027). The ReWY news performance range
uses the owner's supplied 1.25–2.89× summary; per-platform arXiv benchmark ranges
have a different scope, recorded in the news metadata. PAT's one-line integration
refers to configuration after plugin installation. The Xiaomi award year is 2025
in both News and Honors. Earlier Xiaotian, SoCC, and Twen items are preserved.

## Validation

The local revision was checked in Chromium at widths 320, 375, 390, 600, 768,
1024, 1440, and 1920 pixels, including overflow, images, menu behavior, same-page
navigation, active sections, native disclosures, citation copying, legacy
language redirect, no-JavaScript reading, and reduced-motion behavior.
Local fragment and asset references were checked. External publishers may
restrict automated requests; their availability is not guaranteed by a local
link check. No commit, push, or production deployment is part of this revision.


## Publication display refinements (2026-11-14)

Paper entries use whitespace between them and year headings as separators.
Venue badges contain abbreviations only; the year is shown once per group.
Yitao Hu’s name is bold and underlined; an asterisk follows his name only when
his corresponding-author role is explicitly verified or confirmed by him.
Other corresponding-author roles remain in the source metadata but are not
marked in the rendered page. The introductory publication caption is removed.

Scrooge, Rim, and ServerlessLoRA do not explicitly designate corresponding
authors in the checked full texts, so no mark is inferred. Provenance is stored
per paper in `corresponding_author_evidence`. The owner’s confirmation resolves
Mosaic’s older-versus-current arXiv correspondence-footnote difference.
