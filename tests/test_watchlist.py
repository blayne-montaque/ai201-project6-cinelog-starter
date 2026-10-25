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


def test_watchlist_defaults_to_private_preference(app, sample_user, sample_film):
    client = app.test_client()
    response = client.post(f"/watchlist/{sample_user}/add", json={"film_id": sample_film})
    assert response.status_code == 201
    assert response.get_json()["public"] is False
    with app.app_context():
        db.session.remove()
        stored = WatchlistEntry.query.filter_by(user_id=sample_user).one()
        assert stored.public is False
    assert client.get(f"/watchlist/{sample_user}").get_json()[0]["public"] is False
