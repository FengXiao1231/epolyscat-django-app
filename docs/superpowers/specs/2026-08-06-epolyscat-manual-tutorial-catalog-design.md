# ePolyScat Manual Sample Tutorials Design

## Goal

Replace the current lexically selected tRecX-style tutorial catalog with five curated sample jobs from the locally archived ePolyScat User's Manual. Each tutorial remains a shared, completed, immutable run with browsable inputs, output, and reference material. Cloning must produce a user-owned editable run that already contains every runtime input and a valid staged-file reference, so it can be submitted without asking the user to locate the original manual assets.

The deployed application must not read from `/Users/fengxiao/Amos/docs/rrlucchese-epolyscat-manual`. Required artifacts are extracted from that archive and packaged with the Django application.

## Selected cases

The catalog contains exactly these five official sample jobs, in this order:

| Tutorial | Runtime data format | Calculation coverage | Runtime data file |
| --- | --- | --- | --- |
| Test 01 | Molpro 2015 Molden | CH4 electron scattering, static exchange plus model polarization | `test01.molden2015` |
| Test 04 | Gaussian 09 | SiH4 electron scattering at multiple energies, T-matrix form | `test04.g09` |
| Test 08 | Molpro 2012 Molden | F2- static-exchange photodetachment | `test08.molden2012` |
| Test 12 | OpenMolcas Molden | N2 photoionization | `test12.molcas.scf.molden` |
| Test 36 | GAMESS | CH4 photoionization | `test36.gms.dat` |

This selection intentionally balances input-data provenance with calculation coverage. Cases that require multiple independent runtime data files, unavailable `$pd` assets, or other uncrawled dependencies are excluded from the initial catalog.

## Packaged catalog

Add a dedicated manual-sample directory under `epolyscat_django_app/data/epolyscat/`. It contains a versioned manifest and one directory per selected case. The packaged files retain their official basenames and text contents.

Each case contains three groups:

- **Inputs**: the ePolyScat `.inp` script and the single quantum-chemistry data file required by its `Convert` command.
- **Output**: the official `.ostnd` standard output.
- **Reference**: the corresponding quantum-chemistry generator input, such as `.molpro.inp`, `.g09.inp`, `.molcas.inp`, or `.gms.inp`.

Reference files and standard output are readable tutorial artifacts but are not copied into a cloned run. No official-manual source URL is stored in the manifest or rendered in the product.

The manifest is authoritative. Each entry records:

- stable case ID and display order;
- display title and concise calculation description;
- relative paths and display names for the script, runtime data, standard output, and reference input;
- the explicit `Convert` format: `molden`, `gaussian`, or `gamess`;
- the runtime data basename that must be staged and referenced by the cloned script.

Manifest validation requires exactly the five selected unique IDs, safe relative paths, safe basenames, allowed `Convert` formats, and the presence of every declared packaged file.

## Tutorial synchronization

`epolyscat_django_app/tutorials.py` loads the manifest instead of sorting tutorial directories and taking the first five. `ensure_tutorial_view()` remains the single synchronization entry point and continues to create or update one `View(type="tutorial", owner=None)` and five `Run(owner=None)` records.

For each synchronized run it stores the stable case identifier, calculation description, input-format label, explicit `Convert` format, grouped file metadata, and the packaged directory in `workflow_metadata`. It creates two file-input records:

- `ePolyscat_Input_File` containing the official `.inp` script descriptor;
- `ePolyScat_Input_Data` containing the required Gaussian, Molden, or GAMESS descriptor.

Tutorial membership is replaced with exactly the five manifest runs in manifest order. Synchronization is transactional and idempotent. Previously synchronized tutorial runs are removed from the shared view when no longer declared, but are not destructively deleted. User-owned runs and views are never modified.

Tutorial status remains local catalog state. Both displayed run status and job status are `COMPLETED`; no Airavata experiment or scheduler lookup is attempted.

## File access and presentation

All tutorial files are opened through the validated manifest and packaged root. A request must identify a synchronized tutorial run and a filename declared for that case. Only direct basenames are accepted; path traversal and undeclared files return 404.

