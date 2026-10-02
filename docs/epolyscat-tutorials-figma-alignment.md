# ePolyScat Tutorials — Figma Alignment Handoff

## Shareable pointers and current status

- Figma file: [ePolyScat App — Copy](https://www.figma.com/design/77FuerqYXgB8yZnAYVEejN/ePolyScat-App--Copy-?node-id=0-1).
- Running-code reference — Tutorials list: [node `2041:2698`](https://www.figma.com/design/77FuerqYXgB8yZnAYVEejN/ePolyScat-App--Copy-?node-id=2041-2698).
- Running-code reference — Tutorial detail: [node `2041:2699`](https://www.figma.com/design/77FuerqYXgB8yZnAYVEejN/ePolyScat-App--Copy-?node-id=2041-2699).
- Running-code reference — Clone-ready New Run: [node `2042:2698`](https://www.figma.com/design/77FuerqYXgB8yZnAYVEejN/ePolyScat-App--Copy-?node-id=2042-2698).

These three nodes are 1470 × 798 captures from the locally running implementation and are the visual acceptance baseline. They are image layers, not a claim of a completed editable, layer-for-layer Figma reconstruction.

The earlier Figma Agent frames — list [`2038:2702`](https://www.figma.com/design/77FuerqYXgB8yZnAYVEejN/ePolyScat-App--Copy-?node-id=2038-2702), detail [`2038:2810`](https://www.figma.com/design/77FuerqYXgB8yZnAYVEejN/ePolyScat-App--Copy-?node-id=2038-2810), and clone [`2038:2894`](https://www.figma.com/design/77FuerqYXgB8yZnAYVEejN/ePolyScat-App--Copy-?node-id=2038-2894) — are conceptual drafts. Their shell, typography, spacing, table treatment, and form composition differ materially from the running application, so they must not be used for visual acceptance.

On 2026-08-12, Figma MCP was rechecked with the authenticated account and still reported a Starter-plan tool-call limit and a View seat. The browser Agent also reported that its daily credits were exhausted. Consequently, this pass adds truthful running-code references and a precise reconstruction checklist; it does not represent that the mismatched Agent frames were automatically repaired into editable production-parity layers.

No official manual-source URL was added to Figma or this handoff.

## Exact editable-reconstruction checklist

Use the three running-code reference nodes above as the sole visual source of truth. An editable Figma rebuild is complete only when the following deltas have been resolved:

### Shared application shell

- Reproduce the AMOS gateway header visible in the application, including its actual height, title treatment, account area, borders, and spacing.
- Reproduce the narrow dark global rail and the separate white ePolyScat navigation sidebar; do not substitute a generic single-sidebar SaaS shell.
- Match the production BentonSans typography and weights. Use the production monospace treatment for script and file previews.
- Match the production content width, whitespace, muted colors, borders, button styling, icons, and responsive wrapping rather than the Agent draft's invented tokens.

### Tutorials list

- Match the exact breadcrumb/title area, `Tutorials` heading, `Filter runs` input, and table layout shown in node `2041:2698`.
- Use the production columns `Tutorial`, `Input Format`, `Status`, and `Actions` with the same widths and alignment.
- Keep the five approved rows in this order: `Test 01`, `Test 04`, `Test 08`, `Test 12`, `Test 36`.
- Show the full production input-format values: `Molpro 2015 Molden`, `Gaussian 09`, `Molpro 2012 Molden`, `OpenMolcas Molden`, and `GAMESS`.
- Match the production `COMPLETED` status styling and file-copy Clone action icon. Do not add create, delete, submit, resubmit, or selection controls to tutorial sources.

### Tutorial detail

- Match the exact `Tutorials / Test 01` breadcrumb, `Test 01` title, module line, completed Run status, and `Clone Tutorial` button shown in node `2041:2699`.
- Reproduce the production Inputs, Output, and Reference groups and filenames, plus the tabbed read-only file preview.
- Match the actual resource/status section that continues below the first fold; do not replace it with invented remote job metadata.
- Preserve the immutable-source presentation: no edit, delete, continue, submit, or resubmit affordance.

### Clone-ready New Run

- Match the exact `Experiments / Test 01 / Clone` breadcrumb and `Clone Run` title shown in node `2042:2698`.
- Reproduce the existing production form composition: Run Type, Modules, Required Files, script editor, and the normal save actions below the first fold.
- Carry the hydrated runtime filenames and values exactly: `test01.inp`, `test01.molden2015`, required keys `input_file` and `input_data`, and `$pt/test01.molden2015` in the cloned script.
- Preserve the explicit converted-input format and the cloned values such as `LMaxK = 1`; the fields are editable because the clone belongs to the current user.
- Represent loading by disabling Save and Save & Submit, and represent failure with `Retry loading tutorial files`; these may remain compact state callouts rather than duplicate full-screen frames.

### Prototype and review

- Wire List row → Detail and `Clone Tutorial` → Clone-ready New Run.
- Compare the editable frames side by side against nodes `2041:2698`, `2041:2699`, and `2042:2698` at 100% zoom before marking alignment complete.
- Keep the conceptual Agent frames visibly labeled as outdated or move them to an archive area once edit access is available; do not silently present them as the implemented UI.

## Packaged tutorial catalog

The repository catalog uses these five sample cases, selected from the locally stored ePolyScat manual material to exercise different input producers and conversion formats:

1. `Test 01` — Molpro 2015 Molden — CH4 electron scattering, static exchange plus model polarization
2. `Test 04` — Gaussian 09 — SiH4 electron scattering at multiple energies, T-matrix form
3. `Test 08` — Molpro 2012 Molden — F2- static-exchange photodetachment
4. `Test 12` — OpenMolcas Molden — N2 photoionization
5. `Test 36` — GAMESS — CH4 photoionization using GAMESS output

Each packaged case contains its ePolyScat script, runtime quantum-chemistry input, completed `.ostnd` output, and generator/reference input. The manifest fixes display order and the explicit `molden`, `gaussian`, or `gamess` conversion format.

## Product contract implemented in code

- `GET /views/tutorials/` idempotently synchronizes one ownerless `View(type="tutorial")` and five ownerless completed tutorial runs into the Django database configured for that deployment.
- The sync uses stable unique tutorial keys, transactions, row locking, catalog validation, and canonical input reconstruction. Repeated and concurrent requests converge on one shared view and one run per case.
- Packaged files remain the source of truth; database rows store catalog/run metadata and file descriptors, while reads are constrained to declared basenames inside each packaged case directory.
- Authenticated users can read the catalog and files. Backend permissions reject ordinary mutations, destructive actions, continuation, and submission of tutorial sources.
- Clone hydration fetches the script and runtime-data bytes, rewrites the script's `Convert` source and explicit format, and populates both required New Run inputs.
- Saving produces a current-user-owned run that is editable and is not a member of the shared Tutorials view. Outputs and reference inputs are not copied into the clone.

“Database sync verified” means this behavior was exercised against the local/test database selected by Django during verification. The same code targets the configured database in a deployed environment after its migration and packaged files are deployed; no production or shared remote database was mutated as part of this work.

## Remaining access dependency

The running-code visual baseline is available now through the three node links above. A fully editable production-parity reconstruction remains pending until Figma MCP/Agent access reflects an upgraded seat or another editor completes the checklist manually; after access changes, re-authenticate the Figma integration before retrying so it no longer reports the cached Starter/View entitlement.
