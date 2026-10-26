"""Explicit Boolean visibility survives commit and never changes on duplicates."""

import pytest
from app import db
from models import WatchlistEntry
from services.watchlist_service import add_to_watchlist
from tests.test_collection import app, sample_user, sample_film


@pytest.mark.parametrize("public", [True, False])
def test_explicit_visibility_round_trip(app, sample_user, sample_film, public):
    client = app.test_client()
    created = client.post(f"/watchlist/{sample_user}/add", json={
        "film_id": sample_film, "public": public,
    })
    assert created.status_code == 201
    assert created.get_json()["public"] is public
    with app.app_context():
        db.session.remove()
        stored = WatchlistEntry.query.one()
        assert stored.public is public
        assert stored.user_id == sample_user
        assert stored.film_id == sample_film
    assert client.get(f"/watchlist/{sample_user}").get_json()[0]["public"] is public


@pytest.mark.parametrize("public", ["false", "true", 0, 1, None, [], {}])
def test_visibility_rejects_non_boolean(app, sample_user, sample_film, public):
    response = app.test_client().post(f"/watchlist/{sample_user}/add", json={
        "film_id": sample_film, "public": public,
    })
    assert response.status_code == 400
    assert response.get_json() == {"error": "public must be a boolean"}
    with app.app_context():
        with pytest.raises(ValueError, match="public must be a boolean"):
            add_to_watchlist(sample_user, sample_film, public=public)
        assert WatchlistEntry.query.count() == 0


def test_duplicate_cannot_change_visibility(app, sample_user, sample_film):
    client = app.test_client()
    url = f"/watchlist/{sample_user}/add"
    first = client.post(url, json={"film_id": sample_film, "public": False})
    repeated = client.post(url, json={"film_id": sample_film, "public": True})
    assert first.status_code == 201
    assert repeated.status_code == 409
    with app.app_context():
        db.session.remove()
        entry = WatchlistEntry.query.one()
        assert entry.id == first.get_json()["id"]
        assert entry.public is False
