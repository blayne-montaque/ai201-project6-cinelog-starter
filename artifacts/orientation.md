# Orientation before fetching the review discussion

Read `models.py`, `services/collection_service.py`, and `tests/test_collection.py` first, then the factory, shared extension, routes, watchlist service, seed script, README, and contribution guide.

- Recovery: empty Project 6 workspace; cloned the user's fork. No local changes existed. Origin initially had only main.
- Original feature tip: `af28e3c17551c9214411d8ff0f9972fabbae4029` (`fix: update film retrieval method to use db.session.get in collection and watchlist services`). Previous feature commit: `9eafe68` (`added watchlist model and endpoint fixed a bug more changes`). Base: `d77a5e8` (`feat: initial CineLog API with film collection feature`).
- Local main, origin/main, and upstream/main all point to `57ec3f9052b21460800d89e4929f0584c4aacc11` (`refactor: migrate film IDs from integer to UUID`). The feature branch was created from upstream/feature/watchlist, not main.
- `add_to_collection()` uses verb_to_noun naming. It loads Film with `db.session.get`, raises `FilmNotFoundError` when absent, queries CollectionEntry by both user_id and film_id, and raises `AlreadyInCollectionError` on a duplicate. Otherwise it adds, commits, and returns the new entry. It does not validate user existence. The model also has a composite unique constraint.
- Collection routes translate missing films to 404 and duplicates to 409. Removal queries the pair, raises `NotInCollectionError` if absent, deletes/commits, and returns True. Retrieval sorts date_added descending and returns film dictionaries with metadata.
- Tests use function-scoped pytest fixtures, an app factory, an in-memory SQLite database, application contexts, real inserts/commits, and teardown. Sample fixtures return persisted IDs. Missing-film tests use pytest.raises(FilmNotFoundError).
- The feature model has integer Film.id, CollectionEntry.film_id, and WatchlistEntry.film_id (indexed); User and entry IDs are UUID strings. Some existing docstrings/tests already describe UUIDs. Main changes all three film columns to String(36). Source, rather than those premature docstrings, determines current behavior.
- The recovered watchlist inserts without duplicate protection, defaults public=True at the model, sorts alphabetically through a Film join, and exposes GET/POST routes. Its POST lacks the collection route's exception translation.
- This is a REST-only teaching app. There is no authentication, owner authorization, social feed, or visibility filtering. CollectionEntry has no public field. WatchlistEntry.public is per-entry metadata returned by get_watchlist(); it is not access control. The factory creates tables but cannot migrate an existing SQLite schema.
- One shared SQLAlchemy instance lives in extensions.py and is re-exported by app.py. No external AI API is needed.

The user's request already contained review summaries; this source orientation was completed before retrieving the actual GitHub review comments.
