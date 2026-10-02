# Packaged tutorial source independence

This change follows a4cebaddad1cc3a8320ee7947f51509236fe1f34 on local/tutorial-integration-fc8ff10. Apply this delta to the unified local integration; it does not include Utility or dev configuration changes.

## Contract

Five packaged cases remain the sole source of tutorial bytes. v2 keys (`epolyscat:packaged-tutorials:v2` and `epolyscat:packaged-tutorial:v2:<case>`) identify new deployment-owned source records. Synchronization never adopts v1 or unkeyed legacy views/runs, even if their paths match the packaged catalog. Original records, file descriptors, memberships and executions remain untouched.

Canonical sources have no user owner, root, experiment, parent/source run, Airavata project, legacy input URI or user directory. Migration 0029 adds database constraints for those forward fields. Run.save no longer synthesizes a user directory for v2 sources. Normal RemoteExecution.save rejects v2 sources; synchronization also fails explicitly if an execution was inserted through a bypass such as bulk SQL (the cross-table condition is not a database CHECK constraint).

Package reads require the v2 run key and v2 view membership, manifest-declared names and matching package paths. Missing/corrupt packaged catalog returns an explicit 503 for the catalog endpoints; file endpoints return 404. Neither case falls back to personal storage. Legacy source links are retained as records but are not accepted as packaged source templates. Newly listed tutorial links target the new canonical IDs.

User clones continue to have their own owner and files in user storage. Tutorial sources never allocate that storage. Normal runs and legacy executions retain their existing behavior.

## Migration compatibility

- 0028 retains the same schema, but its legacy-assignment/reverse functions now perform no data mutation. This prevents destructive duplicate deletion on fresh installations. The migration's historical name remains unchanged.
- A database that already executed the earlier 0028 keeps its existing v1 records as-is; Django will not rerun the edited migration. Apply 0029 normally, then the first catalog sync creates the separate v2 records. Do not fake, unapply/reapply or manually rerun 0028 to obtain the new catalog.
- This patch cannot recover records deleted by the earlier 0028 implementation. Recovery, if required, must use a separately verified backup; this work has not modified any real database.
- 0029 depends on 0028. If another local change claims migration number 0029 before integration, resolve the graph explicitly and rerun migration/model checks.
- Canonical database IDs change deliberately; never repoint or rewrite old shared files, execution history or personal permissions. Update clients by using the catalog endpoint rather than retaining old tutorial IDs.
- Before dev use, verify the runtime package path and deployment ownership: an editable installation inside a personal home is not proof of project-managed deployment storage. This patch provides no new service account, credentials or permissions.

## Verification

All tests use SQLite in memory, configured before Django setup:

- Full suite: 364 passed, 1 skipped in 13.31s (../verification/lifecycle-full-tests.log).
- Actual MigrationExecutor upgrade from 0028 to 0029 preserves a synthetic v1 source's personal associations, key, membership and history, then creates separate v2 sources. Deleting the synthetic administrator leaves all five canonical sources available (../verification/lifecycle-upgrade-check.log).
- Regression verifies legacy records are byte/value unchanged by repeated migration functions and sync; synthetic administrator deletion is followed by real local API list/preview and user-owned clone checks.
- Malicious legacy URI is not passed to user_storage.open_file; missing package raises explicit catalog failure with no remote fallback.
- Database constraints reject personal ownership/root/experiment/project/URI/directory updates; execution guard preserves old histories and rejects new source executions.
- Older legacy views cannot cause the current canonical run list to be classified as non-tutorial.
- makemigrations --check --dry-run has no changes; sole leaf is 0029_packaged_tutorial_independence.

Frontend source is unchanged by this patch. The previous production build and local synthetic-browser evidence apply to a4cebad; this hardening did not repeat browser acceptance or alter any running dev service. Source worker and unified integration worktrees were not edited. No GitHub writes or external jobs occurred.
