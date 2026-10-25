"""Removal follows collection semantics and scopes changes to the requested user."""

import pytest
from app import db
from models import User, Film, WatchlistEntry
from services.watchlist_service import (
    add_to_watchlist, remove_from_watchlist, NotInWatchlistError,
)
from tests.test_collection import app, sample_user, sample_film


def test_remove_from_watchlist_preserves_other_user(app, sample_user, sample_film):
    with app.app_context():
        other = User(username="other", email="other@example.com")
        db.session.add(other)
        db.session.commit()
        other_id = other.id
        add_to_watchlist(sample_user, sample_film)
        other_entry_id = add_to_watchlist(other_id, sample_film).id
        assert remove_from_watchlist(sample_user, sample_film) is True
        db.session.remove()
        remaining = WatchlistEntry.query.one()
        assert remaining.id == other_entry_id
        assert remaining.user_id == other_id
        assert db.session.get(Film, sample_film) is not None


def test_remove_nonexistent_entry_raises(app, sample_user, sample_film):
    with app.app_context():
        with pytest.raises(NotInWatchlistError):
            remove_from_watchlist(sample_user, sample_film)
        assert WatchlistEntry.query.count() == 0


def test_remove_endpoint_persists_and_repeat_returns_404(app, sample_user, sample_film):
    client = app.test_client()
    body = {"film_id": sample_film}
    assert client.post(f"/watchlist/{sample_user}/add", json=body).status_code == 201
    removed = client.delete(f"/watchlist/{sample_user}/remove", json=body)
    assert removed.status_code == 200
    assert removed.get_json() == {"message": "Removed from watchlist"}
    assert client.get(f"/watchlist/{sample_user}").get_json() == []
    assert client.delete(f"/watchlist/{sample_user}/remove", json=body).status_code == 404


@pytest.mark.parametrize("body", [{}, {"film_id": 12}, {"film_id": "invalid"}])
def test_remove_rejects_invalid_id(app, sample_user, body):
    response = app.test_client().delete(f"/watchlist/{sample_user}/remove", json=body)
    assert response.status_code == 400
    assert "film_id" in response.get_json()["error"]
