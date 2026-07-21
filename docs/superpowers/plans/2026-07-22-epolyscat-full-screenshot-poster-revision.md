# ePolyScat Full-Screenshot Poster Revision Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Show every evidence image in full while preserving the approved English copy, equal contributor widths, and a one-page 122 x 91 cm poster.

**Architecture:** Keep the existing 2-by-2 evidence narrative, but increase each evidence tile to the natural full-image aspect ratio. Recover vertical space by compressing Engineering Decisions and Scientific Value into a shallow two-column band, reducing Acceptance Result to a banner, and replacing the tall metric cards with a compact single-row strip.

**Tech Stack:** LaTeX, beamerposter, tcolorbox, TikZ, Tectonic, Poppler.

---

### Task 1: Replace cropped evidence frames with complete images

**Files:**
- Modify: `docs/poster/epolyscat-progress-poster.tex:113-137`
- Modify: `docs/poster/epolyscat-progress-poster.tex:284-319`

- [ ] **Step 1: Increase evidence-card height**

Change `\EvidenceTile` from `height=9.25cm` to `height=14.3cm`. Keep the numbered heading and caption styles unchanged so the additional height is assigned to image content.

- [ ] **Step 2: Remove all image-content cropping**

Use these complete-image expressions in the four evidence tiles:

```tex
\includegraphics[width=\linewidth]{workflow-new-run.png}
\includegraphics[width=\linewidth]{input-preservation.png}
\includegraphics[width=\linewidth]{workflow-evidence.png}
\includegraphics[width=0.47\linewidth]{scientific-visualization.png}\hfill
\includegraphics[width=0.47\linewidth]{scientific-visualization-alt.png}
```

The browser chrome is already excluded from the three portal assets, so no additional clipping or `trim` option is needed.

- [ ] **Step 3: Increase the containing evidence block**

Change the `Evidence narrative: from input to interpretation` content box from `height=22.7cm` to `height=32.5cm`. Keep the 2-by-2 Configure, Preserve, Verify, and Interpret order and all approved captions.

- [ ] **Step 4: Compile to expose any geometry overflow**

Run:

```bash
tectonic --keep-logs --keep-intermediates --outdir docs/poster docs/poster/epolyscat-progress-poster.tex
```

Expected: exit code 0. Temporary vertical overflow is acceptable until Task 2; undefined controls or missing assets are not.

### Task 2: Recover height from explanatory and metric regions

**Files:**
- Modify: `docs/poster/epolyscat-progress-poster.tex:322-373`

- [ ] **Step 1: Compress the Engineering Decisions / Scientific Value band**

Set both `contentbox` heights to `6.3cm`. Use `\fontsize{13.4}{15.8}\selectfont` for the four engineering bullets with `\itemsep=0.02cm`, and `\fontsize{14.0}{17.0}\selectfont` for the scientific-value paragraph. Retain the exact approved wording.

- [ ] **Step 2: Reduce the acceptance banner**

Change the Acceptance Result claim box to `height=3.4cm`, its label gap to `0.08cm`, and its body to `\fontsize{14.2}{17.0}\selectfont`. Retain the complete portal-to-visualization conclusion.

- [ ] **Step 3: Convert validation into a compact strip**

Change the Acceptance Evidence content box to `height=5.5cm`. Change each metric to `\TinyEvidence[2.75cm]` and reduce `\TinyEvidence`'s number and label sizes only if the first compile shows wrapping. Keep all four approved values and the single approved supporting line.

- [ ] **Step 4: Tighten vertical gaps in Contribution A**

Use `0.35cm` between the Key Contribution, evidence narrative, engineering band, acceptance banner, and metric strip. Do not change Contribution B spacing or any `\Partner...` macro.

### Task 3: Compile, render, and visually inspect

**Files:**
- Regenerate: `docs/poster/epolyscat-progress-poster.pdf`
- Regenerate: `docs/poster/epolyscat-progress-poster-preview.png`

- [ ] **Step 1: Compile twice**

Run:

```bash
tectonic --keep-logs --keep-intermediates --outdir docs/poster docs/poster/epolyscat-progress-poster.tex
tectonic --keep-logs --keep-intermediates --outdir docs/poster docs/poster/epolyscat-progress-poster.tex
```

Expected: both commands exit 0.

- [ ] **Step 2: Verify PDF geometry and TeX diagnostics**

Run:

```bash
pdfinfo docs/poster/epolyscat-progress-poster.pdf | rg 'Pages|Page size'
rg -n 'Overfull|Underfull|Undefined control sequence|LaTeX Error|Package .* Error|Emergency stop' docs/poster/epolyscat-progress-poster.log
```

Expected: one page, `3458.27 x 2579.53 pts`, and no diagnostic matches.

- [ ] **Step 3: Render the review image**

Run:

```bash
pdftoppm -png -r 80 -singlefile docs/poster/epolyscat-progress-poster.pdf docs/poster/epolyscat-progress-poster-preview
```

Inspect the preview and confirm that all three portal screenshots show their complete captured page, both orbital images show their original labels and boundaries, Contribution A stays above the footer, and Contribution B is unchanged.

- [ ] **Step 4: Verify required copy and replacement macros**

Extract PDF text and confirm Configure, Preserve, Verify, Interpret, Engineering decisions, Scientific value, Acceptance result, and all four metrics are present. Confirm exactly eight named partner macros remain in the TeX source.

### Task 4: Commit the scoped poster revision

**Files:**
- Commit: `docs/poster/epolyscat-progress-poster.tex`
- Commit: `docs/poster/epolyscat-progress-poster.pdf`
- Commit: `docs/poster/epolyscat-progress-poster-preview.png`

- [ ] **Step 1: Remove generated auxiliary files from the working tree**

Delete only `docs/poster/epolyscat-progress-poster.aux`, `.log`, and `.nav` after verification. Do not modify unrelated existing worktree files.

- [ ] **Step 2: Check and stage the exact scope**

Run:

```bash
git diff --check -- docs/poster/epolyscat-progress-poster.tex
git add docs/poster/epolyscat-progress-poster.tex \
  docs/poster/epolyscat-progress-poster.pdf \
  docs/poster/epolyscat-progress-poster-preview.png
git diff --cached --stat
```

Expected: only the three poster outputs are staged.

- [ ] **Step 3: Commit**

Run:

```bash
git commit -m "docs: show complete poster evidence screenshots"
```

Expected: one scoped documentation commit on `feature/epolyscat-workflow-run-flow`.
