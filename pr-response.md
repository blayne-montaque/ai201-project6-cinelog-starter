# PR Response Doc — CineLog Watchlist Feature

## AI Usage

Codex is carrying out the implementation, review analysis, design reasoning, tests, Git operations, and documentation at the user's request. This document will report the completed work and actual evidence; it does not claim independent human authorship.

## Comment 1 — Rename

[Original inline comment](https://github.com/codepath/ai201-project6-cinelog-starter/pull/1#discussion_r3640497532).

**What I did:** Renamed `save_to_watchlist()` to `add_to_watchlist()` in `services/watchlist_service.py`, following `add_to_collection()` and the contribution guide's verb_to_noun convention. Updated the import and POST handler call in `routes/watchlist/watchlist.py`; behavior is unchanged.

**How I verified:** Project-wide `rg -n 'save_to_watchlist' --glob '*.py' .` returned no references. Importing the renamed service and constructing an isolated Flask app successfully registered the watchlist routes. Full suite: **4 passed**.

## Comment 2 — Deduplication

[Original inline comment](https://github.com/codepath/ai201-project6-cinelog-starter/pull/1#discussion_r3640497660).

**What I did:** Followed `add_to_collection()` exactly in the important behavior: after confirming the film exists, its duplicate check queries `CollectionEntry` for the same `user_id` AND `film_id`; if found, it raises `AlreadyInCollectionError` without inserting or returning an existing row. `add_to_watchlist()` now queries `WatchlistEntry` for that pair and raises `AlreadyInWatchlistError`, preserving the original entry. A matching database unique constraint prevents duplicate stored pairs. The route follows `routes/collection.py`: missing film becomes JSON 404 and an existing entry becomes JSON 409.

**How I verified:** `tests/test_watchlist_duplicates.py` checks the exception, reloads the database session, confirms one row with its original ID, and repeats real Flask POST requests (201 then 409) followed by GET. Targeted: **2 passed**; full suite: **6 passed**. Tests are committed separately per CONTRIBUTING.md.

## Comment 3 — Missing Test

[Original conversation comment](https://github.com/codepath/ai201-project6-cinelog-starter/pull/1#issuecomment-5062028682).

**What I did:** Created `tests/test_watchlist.py` with `test_add_to_watchlist_nonexistent_film_raises`, modeled on `test_add_to_collection_nonexistent_film_raises`. It reuses the collection fixtures (isolated in-memory SQLite/app context and persisted user ID), supplies the same nonexistent UUID, and uses `pytest.raises(FilmNotFoundError)`. It additionally asserts no watchlist row was written. The service's expected exception was preserved.

**How I verified:** Targeted watchlist file: **1 passed**; full suite: **7 passed**. No existing collection tests were edited.

## Comment 4 — Default Visibility

Pending source-grounded design decision.

## Comment 5 — Sort Order

Pending source-grounded design decision.

## Comment 6 — Rebase and UUID Migration

Pending real rebase after the earlier review items are stable.

## Stretch Features

Pending removal, independent edge-case tests, and explicit visibility.

## PR Description

To be finalized after verification.

## Verification and Commit History

Original branch and architecture are recorded in [orientation](artifacts/orientation.md).
