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
| Demo preparation | [DEMO_GUIDE.md](../DEMO_GUIDE.md), demo_watchlist.py; `5ac2428` | Complete; repeatable isolated DB, PowerShell commands, individual curl examples, narration, checklist |
| Repository hygiene | .gitignore checked against every required pattern; tracked file inventory | Complete; no keys, .env, databases, caches, or environments tracked; existing collection tests unchanged |
| Real embedded history screenshot | pr-response.md image link; intended artifacts/git-history.png | **Incomplete:** computer-use runtime blocks PowerShell; no image file exists. Exact manual capture/commit steps are in the response document. No fabricated image. |
| Published feature branch | [feature/watchlist](https://github.com/blayne-montaque/ai201-project6-cinelog-starter/tree/feature/watchlist); origin restricted to blayne-montaque fork | Complete; normal push created the remote branch; local branch tracks origin/feature/watchlist; main unchanged |
| OPEN same-fork PR | Prepared exact body in pr-response.md; intended base main, head feature/watchlist, both in blayne-montaque/ai201-project6-cinelog-starter | **Incomplete:** GitHub connector returned HTTP 403 “Resource not accessible by integration.” Browser fallback stopped because the runtime could not confidently determine the current browser URL. No PR URL exists or is claimed. |

## Limits and remaining verification

- The starter is unauthenticated and does not check user existence; public=False is a stored sharing preference, not access control. Use seeded users for this assignment.
- Existing SQLite files need a migration outside this task; demo preparation always creates a fresh isolated file.
- Network cloning initially failed inside the sandbox and succeeded after permitted network escalation. This was an environment restriction, not a baseline test failure.
- No upstream PR was modified. No merge or course-portal submission is authorized or claimed.
- Screenshot remains manual because the runtime rejected PowerShell with “product policy blocks this app.” Shell-launched consoles did not expose a capturable window.
- The branch was published successfully with `git push -u origin feature/watchlist`; no force push was needed because the branch did not previously exist. Backup branches were not pushed. Main was not changed.
- The exact PR Description was extracted from pr-response.md and passed to GitHub create_pull_request with the correct same-fork repository, head feature/watchlist, base main, and draft=False. The integration rejected creation with 403. A search found no existing open feature/watchlist-to-main PR before the attempted creation. Browser automation ended with: “could not determine the current browser URL on Windows with enough confidence to enforce policy.” No browser security control was bypassed.
- Remote Markdown content can be fetched through the GitHub connector. Visual browser rendering and image rendering could not be verified because browser automation stopped and the required screenshot is absent.

## Exact remaining steps

1. Capture the real terminal history as `artifacts/git-history.png`, following the commands in pr-response.md; commit and push the image. Update this audit's screenshot status after verifying it renders.
2. Open [the same-fork comparison](https://github.com/blayne-montaque/ai201-project6-cinelog-starter/compare/main...feature/watchlist?expand=1). Confirm base repository **blayne-montaque/ai201-project6-cinelog-starter**, base **main**, and compare **feature/watchlist**. Use title **feat: complete reviewed watchlist with UUIDs, visibility, and removal** and paste the exact PR Description section from pr-response.md. Create an OPEN PR; do not merge it. Record its actual URL here and in DEMO_GUIDE.md.
3. If GitHub CLI is installed and authenticated later, these PowerShell commands create the same PR with the prepared body (gh is not currently installed in this environment):

```powershell
.\.venv\Scripts\python.exe -c "from pathlib import Path; text=Path('pr-response.md').read_text(encoding='utf-8'); Path('../cinelog-pr-body.md').write_text(text.split('## PR Description\n',1)[1].split('\n## Verification and Commit History',1)[0].strip(), encoding='utf-8')"
gh pr create --repo blayne-montaque/ai201-project6-cinelog-starter --base main --head feature/watchlist --title 'feat: complete reviewed watchlist with UUIDs, visibility, and removal' --body-file ../cinelog-pr-body.md
```

4. Verify GitHub renders the response document and its actual image. Submit the branch URL through the course portal. The screenshot and open PR are required deliverables, so a full 28/28-ready submission is **not yet claimed**.
