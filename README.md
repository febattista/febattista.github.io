# febattista.github.io

Personal website built on [al-folio](https://github.com/alshedivat/al-folio) (Jekyll, MIT license).
This file is the house standard: what to touch when adding a paper, a talk, a
software project, or a news item, and how the site turns those files into pages.
Theme documentation lives in `INSTALL.md`, `CUSTOMIZE.md`, and `FAQ.md`.

## 1. Where things live

| What | File(s) | Edited by |
| --- | --- | --- |
| Papers, software, talks | `_bibliography/papers.bib`, `software.bib`, `talks.bib` | **never by hand** (see §2) |
| Badge colors / links (`abbr`, `note`) | `_data/venues.yml` | you |
| Coauthor links | `_data/coauthors.yml` | you |
| Talk slides | `assets/pdf/talks/*.pdf` | you |
| CV PDF (the "cv" nav item, `cv:` in `_config.yml`) | `assets/pdf/CV.pdf` | `make install` |
| News | `_news/announcement_N.md` | you |
| Page intros | `_pages/about.md` (home), `publications.md` (`/research/`), `talks.md`, `repositories.md` (`/software/`) | you |
| How a bib entry is rendered | `_layouts/bib.liquid` | only when changing the standard |

## 2. The bibliography pipeline

```
Zotero (Better BibTeX auto-export)
  └─> applicationMaterial/references/{MyPapers,MySoftware,MyTalks}.bib   (also used by the LaTeX CV)
        └─> make install  (in applicationMaterial)
              └─> _bibliography/{papers,software,talks}.bib  +  assets/pdf/CV.pdf   → commit → push
```

- Add or fix an entry **in Zotero**, then run `make install` in `applicationMaterial`.
  Anything edited directly in `_bibliography/` is overwritten at the next install.
- Files must be in **BibTeX** format (`year`, `journal`, `address`, `@techreport`,
  `@phdthesis`), not BibLaTeX (`date`, `journaltitle`, `location`, `@report`).
  jekyll-scholar only understands the former.
- The custom fields below (`abbr`, `selected`, `keywords`, `pdf`, `note`, …) are
  Zotero "extra" fields; they are hidden from the Bib popup by
  `filtered_bibtex_keywords` in `_config.yml`.

## 3. Adding a paper (`papers.bib` → `/research/`)

```bibtex
@article{BatDeDealing24,
  title     = {Dealing with Inequality Constraints in ...},
  author    = {Battista, Federico and De Santis, Marianna},
  year      = 2024,
  journal   = {4OR. A Quarterly Journal of Operations Research},
  doi       = {10.1007/s10288-024-00569-5},
  abbr      = {4OR},
  selected  = {true},
  keywords  = {paper}
}
```

How each field is used on the site:

| Field | Effect |
| --- | --- |
| `abbr` | Text of the badge on the left. Add the same key to `_data/venues.yml` for a color (and an optional `url`); otherwise the badge is gray. |
| *(no `abbr`)* | Badge is derived from the entry: `@techreport` with `doi`/`url` → **Preprint**, `@techreport` without → **Working Paper**, `@phdthesis` → **Ph.D. Thesis**, `@inproceedings` → **Proceedings**. These four keys are already in `venues.yml`. |
| `journal` / `type`+`institution` / `booktitle` / `school` | Venue line, for `@article` / `@techreport` / `@inproceedings` / `@phdthesis` respectively, followed by `year`. |
| `note` | Printed as a second line under the venue (e.g. `Under review at ...`). |
| `doi` | **DOI** button. If absent, `url` gets the button instead. |
| `pdf` | **PDF** button; the value is a path relative to `assets/pdf/`. |
| `selected` | Only used by the "selected publications" block on the home page, which is **disabled** (`selected_papers` commented out in `_pages/about.md`). Harmless; keep `{true}` for the main papers so it works when enabled. |
| `keywords` | `paper` / `talk` are used by the LaTeX CV only. `software` is the one value the site reacts to (§5). Keep them consistent anyway. |
| `author` | Your name is italicized automatically (`scholar.last_name` in `_config.yml`). Coauthors get a link if listed in `_data/coauthors.yml` (§6). Entries with more than 3 authors are truncated with a "more authors" toggle. |

Working paper / preprint example:

```bibtex
@techreport{BatRalBranchcut24,
  type        = {arXiv Preprint},            % shown in the venue line; makes the badge "Preprint"
  title       = {Improving Directions in Mixed Integer Bilevel Linear Optimization},
  author      = {Battista, Federico and Ralphs, T. K.},
  year        = 2025,
  institution = {COR@L Laboratory, Lehigh University},
  url         = {https://doi.org/10.48550/arXiv.2511.03566},   % gives the button; without it → "Working Paper"
  note        = {Under review at Mathematical Programming Computation},
  keywords    = {paper}
}
```

## 4. Adding a talk (`talks.bib` → `/talks/`)

Talks are stored as `@article` where `journal` is the event.

```bibtex
@article{BatRalBranchcut24a,
  title    = {A Branch-and-Cut Algorithm for ...},
  author   = {Battista, Federico and Ralphs, T. K.},
  year     = 2024,
  journal  = {International Symposium on Mathematical Programming},  % event name
  address  = {Montreal, Canada},                                     % city
  abbr     = {ISMP},                                                 % badge → add to venues.yml
  pdf      = {talks/ISMP2024.pdf},                                   % slides → assets/pdf/talks/ISMP2024.pdf
  keywords = {talk}
}
```

Checklist: copy the slides to `assets/pdf/talks/`, name them `<ABBR><YEAR>.pdf`,
and add a new `abbr` to `_data/venues.yml` under "Conferences".

## 5. Adding software (`software.bib` → `/software/`)

```bibtex
@article{SDPliftandproject,
  title    = {SDP\_lift\_and\_project},
  author   = {Battista, Federico and Rossi, Fabrizio and Smriglio, Stefano},
  year     = 2025,
  url      = {https://github.com/febattista/SDP_lift_and_project},  % button
  note     = {Maintainer},          % badge: "Maintainer" or "Contributor" (colors in venues.yml)
  keywords = {software}             % REQUIRED: this is what switches the template to software mode
}
```

In software mode the badge is taken from `note` instead of `abbr`, and `note` is
not printed as text. `publisher` is accepted but not shown.
`_data/repositories.yml` is not used by the page at the moment.

## 6. Coauthor links (`_data/coauthors.yml`)

Key is the lowercase last name; list every first-name spelling that appears in
the `.bib` files, otherwise the link is not applied.

```yaml
"ralphs":
  - firstname: ["Ted", "T. K.", "T.K.", "Ted K."]
    url: https://scholar.google.com/citations?user=ljOCOAwAAAAJ
```

## 7. Adding news (`_news/`)

One file per item, `announcement_<N>.md`. The `date` sets the order; the home
page shows the 5 most recent (`announcements.limit` in `_config.yml`), all of
them appear on `/news/`.

```markdown
---
layout: post
date: 2025-11-10 08:00:00-0400
inline: true
related_posts: false
---

Our work entitled _Title_ is available as a pre-print in [arXiv](https://doi.org/...).
```

`inline: true` = one-liner in the list (the standard here). Link slides as
`/assets/pdf/talks/<file>.pdf`.

