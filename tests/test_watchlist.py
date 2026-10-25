"""Watchlist service tests using the collection suite's isolated fixtures."""

import pytest
from app import db
from models import WatchlistEntry
from services.collection_service import FilmNotFoundError
from services.watchlist_service import add_to_watchlist
from tests.test_collection import app, sample_user, sample_film


def test_add_to_watchlist_nonexistent_film_raises(app, sample_user):
    """A missing catalog film raises the domain exception before persistence."""
    with app.app_context():
        fake_film_id = "00000000-0000-0000-0000-000000000000"
        with pytest.raises(FilmNotFoundError):
            add_to_watchlist(user_id=sample_user, film_id=fake_film_id)
        assert WatchlistEntry.query.count() == 0