The detail presentation exposes three file groups:

1. Inputs
2. Output
3. Reference

All files are selectable and previewable as read-only text. Missing packaged files produce an unavailable/404 state and never fall through to user storage or the external crawl directory.

## Tutorials interface

The `/tutorials` route continues to reuse the Runs list shell. In tutorial context its columns are:

- Tutorial
- Input Format
- Status
- Actions

The tutorial name links to the normal run-detail route. Its secondary text contains the concise calculation description. Input Format uses the manifest label. Status is always `COMPLETED`. Clone is the only row action. Selection, New Run, Save selection, Remove from view, Submit, Resubmit, and Delete remain unavailable.

The tutorial detail keeps the normal run-detail shell, the `Tutorials / <name>` breadcrumb, completed status treatment, grouped read-only file preview, and primary `Clone Tutorial` action. It does not show edit, submit, delete, workflow-continuation, or remote-resource affordances.

## Clone behavior

Clone is a deep copy of the two runtime inputs, not a reference to packaged files.

When `/runs/new?clonedFrom=<tutorial-run-id>` loads:

1. Fetch the tutorial run and its grouped input metadata.
2. Read the packaged `.inp` and runtime data contents through authenticated tutorial file endpoints.
3. Add the script to `ePolyscat_Input_File` and the data file to `ePolyScat_Input_Data`, clearing packaged/source URIs and marking both files as changed local content.
4. Parse the script and locate its single `Convert` command.
5. Replace the command's source with `$pt/<actual-runtime-data-basename>` and its format with the manifest's explicit `molden`, `gaussian`, or `gamess` value.
6. Validate that both required inputs are ready before allowing save.

The clone name defaults to `Clone of <tutorial name>`. Saving creates a normal current-user-owned unsubmitted run, removes all tutorial-view membership, and leaves the shared source unchanged. The cloned run then uses the ordinary edit, submit, and delete lifecycle.

## Failure handling

- Invalid manifest structure or a missing packaged artifact is a catalog/deployment error. Synchronization fails atomically and logs the affected case and field.
- A tutorial whose runtime script has no `Convert` command, more than one ambiguous `Convert` command, or a disallowed format cannot be cloned. The clone form displays a focused hydration error and does not save a partial run.
- Failure while fetching either runtime input leaves the clone form in an explicit failed state with retry available; it does not silently omit a dependency.
- Failed clone hydration does not mutate the tutorial source or create a user run.
- Object permissions remain backend-enforced: ordinary users may perform safe reads but cannot patch or delete ownerless tutorial records.

## Testing

Focused backend tests cover:

- exact manifest order: Test 01, 04, 08, 12, and 36;
- manifest validation, declared file existence, safe paths, and allowed formats;
- transactional and idempotent synchronization;
- replacement of old tutorial membership without deleting user data;
- ownerless visibility, immutable object permissions, and local `COMPLETED` status without Airavata calls;
- Inputs, Output, and Reference file catalogs and read-only previews;
- rejection of undeclared files, path traversal, and missing packaged files;
- clone payloads containing both runtime inputs;
- rewritten `Convert` commands for Molden, Gaussian, and GAMESS;
- creation of a user-owned clone with no Tutorials membership.

Focused frontend tests cover:

- the Tutorial, Input Format, Status, and Actions columns;
- calculation descriptions and input-format labels;
- tutorial-only hidden controls and Clone-only actions;
- the three detail file groups;
- two-file clone hydration, path rewriting, format preservation, readiness validation, failure messaging, and retry;
- normal lifecycle behavior after a clone is saved.

Completion gates are the focused Django suites, the complete Django suite, the Vue production build, `git diff --check`, and a scope review confirming that no BSR files, commits, pushes, or pull requests are included.

## Non-goals

- Dynamically scraping or reading the manual archive in production.
- Exposing an official-manual source link in the interface.
- Running the five official jobs during catalog synchronization.
- Supporting cases with multiple runtime dependencies or missing archived assets in this iteration.
- Copying standard output or quantum-chemistry generator inputs into cloned user runs.
- Modifying BSR functionality.
