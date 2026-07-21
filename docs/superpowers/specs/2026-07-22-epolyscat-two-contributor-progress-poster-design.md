# ePolyScat Two-Contributor Progress Poster Design

## Goal

Create an English-language, 122 x 91 cm landscape poster for a project acceptance defense. The poster presents the ePolyScat research portal as an evidence-driven system and gives Ziming Zhang and Nguyen, Thinh M equal visual ownership. Ziming's half is fully authored from the current branch and verified execution records; Thinh's half is a structured, replaceable contribution template.

## Audience and Success Criterion

The primary audience is a project acceptance review panel. The poster should make one conclusion immediately visible: the portal provides an end-to-end workflow whose implemented behavior is backed by reproducible input handling, remote execution contracts, scientific-output verification, and real portal/HPC evidence.

The poster intentionally omits a risks, limitations, future work, and references section at the user's request. Claims in Ziming's section must still remain narrowly scoped to evidence that can be reproduced from the branch, the local portal, or the validation record.

## Format and Visual Direction

- Canvas: 122 cm wide by 91 cm high, landscape, matching the supplied beamerposter template.
- Language: English.
- Style: evidence-led academic poster with a modern editorial treatment.
- Palette: deep navy, teal, warm white, and restrained amber highlights.
- Typography: large sans-serif hierarchy, short paragraphs, compact captions, and no dense code listings.
- Composition: a shared header and shared project claim above two equally weighted contribution zones.

The implementation will use `beamerposter` with self-contained colors and block styling so the poster does not depend on unavailable external Gemini/MSU theme files. The supplied template determines the physical format and overall academic-poster idiom rather than requiring a byte-for-byte theme fork.

## Header and Shared Content

Title:

> An Evidence-Driven ePolyScat Research Portal

Subtitle:

> End-to-End Scientific Workflows, Reproducible Inputs, and Verified Computation

Authors and affiliation:

> Ziming Zhang; Nguyen, Thinh M  
> Georgia Institute of Technology

The shared strip contains two concise statements:

- Project objective: turn fragmented scientific tools into a traceable, reviewable research workflow.
- Acceptance claim: connect configuration, execution, scientific validation, and stage-to-stage handoff in one portal experience.

The shared content uses approximately 18 percent of the body height. The two contribution zones split the remaining principal body width equally.

## Contribution A: Ziming Zhang

Section title:

> Workflow Portal and Scientific Verification

The section is organized around a four-stage presentation flow:

1. Data Generation
2. ePolyScat Run
3. Post-processing
4. Visualization

The first three stages represent the remote computational chain; Visualization is a local presentation stage. This distinction follows the current branch's `WORKFLOW_STAGES` and `WORKFLOW_PRESENTATION_STAGES` definitions.

### Content Blocks

1. **Guided workflow**
   - Module, Utility, and Workflow run modes.
   - Required-file contracts and readiness state.
   - Editable step continuation rather than a hidden batch chain.

2. **Reproducible scientific inputs**
   - File View and Table View synchronization.
   - Lossless ordered document model for repeated records, commands, comments, blank lines, and unknown input.
   - Ordered Sequence editing without replacing source text with generated defaults.

3. **Verified handoff**
   - Output manifests carry semantic roles and provenance.
   - Stage continuation depends on scientific evidence, not scheduler completion alone.
   - Compatible predecessor output is selected and remains reviewable before submission.

4. **Runtime contracts**
   - Django orchestration over Airavata gRPC.
   - Resource-aware application and utility dispatch.
   - Remote wrappers propagate failure and require application-specific scientific completion evidence.

### Primary Visuals

- Four-stage Workflow screenshot showing the configured research journey.
- Ordered Sequence / structured input screenshot demonstrating lossless editing.
- View Run screenshot showing scientific verification, output provenance, and continuation.
- Molecular-orbital or scientific-result screenshot demonstrating local interpretation.
- Architecture diagram: a native TikZ flow from Portal to Django to Airavata gRPC to HPC execution to Scientific Verification and Provenance-Aware Handoff.

If live authenticated data prevents a useful capture, the poster uses the repository's existing browser screenshots as a fallback and labels their represented behavior precisely.

### Validation Evidence Sources

The following detailed records support the concise visible metrics and remain
available for oral defense:

- Current branch delta against `origin/main`: 34 commits, 67 changed files, 24,896 insertions, and 782 deletions at design time.
- Fresh local automated test/build results collected during poster production, replacing older counts when a broader successful run is available.
- Portal Run 23 on Expanse: verified OpenMolcas scientific outputs and inherited `.scf.molden` handoff.
- Portal Run 31 on Frontera: verified ePolyScat command sequence and generated `test01Blms.dat`.
- Frontera job 7861631: four-task manual `test03`, `COMPLETED 0:0`, four `End EDCS` markers, final `Finalize`, and no `Abnormal Ending`.
- Stampede3 jobs 3316916 and 3316918: verified ePolyScat EDCS completion and OpenMolcas `Happy landing` with Molden outputs.

The visible validation block uses only the four approved headline metrics. The
detailed records above are not printed as a job log. The layout still emphasizes
the separation between scheduler state and scientific success without adding a
risks or failure-summary panel.

## Contribution B: Nguyen, Thinh M

Thinh's section has the same border weight, title hierarchy, main-visual area, and evidence-card density as Ziming's section. It is deliberately structured rather than left blank.

All replaceable content is defined near the beginning of the TeX file through named macros:

- `\PartnerTitle`
- `\PartnerClaim`
- `\PartnerMethod`
- `\PartnerImplementation`
- `\PartnerVisual`
- `\PartnerVisualCaption`
- `\PartnerValidation`
- `\PartnerMetrics`

