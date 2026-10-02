# ePolyScat Manual Tutorial Catalog Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the current first-five packaged tutorial runs with five curated official manual sample jobs that deep-clone both runtime inputs and rewrite `Convert` paths for immediate submission.

**Architecture:** Package a small manifest-driven catalog and the selected official text artifacts inside the Django package. Keep the existing ownerless tutorial View/Run model and API, but derive metadata, file groups, and clone inputs from the manifest. Reuse the normal New Run form and add explicit clone hydration/path-rewrite validation.

**Tech Stack:** Django 3.2/DRF, Vue 2, Vuex, BootstrapVue, Python unittest/Django TestCase, source-structure frontend tests, Vue CLI.

---

### Task 1: Package and validate the five-case manual catalog

**Files:**
- Create: `epolyscat_django_app/data/epolyscat/manual_tutorials/manifest.json`
- Create: `epolyscat_django_app/data/epolyscat/manual_tutorials/test01/*`
- Create: `epolyscat_django_app/data/epolyscat/manual_tutorials/test04/*`
- Create: `epolyscat_django_app/data/epolyscat/manual_tutorials/test08/*`
- Create: `epolyscat_django_app/data/epolyscat/manual_tutorials/test12/*`
- Create: `epolyscat_django_app/data/epolyscat/manual_tutorials/test36/*`
- Modify: `epolyscat_django_app/tutorials.py`
- Test: `epolyscat_django_app/tests/test_tutorials.py`

- [ ] **Step 1: Replace the discovery test with a failing manifest test**

```python
def test_loads_curated_manual_cases_in_manifest_order(self):
    cases = tutorials.load_catalog()
    self.assertEqual([case["id"] for case in cases], [
        "test01", "test04", "test08", "test12", "test36",
    ])
    self.assertEqual(
        {case["convert_format"] for case in cases},
        {"molden", "gaussian", "gamess"},
    )
```

- [ ] **Step 2: Run the test and verify RED**

Run: `python runtests.py epolyscat_django_app.tests.test_tutorials.TutorialViewBackendTests.test_loads_curated_manual_cases_in_manifest_order`

Expected: FAIL because `load_catalog` and the manifest do not exist.

- [ ] **Step 3: Copy the approved official artifacts into the package**

For each selected case copy the `.inp`, runtime data, `.ostnd`, and quantum-chemistry generator input from `/Users/fengxiao/Amos/docs/rrlucchese-epolyscat-manual/text/`. Preserve the official basename while removing the crawler hash from the packaged filename.

- [ ] **Step 4: Add an explicit manifest**

Each entry must have this complete shape:

```json
{
  "id": "test01",
  "name": "Test 01",
  "description": "CH4 electron scattering, static exchange plus model polarization",
  "input_format": "Molpro 2015 Molden",
  "script": "test01.inp",
  "runtime_data": "test01.molden2015",
  "standard_output": "test01.ostnd",
  "reference_input": "test01.molpro.inp",
  "convert_format": "molden"
}
```

- [ ] **Step 5: Implement strict catalog loading**

Add `MANUAL_TUTORIALS_DIR`, `MANIFEST_PATH`, `EXPECTED_CASE_IDS`, and `ALLOWED_CONVERT_FORMATS`. `load_catalog()` must parse JSON, require the exact IDs/order, reject unsafe relative paths/basenames, require all four declared files, and return normalized entries with an absolute `case_path` only after validation.

- [ ] **Step 6: Run focused tests and verify GREEN**

Run: `python runtests.py epolyscat_django_app.tests.test_tutorials.TutorialViewBackendTests.test_loads_curated_manual_cases_in_manifest_order`

Expected: PASS.

### Task 2: Synchronize manifest cases into the shared tutorial View

**Files:**
- Modify: `epolyscat_django_app/tutorials.py`
- Test: `epolyscat_django_app/tests/test_tutorials.py`

- [ ] **Step 1: Write failing synchronization assertions**

Assert exact run names, descriptions, `input_format`, `convert_format`, two file-input records, and membership replacement:

```python
runs = list(tutorials.ensure_tutorial_view().runs.order_by("name"))
self.assertEqual([run.name for run in runs], [
    "Test 01", "Test 04", "Test 08", "Test 12", "Test 36",
])
for run in runs:
    self.assertEqual(
        set(run.inputs.filter(type="files").values_list("name", flat=True)),
        {"ePolyscat_Input_File", "ePolyScat_Input_Data"},
    )
    self.assertTrue(run.workflow_metadata["tutorialStandalone"])
    self.assertIn(run.workflow_metadata["tutorialConvertFormat"], {
        "molden", "gaussian", "gamess",
    })
```

