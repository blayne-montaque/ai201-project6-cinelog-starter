"""Watchlist duplicate behavior mirrors the collection service."""

import pytest
from app import db
from models import WatchlistEntry
from services.watchlist_service import add_to_watchlist, AlreadyInWatchlistError
from tests.test_collection import app, sample_user, sample_film


def test_add_to_watchlist_duplicate_raises(app, sample_user, sample_film):
    with app.app_context():
        original = add_to_watchlist(sample_user, sample_film)
        original_id = original.id
        with pytest.raises(AlreadyInWatchlistError):
            add_to_watchlist(sample_user, sample_film)
        db.session.remove()
        entries = WatchlistEntry.query.filter_by(
            user_id=sample_user, film_id=sample_film
        ).all()
        assert len(entries) == 1
        assert entries[0].id == original_id


def test_duplicate_request_returns_conflict(app, sample_user, sample_film):
    client = app.test_client()
    url = f"/watchlist/{sample_user}/add"
    first = client.post(url, json={"film_id": sample_film})
    second = client.post(url, json={"film_id": sample_film})
    assert first.status_code == 201
    assert second.status_code == 409
    assert "already" in second.get_json()["error"]
    listing = client.get(f"/watchlist/{sample_user}")
    assert listing.status_code == 200
    assert [film["id"] for film in listing.get_json()] == [sample_film]
