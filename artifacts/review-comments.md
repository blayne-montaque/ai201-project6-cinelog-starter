# Original CodePath review evidence

Retrieved from CodePath PR #1 through the GitHub connector after source orientation. The merged timeline contained **six substantive comments** from `Aburke225` (the assignment's maintainer persona), plus three empty COMMENTED review-submission records. The empty records are not additional feedback. No upstream comment or review was modified.

1. [Rename — Files changed, services/watchlist_service.py](https://github.com/codepath/ai201-project6-cinelog-starter/pull/1#discussion_r3640497532)

   > `save_to_watchlist()` should follow the project's naming convention. Compare with `add_to_collection()` — the pattern here is `verb_to_noun`. Please rename to `add_to_watchlist()` and update all call sites.

2. [Deduplication — Files changed, services/watchlist_service.py](https://github.com/codepath/ai201-project6-cinelog-starter/pull/1#discussion_r3640497660)

   > What happens if a user calls this with a film that's already on their watchlist? The current implementation would add a duplicate entry. Please handle this case.

3. [Missing test — Conversation](https://github.com/codepath/ai201-project6-cinelog-starter/pull/1#issuecomment-5062028682)

   > Please add a test for the case where `film_id` doesn't exist in the database. Look at the existing tests in `test_collection.py` — the pattern is there.

4. [Visibility — Conversation](https://github.com/codepath/ai201-project6-cinelog-starter/pull/1#issuecomment-5062028816)

   > I notice watchlists default to `public=True`. We don't have a documented decision on default visibility for user lists. Before I can approve this, I need you to add a note to your PR description explaining your reasoning. I want to make sure we're being intentional here, not just inheriting a default.

5. [Sort order — Files changed, services/watchlist_service.py](https://github.com/codepath/ai201-project6-cinelog-starter/pull/1#discussion_r3640497943)

   > I'd prefer watchlists to default to "date added" order rather than alphabetical. Most users want to see what they added recently. I'm open to discussion if you see it differently — but let's make a decision and document it.

6. [Rebase — Conversation](https://github.com/codepath/ai201-project6-cinelog-starter/pull/1#issuecomment-5062029097)

   > A refactor merged to `main` that changed film IDs from integers to UUIDs. Your watchlist code still references integer IDs. Please rebase on `main` and update accordingly.

Upstream PR metadata confirmed the authentic feature tip `af28e3c17551c9214411d8ff0f9972fabbae4029`, base `57ec3f9052b21460800d89e4929f0584c4aacc11`, two feature commits, open state, and an unresolved merge conflict before this work.
