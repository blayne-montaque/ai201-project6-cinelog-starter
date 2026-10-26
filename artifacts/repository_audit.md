# Project 6 deliverable audit

Target: all required features (25 points) and all three stretch features (3 points). This audits the requirements in the supplied assignment; it does not claim an awarded grade or invent a per-item point allocation. Codex's full involvement is disclosed in pr-response.md.

| Requirement | Evidence | Result |
|---|---|---|
| Recover authentic upstream feature | [orientation.md](orientation.md); original `9eafe681140afec72b8502c8bdea36d31fd7bfe5` and `af28e3c17551c9214411d8ff0f9972fabbae4029`; backup/original-watchlist | Complete; not recreated from main |
| Orient before fetching comments | models, collection service, collection tests read first; [orientation.md](orientation.md) | Complete; source facts distinguish actual code from premature UUID docstrings |
| Six actionable comments | [review-comments.md](review-comments.md), six substantive response sections | Complete; three inline + three Conversation; three empty review records excluded |
| Comment 1 rename | services/watchlist_service.py, routes/watchlist/watchlist.py; `1c258cb`; response Comment 1 | Complete; no stale Python references |
| Comment 2 duplicates | model unique pair, service exception, JSON 409; tests/test_watchlist_duplicates.py; `1fe2094`, `394400b` | Complete; document explicitly explains add_to_collection's pair query and raised exception |
| Comment 3 missing film | tests/test_watchlist.py::test_add_to_watchlist_nonexistent_film_raises; `81c22d4` | Complete; collection fixtures and pytest.raises pattern; no rows written |
| Comment 4 visibility reasoning | response Comment 4 and PR Description; model False; visibility tests; `6f7eed3`, `117f9d5` | Complete; specific product evidence, public-default counterargument, opt-in cost, metadata-only limitation |
| Comment 5 ordering reasoning | service date_added DESC/id ASC; controlled-date test; `061b3bc`, `ccd6869` | Complete; directly addresses recent additions and alphabetical/oldest-first tradeoffs |
| Comment 6 genuine rebase | response Comment 6; [git-workflow.txt](git-workflow.txt); base `57ec3f9`; models.py conflict | Complete; String(36) plus original index preserved; 11 commits replayed without skips |
| Separate UUID fix | `ec71f5f`; request normalization and obsolete integer contract corrected; `1f8f92c` UUID tests | Complete; meaningful follow-up beyond folded model conflict |
| Stretch 1 removal | remove_from_watchlist and DELETE route; tests/test_watchlist_removal.py; `4b79651`, `d405e1b` | Complete; success, absent membership, repeat removal, user isolation, retained film |
| Stretch 2 independent test | test_remove_from_watchlist_preserves_other_user; response Stretch Features | Complete; two users share one film, removal retains the other user's exact entry |
| Stretch 3 explicit visibility | Boolean service argument and POST parsing; tests/test_watchlist_visibility.py; `bf23115`, `b1cd2b4` | Complete; true/false persisted, omission defaults False, invalid types rejected, duplicates preserve preference |
| Real interactive rebase | [interactive-rebase-todo.txt](interactive-rebase-todo.txt), [git-workflow.txt](git-workflow.txt), backup/before-interactive-rebase | Complete; 19 commits, three actual reword operations; tree before/after identical `7e8b7fe5cd7a4df338d344163ae30ff72a822a31` |
| Clean conventional history | [rewritten-history.txt](rewritten-history.txt); distinct original feature/rename/dedup/test/UUID/stretch changes | Complete; original authors retained; tests separated per CONTRIBUTING.md |
| No merge commits and correct base | git rev-list --merges origin/main..HEAD empty; merge-base ancestor check succeeds | Complete; main/origin/main/upstream/main remain `57ec3f9052b21460800d89e4929f0584c4aacc11` |
| Baseline and final tests | [baseline-tests.txt](baseline-tests.txt), [final-tests.txt](final-tests.txt) | Complete; baseline 4 passed, final 34 passed, no test failures; one pre-existing catalog Query.get deprecation warning |
| Actual HTTP verification | [demo-http.txt](demo-http.txt), [app-py-http.txt](app-py-http.txt) | Complete; actual TCP requests through helper and supported app.py startup; expected root 404 |
| HTTP demo evidence | [demo_watchlist.py](../demo_watchlist.py); `5ac2428`; manual commands in [pr-response.md](../pr-response.md) | Complete; repeatable isolated database and recorded real HTTP responses; the optional demo guide was intentionally removed |
| Repository hygiene | .gitignore checked against every required pattern; tracked file inventory | Complete; no keys, .env, databases, caches, or environments tracked; existing collection tests unchanged |
| Real embedded history screenshot | [git-history.png](git-history.png), embedded in [pr-response.md](../pr-response.md); `279b81b` | Complete; tracked actual terminal capture shows feature/watchlist and conventional history through `422b7b4`; subsequent commits are documentation-only |
| Published feature branch | [feature/watchlist](https://github.com/blayne-montaque/ai201-project6-cinelog-starter/tree/feature/watchlist); origin restricted to blayne-montaque fork | Complete; normal push created the remote branch; local branch tracks origin/feature/watchlist; main unchanged |
| OPEN same-fork PR | [PR #1](https://github.com/blayne-montaque/ai201-project6-cinelog-starter/pull/1); base main, head feature/watchlist, both in blayne-montaque/ai201-project6-cinelog-starter | Complete; verified open, non-draft, and unmerged on October 26, 2026 |

## Technical limits

- The starter is unauthenticated and does not check user existence; public=False is a stored sharing preference, not access control. Use seeded users for this assignment.
- Existing SQLite files need a migration outside this task; demo preparation always creates a fresh isolated file.
- Network cloning initially failed inside the sandbox and succeeded after permitted network escalation. This was an environment restriction, not a baseline test failure.
- No upstream PR was modified. No merge or course-portal submission is claimed.

## Publication and documentation verification

- The branch was published successfully with `git push -u origin feature/watchlist`; no force push was needed because the branch did not previously exist. Backup branches were not pushed. Main was not changed.
- [PR #1](https://github.com/blayne-montaque/ai201-project6-cinelog-starter/pull/1) is open from `feature/watchlist` into this fork's `main`. GitHub metadata confirms it is not a draft and has not been merged.
- The tracked screenshot was visually inspected: it contains the actual terminal, branch name, and conventional commit history. Its relative image link remains embedded directly in pr-response.md. The screenshot predates the later documentation-only commits, including its own addition; no replacement capture is required for this cleanup.
- All relative Markdown links and the embedded image in these two documents resolve to existing tracked files. References to the intentionally removed optional demo guide have been removed from both documents.
- This cleanup changes only pr-response.md and artifacts/repository_audit.md. The six review responses, design arguments, AI disclosure, technical evidence, and recorded test results are preserved. Application code, tests, existing commit history, and the PR's open status are unchanged.
- The PR's own description still contains links to the removed demo guide and duplicated HTML/Markdown content. Those are outside the requested two-file cleanup and remain a separate documentation issue.
- The required screenshot and open same-fork PR are complete. Course portal submission is outside this cleanup, and no awarded grade is claimed.