Default macro values render explicit bracketed prompts such as `[Partner Progress Title]` and `[Primary result figure or screenshot]`. A short comment beside each macro explains the intended content length. Replacing the macros must not require edits to layout code.

## Footer

The footer contains:

- Shared stack: Vue 2, Django, Airavata gRPC, and HPC.
- `Project Acceptance Review - July 2026`.
- `Georgia Institute of Technology`.

No repository URL or email address is shown unless the user supplies them later.

## Files and Assets

Create a self-contained poster directory:

- `docs/poster/epolyscat-progress-poster.tex`: poster source and partner macros.
- `docs/poster/assets/`: cropped live screenshots and any rendered supporting assets.
- `docs/poster/epolyscat-progress-poster.pdf`: compiled review artifact.

Application source files are not modified. Existing untracked databases, archives, and user documents remain untouched.

## Evidence Sources

The poster content is derived from:

- Current Git history and `origin/main...HEAD` diff on `feature/epolyscat-workflow-run-flow`.
- Current workflow, serializer, scientific-output, runtime-contract, and input-document code.
- Existing repository notes in `docs/` and wrapper regression tests in `ops/`.
- Feishu document `WpeldzUJQoEfGFxH0skckKQbn0b`, revision 15, especially Sections 9 and 10.
- Live local portal at `127.0.0.1:8000` and its Vue development server for current screenshots.

When evidence sources differ, the current code and a fresh reproducible check take precedence over historical prose.

## Build and Verification

1. Capture screenshots at a consistent desktop viewport and crop them to the poster's image frames.
2. Run a representative backend test suite, parser/contract tests, frontend production build, and wrapper regression tests in proportion to available local dependencies.
3. Record only successful, reproducible counts in the poster.
4. Compile the TeX source twice with Tectonic/XeTeX.
5. Render the PDF to a high-resolution image and inspect it for clipping, text overflow, unreadable captions, raster blur, and unequal contributor weight.
6. Check that replacing every partner macro with realistic text does not require layout changes.
7. Run `git diff --check` and verify that no unrelated working-tree files are staged.

## Acceptance Criteria

- The output is a valid 122 x 91 cm landscape PDF and a reusable local `.tex` source.
- The shared header names both contributors and Georgia Tech.
- Ziming's section communicates the four-stage workflow and presents defensible implementation and validation evidence.
- Thinh's section is visually equal and editable exclusively through clearly named macros and one visual asset reference.
- The poster contains no Remaining Risks, Next Steps, or References block.
- All text remains readable at poster scale and no content crosses block boundaries.

## Approved Evidence-Narrative Revision

The July 22 review identified that two screenshots did not fully communicate the
end-to-end research experience. Contribution A will therefore use a four-image,
2-by-2 evidence narrative. Each image has one job and a short conclusion-led
caption:

1. **Configure** — show the complete four-stage workflow and explicit required
   scientific inputs.
2. **Preserve** — show the Ordered Sequence / structured input surface and the
   lossless preservation of commands, comments, repeated records, and source
   ordering.
3. **Verify** — show a scientifically verified run, its output artifacts, and
   the continuation contract.
4. **Interpret** — show a real molecular-orbital or scientific-result
   visualization produced from workflow output.

The images are evidence tiles rather than four reduced full-page screenshots.
They use consistent crops, numbered labels, and readable captions. The layout
must not reduce the body type below the existing readable poster scale.

### Key English Copy

The shared research gap is:

> Scientific workflows span specialized programs, remote schedulers, and local
> analysis tools. Job completion alone does not prove that scientifically valid
> outputs were produced or that the correct files reached the next stage.

Ziming's key contribution is:

> We transformed ePolyScat from a collection of disconnected tools into a
> guided, inspectable workflow. Each stage preserves the researcher's original
> input, records output provenance, and exposes a verified handoff to the next
> calculation or visualization step.

The engineering decisions remain concise and scannable:

- Lossless ordered document model for reproducible ePolyScat inputs.
- Semantic output roles instead of filename-only inference.
- Resource-aware execution contracts across supported HPC systems.
- Provenance-aware continuation with researcher review before submission.

The scientific value statement is:

> Researchers can reproduce exactly what was submitted, distinguish scheduler
> artifacts from scientific results, and continue a calculation without
> manually rebuilding file dependencies.

The acceptance result is:

> Portal configuration to HPC execution to scientific proof to
> provenance-aware handoff to local visualization is operational and
> demonstrated with real runs.

### Concise Validation Block

Validation remains high-level rather than reproducing a test log. Use four
headline metrics:

- `296` — Automated Checks Passed
- `3` — HPC Platforms Validated
- `2` — Scientifically Verified Runs
- `4` — Operational Workflow Stages

The only supporting line is:

> Non-gRPC test coverage, HPC wrapper regressions, and the production build
> passed successfully.

Detailed job identifiers, EDCS marker counts, abnormal-ending counts, individual
scientific filenames, and branch-size statistics are omitted from the visible
validation block. They remain available as oral-defense evidence.

### Layout Revision

Contribution A becomes a balanced sequence of Research Gap, Key Contribution,
four evidence tiles, Engineering Decisions, Scientific Value, Acceptance Result,
and the concise four-metric validation block. Empty fixed-height cards are
compressed so key copy can use a larger, more visible type size.

Contribution B retains equal width and the same eight partner-editable macros.
The placeholder structure remains visually complete and does not inherit
Ziming-specific claims or metrics.
