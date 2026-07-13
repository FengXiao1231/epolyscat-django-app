# ePolyScat New Run / Workflow Context Notes

Date: 2026-07-07

Branch: `feature/epolyscat-workflow-run-flow`

This note records the current implementation state, the product/domain context learned from Figma, the legacy Airavata portal, BSR Django app, the professor meeting transcript, and the ePolyScat manual/site review.

## Purpose

The current goal is to make the ePolyScat Django app support the same conceptual organization as the legacy portal:

- A new run starts by choosing a top-level run type: `Modules`, `Utilities`, or `Workflows`.
- Each run type exposes a second-level application or stage choice.
- The right side shows what files are required for the selected choice.
- The actual file upload/storage selection happens in the existing `Input Files` area below.
- Workflow runs are not a single hidden batch submission. They are a staged chain where the user can inspect each step before submitting the next one.

## Background Learned

### Legacy Run Organization

From the professor meeting transcript and legacy app behavior:

- The old UI has a heading called `Run Type`.
- Run types are `Modules`, `Utilities`, and `Workflows`.
- Selecting `Modules` shows individual modules.
- Selecting `Utilities` shows utility applications.
- Selecting `Workflows` shows workflow choices/stages.
- Selecting an individual module/utility/workflow stage shows required input files on the right.
- Required files should be clickable as guidance. Clicking should scroll to the lower `Input Files` section instead of duplicating upload controls in the right column.

### Workflow Meaning

The ePolyScat workflow is understood as three staged calculations:

1. `Data Generation`
   - Application choices: `Gaussian16` or `OpenMolcas`.
   - This creates quantum chemistry / molecular orbital data used by ePolyScat.

2. `ePolyScat Run`
   - Application choice: `ePolyScat`.
   - This consumes generated data plus the ePolyScat `.inp` command/control input.

3. `Visualization & Analysis`
   - Application choices are the utility modules, for example `CnvMath`, `CnvMatLab`, `CnvLinFull`, `MoldenMerge`, `NRFPAD`, `Cube2igor`.
   - The professor also noted that analysis can have multiple possible choices.

The important product decision is that workflow steps should be chained but still user-visible:

- After submitting step 1, the user sees the step 1 View Run page.
- Clicking step 2 should open the New Run form configured for step 2.
- Step 2 inputs should be prefilled from step 1 outputs where possible.
- The user can review, replace inputs, and change resource settings before submitting.
- The same pattern applies from step 2 to step 3.

### Figma Reliability

Figma was useful for layout direction but is not fully authoritative for semantics.

Known Figma mismatches:

- `Save to` in New Run resource settings does not make sense. The professor explained save/save selection belongs to selecting completed runs into views, not to configuring a new run. It was removed from New Run.
- Figma showed both `input_data` and `input_file` in a way that made them look like duplicate `.inp` files. That appears wrong.
- Some data entry fields in Figma are placeholders, not the actual complete ePolyScat schema.
- Workflow UI should follow the professor/legacy/manual semantics even where Figma is incomplete.

### ePolyScat Input Meaning

Current understanding:

- `input_file (.inp)` is the ePolyScat control/command input file.
- It contains records such as `LMax`, `EMax`, `EngForm`, `FegeEng`, `ScatContSym`, `LMaxK`, `ScatEng`, and commands such as `Convert`, `GetBlms`, `ExpOrb`, `GetPot`, `Scat`, `TotalCrossSection`, `EDCS`.
- `input_data` is upstream molecular/scattering data consumed by ePolyScat through `Convert`, such as Gaussian or Molden/Molcas output. It is not another `.inp` command file.

The professor explained that ePolyScat input should support two views:

- File view: direct text editing of the `.inp` file.
- Table view: structured fields grouped by domain sections.

The same underlying input should stay synchronized between both views.

### Data Entry Parsing Behavior

Current intended behavior:

- Uploading or selecting a `.inp` file should populate file view with the actual file text.
- Known records should be parsed into table view.
- Unknown or unsupported lines should not be destroyed.
- Fields not found in the uploaded file should remain blank, with recommended values shown as placeholders.
- Switching between table view and file view should preserve user edits and not overwrite uploaded content with generated defaults unless the user edits table fields.

One issue discovered during testing was that files saved by macOS TextEdit as RTF can start with content like `{\rtf1...}`. That is not useful ePolyScat input. The parser now strips/handles common RTF artifacts better, but users should upload plain text `.inp` files.

### Local DB vs Airavata

The ePolyScat Django app follows the BSR Django app pattern:

- App-specific run records live in the local Django database.
- Airavata experiments/jobs are remote and are launched from those local records.
- The local run list depends on local DB rows.
- If a run is not visible in the app list, first check local run creation/API behavior, then check remote Airavata submission state.

