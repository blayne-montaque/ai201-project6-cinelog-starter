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

[Original conversation comment](https://github.com/codepath/ai201-project6-cinelog-starter/pull/1#issuecomment-5062028816).

**Position:** Default `WatchlistEntry.public` to **False**, recording an opt-in sharing preference for each saved film. Optimize for quickly saving a possible future watch without implicitly declaring that interest public. A watchlist is provisional intent; `CollectionEntry` records already-watched films with optional ratings, and has no visibility field whose default we can legitimately inherit.

**CineLog evidence:** `add_to_watchlist()` creates an entry and `get_watchlist()` serializes its `public` field. The starter has catalog browsing and collections but no discovery feed, authenticated viewer, or visibility filtering. Public-by-default could populate a future community feed and remove a sharing step, but there is no implemented discovery benefit to balance the accidental-sharing preference it records today. The model default is False; omitted service/route settings inherit it (and the stretch parameter will make that default explicit).

**Tradeoff and counterargument:** A reviewer could reasonably prefer consistency with the starter's openly readable collections and its community positioning. Opt-in costs a conscious `public: true` choice and could reduce future social participation. That is preferable to assuming consent for every tentative film interest. An explicit Boolean supports both choices; duplicates must not silently change the original setting. Crucially, False is **metadata, not enforced privacy**: GET still returns all entries for the requested user. Real private sharing requires authentication and owner-aware authorization, outside this assignment. The PR and demo disclose this limitation instead of promising protection the code does not provide.

**Verification:** POST with omitted visibility, a new database session, and GET all report False. Targeted: **2 passed**; full suite: **8 passed**. Codex made and stress-tested this decision from the actual code at the user's request.

## Comment 5 — Sort Order

[Original inline comment](https://github.com/codepath/ai201-project6-cinelog-starter/pull/1#discussion_r3640497943).

**Position:** Accept the reviewer's preference: `get_watchlist()` orders by `WatchlistEntry.date_added.desc()` (newest first), with entry ID ascending as a deterministic tie-breaker. The existing timestamp already records when a film was saved, so no new ranking field or dependency is necessary. This also matches `get_collection()`'s newest-first behavior.

**Engagement and tradeoffs:** The reviewer is right that users often return to a film they just saved. Under the original `Film.title.asc()` query, a newly saved Zodiac appears after an old Alien, making the result of a successful add harder to find. Alphabetical order remains useful for scanning a long list by remembered title; newest-first sacrifices that stable title index. Oldest-first would surface neglected films, but would bury the recent additions the reviewer specifically wants visible. There is no priority or queue-position field supporting a meaningful custom ordering. We therefore choose recency now; title search or optional sorting can be a later product decision.

**Verification:** `test_get_watchlist_newest_first_with_stable_ties` deliberately persists Alien on January 1 and Zodiac/Moon on January 2, using controlled entry UUIDs for equal timestamps. Service and GET both return Zodiac, Moon, Alien after session reload, distinguishing newest-first from alphabetical and oldest-first. Targeted: **3 passed**; full suite: **9 passed**. Codex considered the competing use cases and authored this source-grounded decision.

## Comment 6 — Rebase and UUID Migration

Pending real rebase after the earlier review items are stable.

## Stretch Features

Pending removal, independent edge-case tests, and explicit visibility.

## PR Description

To be finalized after verification.

## Verification and Commit History

Original branch and architecture are recorded in [orientation](artifacts/orientation.md).
