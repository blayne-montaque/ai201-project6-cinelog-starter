"""Real Flask requests and database round trips for the UUID watchlist API."""

from uuid import UUID
import pytest
from sqlalchemy import text
from app import db
from models import Film, WatchlistEntry
from tests.test_collection import app, sample_user, sample_film


def test_uuid_round_trip_in_api_and_database(app, sample_user, sample_film):
    assert str(UUID(sample_film)) == sample_film
    client = app.test_client()
    created = client.post(f"/watchlist/{sample_user}/add", json={"film_id": sample_film.upper()})
    assert created.status_code == 201
    assert created.get_json()["film_id"] == sample_film
    with app.app_context():
        db.session.remove()
        entry = WatchlistEntry.query.one()
        assert entry.film_id == sample_film
        assert entry.film.title == "Paddington 2"
        assert db.session.execute(text("SELECT typeof(film_id) FROM watchlist_entry")).scalar_one() == "text"
        assert Film.__table__.c.id.type.length == 36
        assert WatchlistEntry.__table__.c.film_id.type.length == 36
        assert WatchlistEntry.__table__.c.film_id.index is True
    assert client.get(f"/watchlist/{sample_user}").get_json()[0]["id"] == sample_film
    film = client.get(f"/films/{sample_film}")
    assert film.status_code == 200
    assert film.get_json()["id"] == sample_film


@pytest.mark.parametrize("body", [{}, [], ["film_id"], {"film_id": 1}, {"film_id": None}, {"film_id": []}, {"film_id": "bad-uuid"}])
def test_invalid_film_id_request_returns_400(app, sample_user, body):
    response = app.test_client().post(f"/watchlist/{sample_user}/add", json=body)
    assert response.status_code == 400
    assert "film_id" in response.get_json()["error"]
    with app.app_context():
        assert WatchlistEntry.query.count() == 0


def test_missing_uuid_film_returns_404(app, sample_user):
    response = app.test_client().post(f"/watchlist/{sample_user}/add", json={
        "film_id": "00000000-0000-0000-0000-000000000000",
    })
    assert response.status_code == 404
    assert "No film found" in response.get_json()["error"]