## Implementation Summary

### Backend

Implemented workflow-aware run metadata:

- `run_mode`
- `module_application`
- `workflow_stage`
- `workflow_application`
- `utility_application`
- `workflow_metadata`
- `parent_run`
- `workflow_step_order`
- `workflow_step_status`

Added migrations:

- `0023`
- `0024`
- `0025`
- `0026`

API/serializer work includes:

- Support for module, utility, and workflow child runs.
- Parent/child workflow metadata.
- Presentation metadata for View Run.
- Dynamic target-state input/output groups.
- File grouping for selected run files.
- Plot metadata based on run/application output.
- More tolerant create/update paths for New Run forms.

Also fixed a typo in `MASTER_LINP`: `eployscat` -> `epolyscat`.

### New Run Frontend

`CreateRun.vue` was substantially reworked:

- Integrated run type selector for `Modules`, `Utilities`, and `Workflows`.
- Kept module/utility layout close to the legacy pattern.
- Workflow mode uses a three-step visual flow.
- Required files show only requirements and current selected/missing state.
- Clicking required files scrolls to the lower `Input Files` area.
- `Input Files` supports selecting from storage or local computer.
- Selected files can be removed.
- Sections for run types that do not need files are hidden where appropriate.
- Resource and queue settings are reused through a shared component.
- Removed meaningless `Save to` from New Run resource settings.

Supporting files:

- `epolyscat_django_app/src/components/RunResourceSettings.vue`
- `epolyscat_django_app/src/components/UserStorage.vue`
- `epolyscat_django_app/src/services/epolyscat-service.js`

### Data Entry Frontend

Added `epolyscat_django_app/src/utils/epolyscat-input-script.js`.

This handles:

- Parsing ePolyScat `.inp` script text.
- Generating `.inp` script text from table data.
- Keeping file view and table view synchronized.
- Categorizing records into table sections:
  - `Grid / Expansion`
  - `State Definitions`
  - `Potentials`
  - `Energies / Partial Waves`
  - `Outputs`

The old placeholder-style command sequence tab was removed because it displayed generic generated commands rather than the user's actual uploaded input.

### Workflow File Linking

Added `epolyscat_django_app/src/utils/workflow-file-linking.js`.

Current output-to-input linking rules:

Data Generation -> ePolyScat Run:

- Gaussian16:
  - Prefer `gaussian.log`, `fort.7`, `.g03`, `.g09`, `.g16`, or Gaussian `.log` outputs.
  - Fill `ePolyScat_Input_Data` / `input_data`.
  - Patch Data Entry `Convert source`.
  - Set `Convert format = gaussian`.

- OpenMolcas:
  - Prefer Molden output such as `molden.dat`, names containing `molden`, `.molden`, or `.molden.dat`.
  - Fill `ePolyScat_Input_Data` / `input_data`.
  - Patch Data Entry `Convert source`.
  - Set `Convert format = molden`.

ePolyScat Run -> Analysis:

- `CnvMath` / `CnvMatLab`: prefer `BendOrient_Output`.
- `CnvLinFull`: prefer `DumpOut` / `DumpIdy`, not generic `.dat`.
- `NRFPAD`: prefer `Cross_Section_Input_File` / `OrientNCro`.
- `Cube2igor`: prefer `Cube_Output`.
- `MoldenMerge`: prefer `molden.dat`.

### View Run Frontend

Added a real View Run route and page:

- New route: `/runs/:runId`
- Legacy route kept as `/runs/:runId/legacy`
- New run route: `/runs/new`
- Legacy new run route kept as `/runs/new/legacy`

`ViewRun.vue` now supports:

- Workflow stepper.
- Workflow/step status display.
- Dynamic input/output file sections based on run type/application.
- File selector and text preview.
- Resource display.
- Plot panel only when the run/application has plottable files.
- File dropdown filtered to actual displayable files.

Important UX direction from the user:

- In workflow View Run, clicking a future step should configure that step in New Run, not open an empty step View Run.
- A separate `Configure ePolyScat Run` link in the status panel was considered redundant and should not be needed if the stepper itself drives the flow.

## Current User Flow

### Module Run

1. Open New Run.
2. Choose `Modules`.
3. Pick `Gaussian16`, `OpenMolcas`, or `ePolyScat`.
4. Review required files on the right.
5. Click required file to scroll to `Input Files`.
6. Upload/select files.
7. Fill Data Entry if the selected module needs ePolyScat `.inp` input.
8. Select resource/queue.
9. Submit.
10. View Run shows inputs, outputs, resource, file preview, and plot only when applicable.

### Utility Run

