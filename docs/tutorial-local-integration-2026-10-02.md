# Local tutorial integration — 2026-10-02

Base: fc8ff106f13bb8ef3f4a4a95ec101bddc0440630.
Branch: local/tutorial-integration-fc8ff10.
Source: uncommitted tutorial worker at /Users/fengxiao/orca/workspaces/epolyscat-django-app/epolyscat-tutorials-figma-worker, based on 373601b4f0da96d912d88f6de168c7462c5468a5.

## Changes

Imported five packaged manual cases (Test 01/04/08/12/36), shared tutorial synchronization, stable unique keys and migration 0028, safe packaged file reads, read-only tutorial presentation, and two-file clone hydration with Convert rewriting and retry/save gating.

Resolved six three-way conflict regions in CreateRun.vue by preserving application discovery, source application identity and tutorial hydration guards together. Resolved three regions in Runs.vue by preserving current portal-list-table styling, experiment filtering/title, tutorial columns, and failed tutorial-load isolation. Tutorial UI tests live in their own suite rather than restoring the removed monolithic frontend suite.

The source worker, its database, other checkouts, remote registrations, and HPC jobs were not changed. Dependencies were copied locally from the existing installation, not installed or shared via a writable symlink.

## Verification

- Final isolated complete suite: 359 passed, 1 skipped in 30.45s.
- Tests configure SQLite :memory: before Django setup; no user/production database is used.
- Added regression coverage for all current tutorial mutation endpoints, migration deduplication/repeated execution and preservation of user-owned rows, and combined application/hydration guards.
- Production npm build completed successfully. Existing lint warnings and bundle-size warnings remain; all files named in lint warnings are byte-identical to the base.
- makemigrations --check --dry-run reports no changes; the sole migration leaf is 0028_tutorial_keys.
- Code diff whitespace check passed. The full staged check reports one trailing space in imported test04.g09.inp (line 6); the original scientific fixture is deliberately preserved byte-for-byte.
- Logs and worker hashes: ../verification/tests-final.log, build.log, schema-check.log, source-worker-sha256.json (relative to the worktree root these are outside this repository).

No browser acceptance session, deployment, production migration, scientific recalculation, or remote cluster execution was performed. Figma editable reconstruction remains pending as described in the original handoff; this integration does not claim to finish it.

## Utility follow-up

The supplied Utility branch ref names ebd0401392798cba3641f38b56b69aaa893ffea5. Git could not recognize that directory as a repository in this runtime, so the cross-check compares its actual source files against the shared fc8ff10 base, not a verified clean Git HEAD.

Read-only three-way comparison: CreateRun.vue has two conflict regions; epolyscat-service.js and views.py auto-merge; test_new_run_ui_contracts.py is unchanged by tutorial and accepts Utility's additions. No Utility changes were imported here.

Suggested future order: finish tutorial first, apply Utility onto it in another local integration worktree, resolve the two guards, and run both full suites and build. Preserve tutorialCloneBlocked in both save and submit. Save-only may accept Utility's canSaveExistingMoldenDraft exception; submit must still require applicationSelectionAvailable. For example:

- Save disabled: processing || tutorialCloneBlocked || (!applicationSelectionAvailable && !canSaveExistingMoldenDraft).
- onSave: return when tutorialCloneBlocked || (!applicationSelectionAvailable && (submit || !canSaveExistingMoldenDraft)).

Retain Utility's backend draft-versus-submit checks and repeat owner/permissions, missing application, existing draft, double-input hydration and Convert regression tests after the combined merge. No GitHub writes are part of this work.