- [ ] **Step 2: Run the synchronization test and verify RED**

Run: `python runtests.py epolyscat_django_app.tests.test_tutorials.TutorialViewBackendTests.test_synchronizes_one_shared_view_and_five_cloneable_runs_idempotently`

Expected: FAIL against the old harmonic-oscillator runs and one-file input model.

- [ ] **Step 3: Replace directory discovery with manifest synchronization**

Create a reusable `_sync_file_input(run, input_name, filename)` helper. Store this metadata per run:

```python
run.workflow_metadata = {
    "tutorialStandalone": True,
    "tutorialCaseId": case["id"],
    "tutorialInputFormat": case["input_format"],
    "tutorialConvertFormat": case["convert_format"],
    "tutorialRuntimeDataName": case["runtime_data"],
    "tutorialReferenceFiles": [case["reference_input"]],
    "output_files": [case["standard_output"]],
    "file_groups": [
        {"label": "Inputs", "files": [case["script"], case["runtime_data"]]},
        {"label": "Output", "files": [case["standard_output"]]},
        {"label": "Reference", "files": [case["reference_input"]]},
    ],
    "selected_file": case["script"],
}
```

- [ ] **Step 4: Preserve transactional, non-destructive membership replacement**

Identify runs by ownerless manifest filepath, synchronize exactly five, call `tutorial_view.runs.set(synchronized_runs)`, and do not delete runs no longer in membership.

- [ ] **Step 5: Run synchronization and API status tests**

Run: `python runtests.py epolyscat_django_app.tests.test_tutorials.TutorialViewBackendTests`

Expected: catalog/synchronization tests PASS; file-catalog tests may remain RED until Task 3.

### Task 3: Serve grouped Inputs, Output, and Reference files safely

**Files:**
- Modify: `epolyscat_django_app/tutorials.py`
- Modify: `epolyscat_django_app/serializers.py`
- Modify: `epolyscat_django_app/views.py`
- Modify: `epolyscat_django_app/scientific_output_service.py`
- Test: `epolyscat_django_app/tests/test_tutorials.py`

- [ ] **Step 1: Write failing file-catalog and presentation tests**

For Test 36 assert:

```python
self.assertEqual(tutorials.input_file_names(run), [
    "test36.inp", "test36.gms.dat",
])
self.assertEqual(tutorials.output_file_names(run), ["test36.ostnd"])
self.assertEqual(tutorials.reference_file_names(run), ["test36.gms.inp"])
self.assertEqual(
    serializer.data["presentation"]["file_groups"],
    [
        {"label": "Inputs", "files": ["test36.inp", "test36.gms.dat"]},
        {"label": "Output", "files": ["test36.ostnd"]},
        {"label": "Reference", "files": ["test36.gms.inp"]},
    ],
)
```

- [ ] **Step 2: Run tests and verify RED**

Run: `python runtests.py epolyscat_django_app.tests.test_tutorials.TutorialViewBackendTests.test_tutorial_file_catalogs_separate_input_output_and_reference`

Expected: FAIL because the old catalog exposes `inpc` and tRecX outputs.

- [ ] **Step 3: Implement manifest-scoped file lookup**

Resolve the case by `tutorialCaseId` and validated packaged filepath. `open_case_file()` accepts only declared direct basenames from the four manifest fields. Add input, output, and reference descriptor helpers; output/reference descriptors remain viewable but not clone inputs.

- [ ] **Step 4: Preserve manifest file groups in serialization**

In `RunSerializer.get_presentation`, use `workflow_metadata["file_groups"]` for tutorials instead of reconstructing two generic groups. Keep the existing reconstruction for ordinary runs.

- [ ] **Step 5: Run the backend tutorial suite**

Run: `python runtests.py epolyscat_django_app.tests.test_tutorials`

Expected: all catalog, permission, preview, traversal, and completed-status tests PASS except clone creation assertions introduced in Task 4.

### Task 4: Deep-clone both runtime inputs and rewrite `Convert`

**Files:**
- Modify: `epolyscat_django_app/src/utils/workflow-file-linking.js`
- Modify: `epolyscat_django_app/src/components/Pages/CreateRun.vue`
- Modify: `epolyscat_django_app/tests/test_create_run_vue_structure.py`
- Modify: `epolyscat_django_app/tests/test_tutorials.py`

- [ ] **Step 1: Write failing backend clone assertions**