1. Open New Run.
2. Choose `Utilities`.
3. Pick a utility.
4. Required files update for that utility.
5. Upload/select required files.
6. Select resource/queue.
7. Submit.

### Workflow Run

1. Open New Run.
2. Choose `Workflows`.
3. Step 1 is `Data Generation`; choose `Gaussian16` or `OpenMolcas`.
4. Upload/select step 1 input and submit.
5. View Run opens for step 1.
6. Click step 2 in the workflow stepper.
7. New Run opens configured for `ePolyScat Run`.
8. Step 2 inputs should be filled from step 1 outputs when real output files are available.
9. User reviews/edits inputs/resources and submits.
10. View Run opens for step 2.
11. Click step 3.
12. New Run opens configured for analysis.
13. Step 3 inputs should be filled from step 2 outputs when real output files are available.
14. User submits analysis.

If a user tries to configure or submit a later workflow step before the first incomplete prior step is done, the UI should show a modal prompt and take them to the first incomplete step.

## Testing Notes

Verified before this document:

- `python -m pytest epolyscat_django_app/tests/test_create_run_vue_structure.py epolyscat_django_app/tests/test_epolyscat_input_script.py epolyscat_django_app/tests/test_migrations.py`
  - Result: `92 passed`

- `python runtests.py epolyscat_django_app.tests.test_views`
  - Result: `48 tests OK`

- Targeted ESLint on changed frontend files passed.

Local manual testing notes:

- `127.0.0.1:8000` had another VS Code helper process listening in the user's environment.
- Do not kill that helper again without asking; the user needs it.
- Django was tested on `127.0.0.1:8001`.
- A dummy local session was used for UI access during testing. Because it had a dummy Airavata token, some Airavata resource/storage requests returned authorization errors. That is expected for the dummy session and should not happen with real login credentials.

Observed local limitation:

- The workflow child run URL opened correctly.
- Local run serializer/presentation showed expected output names.
- However, the `get_output_files` endpoint returned an empty list in the dummy/local run, so automatic step-to-step file prefill could not be fully validated with real output bytes in that session.

## Current Branch Commits

The work has been committed in functional commits:

1. `5e9102c Add workflow run metadata and APIs`
2. `d8ba5dc Implement workflow-aware new run form`
3. `71d9238 Add workflow view run routes and result UI`
4. `fd3d324 Fix documentation and local dev config`

This document is intended to be committed separately as documentation.

## Open Questions / Follow-up Items

The following points still need confirmation or deeper testing:

### Deferred Workflow Continuation Work

The first continuation entry point is intentionally limited to View Run. After
that path is validated with real completed Airavata runs, add:

- A `Continue in Workflow` action in the Runs list for eligible completed runs.
- An existing-run picker in New Workflow so a user can import a historical run
  without opening View Run first.
- A dedicated Visualization stage after Analysis, including explicit rules for
  which analysis outputs are plottable.

These entry points must reuse the backend run classifier and continuation API;
the run-type and workflow-stage mapping should not be duplicated in frontend
components.

- Exact authoritative output file names for every module/utility on production Airavata runs.
- Whether workflow parent rows should be visible in the main run list, child rows should be visible, or both with grouping.
- Whether analysis should allow multiple utility selections in one workflow step, or one analysis utility per child run.
- Whether generated default `.inp` text should ever overwrite missing table fields automatically. Current direction is no: missing parsed fields stay blank with recommended placeholders.
- How much of the ePolyScat manual should be encoded into the table schema beyond the currently parsed fields.
- Whether View Run should show scheduler/stdout/stderr files in the main output summary or only in the file selector.
- Whether the workflow stepper should show application status, Airavata experiment status, local workflow-step status, or a combined label.
- Production validation of step-to-step file linking once real Airavata output files are available through `get_output_files`.

## Files Most Relevant For Future Work

- `epolyscat_django_app/src/components/Pages/CreateRun.vue`
- `epolyscat_django_app/src/components/Pages/ViewRun.vue`
- `epolyscat_django_app/src/components/RunResourceSettings.vue`
- `epolyscat_django_app/src/components/UserStorage.vue`
- `epolyscat_django_app/src/services/epolyscat-service.js`
- `epolyscat_django_app/src/store/run-storage.store.js`
- `epolyscat_django_app/src/utils/epolyscat-input-script.js`
- `epolyscat_django_app/src/utils/workflow-file-linking.js`
- `epolyscat_django_app/models.py`
- `epolyscat_django_app/serializers.py`
- `epolyscat_django_app/views.py`
- `epolyscat_django_app/tests/test_create_run_vue_structure.py`
- `epolyscat_django_app/tests/test_epolyscat_input_script.py`
- `epolyscat_django_app/tests/test_migrations.py`
- `epolyscat_django_app/tests/test_views.py`
