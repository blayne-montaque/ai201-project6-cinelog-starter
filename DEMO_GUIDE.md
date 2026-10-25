# CineLog recording guide

CineLog is a REST API for logging watched films and saving future watches. This contribution completes the reviewed watchlist: consistent naming, duplicate rejection, UUID support, newest-first retrieval, explicit sharing preferences, and removal. It has no browser frontend. `public` records a preference; it does not restrict access in this unauthenticated starter.

## Fast recording path

Open PowerShell and run:

```powershell
Set-Location 'D:\Productivity\School\Howard University\Courses\Fall 2026\CSCI 485\Project 6\ai201-project6-cinelog-starter'
git branch --show-current
.\.venv\Scripts\python.exe -m pytest tests/ -v
.\.venv\Scripts\python.exe demo_watchlist.py
git --no-pager log --oneline --decorate origin/main..HEAD
git rev-list --merges origin/main..HEAD
```

The helper starts a real local HTTP server on an available port, creates a fresh temporary SQLite database with deterministic user/film IDs, prints actual responses, asserts the outcomes, shuts down, and removes only its temporary database. It needs no API key or extra dependency. It controls persisted dates to make Zodiac sort before Alien reliably. Run it again for another take; it never modifies the normal app database. Evidence from the actual run is in [demo-http.txt](artifacts/demo-http.txt).

## Run the normal app and drive it from a second terminal

For a fresh installation only:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Prepare an isolated recording database:

```powershell
.\.venv\Scripts\python.exe demo_watchlist.py --prepare
```

Copy the printed `$env:DATABASE_URL = 'sqlite:///...'` assignment into the same PowerShell window, then run the supported startup command:

```powershell
.\.venv\Scripts\python.exe app.py
```

In a second PowerShell window, change to the repository and run:

```powershell
.\.venv\Scripts\python.exe demo_watchlist.py --base-url http://127.0.0.1:5000
```

This mode also makes real requests and cleans up the demo user's watchlist, so it can be repeated. It uses the actual insertion timestamps instead of adjusting dates. [app-py-http.txt](artifacts/app-py-http.txt) records the verified app.py run. Stop app.py with Ctrl+C afterward. If port 5000 is occupied, stop your earlier demo server or use the automatic isolated helper. Old integer-schema databases are not migrated by create_all; use the fresh database printed by --prepare.

## Individual requests to narrate

With a fresh --prepare database and app.py running, use these commands in PowerShell. `curl.exe -i` displays error status codes without PowerShell turning expected 409/404 responses into exceptions. Piping JSON through stdin avoids Windows quoting problems.

```powershell
$base = 'http://127.0.0.1:5000'
$userId = '11111111-1111-4111-8111-111111111111'
$alienId = '22222222-2222-4222-8222-222222222222'
$zodiacId = '33333333-3333-4333-8333-333333333333'
curl.exe -sS "$base/films/"

# Omitted visibility defaults to false; repeat gives 409 without a second row.
@{film_id=$alienId} | ConvertTo-Json -Compress | curl.exe -sS -i -X POST "$base/watchlist/$userId/add" -H 'Content-Type: application/json' --data-binary '@-'
@{film_id=$alienId} | ConvertTo-Json -Compress | curl.exe -sS -i -X POST "$base/watchlist/$userId/add" -H 'Content-Type: application/json' --data-binary '@-'

# A real UUID absent from the catalog gives 404.
@{film_id='00000000-0000-0000-0000-000000000000'} | ConvertTo-Json -Compress | curl.exe -sS -i -X POST "$base/watchlist/$userId/add" -H 'Content-Type: application/json' --data-binary '@-'

# Explicit true persists. GET shows Zodiac before Alien, despite alphabetical order.
@{film_id=$zodiacId;public=$true} | ConvertTo-Json -Compress | curl.exe -sS -i -X POST "$base/watchlist/$userId/add" -H 'Content-Type: application/json' --data-binary '@-'
Invoke-RestMethod "$base/watchlist/$userId" | Format-Table title,id,public,date_added

# Remove, then explicitly save with false.
@{film_id=$alienId} | ConvertTo-Json -Compress | curl.exe -sS -i -X DELETE "$base/watchlist/$userId/remove" -H 'Content-Type: application/json' --data-binary '@-'
@{film_id=$alienId;public=$false} | ConvertTo-Json -Compress | curl.exe -sS -i -X POST "$base/watchlist/$userId/add" -H 'Content-Type: application/json' --data-binary '@-'
```

## Explain the rebase and show the PR

Open `pr-response.md`, Comment 6. The authentic original branch was recovered from upstream. During `git rebase upstream/main`, models.py conflicted because main changed WatchlistEntry.film_id to String(36) while the old feature added index=True to an integer column. Resolution combined the UUID type with the feature's index and retained all main UUID changes. A separate fix validates UUID API inputs. The real interactive rebase rewords the original rough message and retains the other logical changes. [Git evidence](artifacts/git-workflow.txt) records backup refs and reflog operations.

Use `git log --oneline --decorate origin/main..HEAD` and the empty `git rev-list --merges origin/main..HEAD` output. Open the [feature branch](https://github.com/blayne-montaque/ai201-project6-cinelog-starter/tree/feature/watchlist), then its Pull requests tab. Select the open watchlist PR, confirm `feature/watchlist` into this fork's `main`, and show its description plus the rendered response document and embedded history screenshot. The audit records the verified PR URL after publication.

## Approximately two-minute spoken walkthrough

“CineLog is a film-tracking REST API. This project completes an existing watchlist contribution through a six-comment code review. I recovered the authentic upstream feature branch because my fork initially contained only main. Codex performed the implementation, testing, design analysis, and Git work; the response document discloses that assistance.

First, the service now follows add_to_collection's naming and duplicate pattern. Adding Alien returns 201. Adding it again returns 409 and leaves one entry. A nonexistent film UUID returns 404, while malformed identifiers return 400.

I chose a private sharing preference by default because saving a tentative future watch should not automatically declare public intent. The endpoint accepts explicit true or false. This starter has no authentication, so the flag is metadata, not enforced privacy.

I accepted the reviewer's newest-first ordering. Zodiac was added after Alien and appears first, which makes recently saved films easier to find. Tests use fixed timestamps and check tie behavior. The removal endpoint deletes only the requested user's membership; it preserves the catalog film and other users' lists.

The real rebase hit a conflict between main's UUID column and the feature's integer column with an index. The resolution preserved UUIDs and the index. A separate UUID fix and an interactive rebase produced this conventional history, with no merge commits.

The full suite passes 34 tests, and this demonstration runs actual HTTP requests against an isolated database. The response document covers all six comments, all three stretch features, and includes the genuine terminal screenshot. The open pull request targets main within my own fork.”

## Recording checklist

1. Open this guide, the response document, and the open PR.
2. Show feature/watchlist and run the 34-test suite (one existing catalog deprecation warning is documented).
3. Run the isolated demo; narrate add, duplicate, invalid film, true/false, ordering, and removal.
4. Show the source-grounded visibility and sorting arguments.
5. Show Comment 6 and the distinct UUID fix in git log.
6. Show conventional history, zero merges, and the embedded real screenshot.
7. Show the open PR's correct fork/base/head and description.
8. Submit the feature-branch URL through the course portal; do not submit just the repository root.