Create a user clone request containing both file inputs, then assert both are stored, the clone is user-owned, and it has no tutorial view membership.

- [ ] **Step 2: Write failing frontend hydration/path assertions**

Assert that `hydrateTutorialCloneInputs` loads both inputs, reads `tutorialRuntimeDataName` and `tutorialConvertFormat`, calls the shared patcher, exposes a hydration error, and provides retry.

- [ ] **Step 3: Run focused tests and verify RED**

Run: `python runtests.py epolyscat_django_app.tests.test_tutorials epolyscat_django_app.tests.test_create_run_vue_structure`

Expected: FAIL on two-file clone and explicit GAMESS rewrite behavior.

- [ ] **Step 4: Add an explicit format override to file linking**

```javascript
export function buildEPolyScatInputDataSelectionValues(
    file,
    sourceApplicationId = "",
    convertFormat = "",
) {
  return {
    convertSource: stagedInputReference(file),
    convertFormat: convertFormat || detectedConvertFormat(file, sourceApplicationId),
  };
}
```

Keep ordinary workflow behavior unchanged when the override is empty.

- [ ] **Step 5: Hydrate and patch tutorial clones atomically in the form**

Fetch both runtime files, clear all source URIs, load the cloned script into `inpcContent`, find the runtime-data file by manifest name, derive `{convertSource, convertFormat}` with the explicit override, patch the single `Convert` command, and sync the patched script back to `ePolyscat_Input_File`.

Add `tutorialCloneHydrating` and `tutorialCloneHydrationError`. On any fetch/parse/patch failure, keep Save disabled and show a retry action that reruns hydration for the source run.

- [ ] **Step 6: Run focused tests and verify GREEN**

Run: `python runtests.py epolyscat_django_app.tests.test_tutorials epolyscat_django_app.tests.test_create_run_vue_structure`

Expected: PASS.

### Task 5: Align the Tutorials list and detail UI

**Files:**
- Modify: `epolyscat_django_app/src/components/Pages/Runs.vue`
- Modify: `epolyscat_django_app/src/components/Pages/ViewRun.vue`
- Modify: `epolyscat_django_app/src/service/epolyscat-service.js`
- Modify: `epolyscat_django_app/tests/test_create_run_vue_structure.py`

- [ ] **Step 1: Write failing UI structure assertions**

Assert tutorial context columns `Tutorial`, `Input Format`, `Status`, `Actions`, description rendering, format metadata decoding, three detail groups, and Clone-only actions.

- [ ] **Step 2: Run the frontend structure suite and verify RED**

Run: `python runtests.py epolyscat_django_app.tests.test_create_run_vue_structure`

Expected: FAIL against the fixed Run Name/Resource columns and two-group detail logic.

- [ ] **Step 3: Implement tutorial-specific columns and metadata**

Decode `tutorialInputFormat` from `workflow_metadata`. Add a `runColumns` computed property and render the calculation description beneath the tutorial name. Keep ordinary Run/View columns unchanged.

- [ ] **Step 4: Preserve the manifest's Reference group in detail**

For tutorial runs, make `resolvedFileGroups` use `presentation.file_groups` directly so Inputs, Output, and Reference remain separate. Continue merging live catalogs for ordinary runs.

- [ ] **Step 5: Run structure tests and the Vue production build**

Run: `python runtests.py epolyscat_django_app.tests.test_create_run_vue_structure`

Run: `NODE_OPTIONS=--openssl-legacy-provider npm run build`

Expected: tests PASS and build exits 0.

### Task 6: Full verification and handoff updates

**Files:**
- Modify: `docs/epolyscat-tutorials-figma-alignment.md`

- [ ] **Step 1: Update the Figma delta checklist**

Replace the harmonic-oscillator case list and old Resource column with the approved Test 01/04/08/12/36 catalog, Input Format column, three detail file groups, and two-input clone behavior. Retain the current edit-access blocker and do not claim a canvas update.

- [ ] **Step 2: Run all Django tests**

Run: `python runtests.py`

Expected: exit 0 with no failures.

- [ ] **Step 3: Run repository checks**

Run: `git diff --check`

Run: `git status --short`

Expected: no whitespace errors, no BSR changes, no commits, no pushes, and no PR artifacts.

- [ ] **Step 4: Smoke-test the local Tutorials flow**

Verify authenticated list, detail previews for all three groups, Clone hydration for one Molden and the GAMESS case, rewritten `$pt/<basename>` references, and user-owned save behavior.

No commit step is included because this task explicitly forbids commits without separate authorization.
