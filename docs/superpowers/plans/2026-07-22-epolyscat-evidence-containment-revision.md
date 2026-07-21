# ePolyScat Evidence Containment Revision Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Keep all three complete portal screenshots fully inside their evidence cards while making Engineering Decisions more compact and more readable.

**Architecture:** Add vertical padding to every evidence tile without changing image width or aspect ratio, then recover the added height from the under-filled Engineering Decisions / Scientific Value row. Regenerate and visually inspect the one-page poster before committing only the TeX, PDF, and preview image.

**Tech Stack:** LaTeX, beamerposter, tcolorbox, Tectonic, Poppler.

---

### Task 1: Correct evidence-card containment

**Files:**
- Modify: `docs/poster/epolyscat-progress-poster.tex:113-137`
- Modify: `docs/poster/epolyscat-progress-poster.tex:284-321`

- [ ] **Step 1: Increase every evidence tile**

Change the shared `\EvidenceTile` height from `14.3cm` to `14.7cm`. Do not change image widths and do not add `trim`, `clip`, or fixed image heights.

- [ ] **Step 2: Increase the two-row evidence container**

Change the Evidence Narrative content box from `32.5cm` to `33.3cm`, adding exactly the combined `0.8cm` growth of its two evidence rows.

- [ ] **Step 3: Compile the containment change**

Run:

```bash
tectonic --keep-logs --keep-intermediates --outdir docs/poster docs/poster/epolyscat-progress-poster.tex
```

Expected: exit code 0 and no missing-asset or undefined-control errors.

### Task 2: Compress and enlarge the engineering row

**Files:**
- Modify: `docs/poster/epolyscat-progress-poster.tex:323-351`

- [ ] **Step 1: Reduce both row boxes**

Set Engineering Decisions and Scientific Value to `height=5.0cm` so the two-column row remains aligned.

- [ ] **Step 2: Increase Engineering Decisions type**

Use this exact type treatment while preserving all four approved bullets:

```tex
{\fontsize{14.8}{17.2}\selectfont
\begin{itemize}
  \setlength{\itemsep}{0cm}
  ... existing four bullets ...
\end{itemize}}
```

- [ ] **Step 3: Increase Scientific Value type**

Set its paragraph to `\fontsize{14.5}{17.2}\selectfont`, reduce the slogan gap to `0.12cm`, and keep the complete approved sentence and slogan.

### Task 3: Verify poster geometry and visual balance

**Files:**
- Regenerate: `docs/poster/epolyscat-progress-poster.pdf`
- Regenerate: `docs/poster/epolyscat-progress-poster-preview.png`

- [ ] **Step 1: Compile twice and render the preview**

Run:

```bash
tectonic --keep-logs --keep-intermediates --outdir docs/poster docs/poster/epolyscat-progress-poster.tex
tectonic --keep-logs --keep-intermediates --outdir docs/poster docs/poster/epolyscat-progress-poster.tex
pdftoppm -png -r 80 -singlefile docs/poster/epolyscat-progress-poster.pdf docs/poster/epolyscat-progress-poster-preview
```

Expected: all commands exit 0.

- [ ] **Step 2: Check automated requirements**

Run:

```bash
pdfinfo docs/poster/epolyscat-progress-poster.pdf | rg 'Pages|Page size'
rg -n 'Overfull|Underfull|Undefined control sequence|LaTeX Error|Package .* Error|Emergency stop' docs/poster/epolyscat-progress-poster.log
sed -n '285,325p' docs/poster/epolyscat-progress-poster.tex | rg 'trim=|clip'
```

Expected: one page, `3458.27 x 2579.53 pts`, no TeX diagnostic matches, and no evidence-cropping matches.

- [ ] **Step 3: Inspect the full-page preview**

Confirm that the lower edge of Configure, Preserve, and Verify remains inside each tinted evidence card; Engineering Decisions uses visibly larger type without overflow; Contribution A stays above the footer; and Contribution B is unchanged.

### Task 4: Commit only revised poster outputs

**Files:**
- Commit: `docs/poster/epolyscat-progress-poster.tex`
- Commit: `docs/poster/epolyscat-progress-poster.pdf`
- Commit: `docs/poster/epolyscat-progress-poster-preview.png`

- [ ] **Step 1: Remove generated auxiliary files**

Remove only the generated `.aux`, `.log`, and `.nav` files under `docs/poster/` after verification.

- [ ] **Step 2: Stage and inspect exact scope**

Run:

```bash
git diff --check -- docs/poster/epolyscat-progress-poster.tex
git add docs/poster/epolyscat-progress-poster.tex \
  docs/poster/epolyscat-progress-poster.pdf \
  docs/poster/epolyscat-progress-poster-preview.png
git diff --cached --stat
```

Expected: exactly three poster files are staged.

- [ ] **Step 3: Commit**

Run:

```bash
git commit -m "docs: contain poster evidence frames"
```

Expected: one scoped documentation commit on the current feature branch.
