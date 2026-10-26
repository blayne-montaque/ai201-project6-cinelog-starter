"""Repeatable real-HTTP demonstration; never touches the normal CineLog database."""

import argparse
from datetime import datetime
import json
from pathlib import Path
import tempfile
from threading import Thread
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from uuid import uuid4

from werkzeug.serving import make_server, WSGIRequestHandler
from app import create_app, db
from models import Film, User, WatchlistEntry

USER_ID = "11111111-1111-4111-8111-111111111111"
ALIEN_ID = "22222222-2222-4222-8222-222222222222"
ZODIAC_ID = "33333333-3333-4333-8333-333333333333"
MISSING_ID = "00000000-0000-0000-0000-000000000000"


def prepare_database(path):
    """Seed a newly chosen isolated database; callers never reuse a user's file."""
    app = create_app({"SQLALCHEMY_DATABASE_URI": f"sqlite:///{path.as_posix()}"})
    with app.app_context():
        db.session.add(User(id=USER_ID, username="recording", email="recording@example.com"))
        db.session.add_all([
            Film(id=ALIEN_ID, title="Alien", year=1979),
            Film(id=ZODIAC_ID, title="Zodiac", year=2007),
        ])
        db.session.commit()
    return app


def exercise(base_url, app=None):
    """Print responses received over TCP and assert the demonstrated behavior."""
    def request(method, path, expected, body=None):
        payload = json.dumps(body).encode() if body is not None else None
        req = Request(base_url + path, data=payload, method=method,
                      headers={"Content-Type": "application/json"})
        try:
            response = urlopen(req, timeout=5)
        except HTTPError as error:
            response = error
        with response:
            status = response.status
            raw = response.read().decode()
        # The root is intentionally HTML 404; every actual API response is JSON.
        data = json.loads(raw) if path != "/" else "No homepage (expected)"
        print(f"{method} {path} -> HTTP {status}")
        print(json.dumps(data, sort_keys=True))
        assert status == expected, (method, path, status, data)
        return data

    request("GET", "/", 404)
    films = request("GET", "/films/", 200)
    assert {film["id"] for film in films} == {ALIEN_ID, ZODIAC_ID}
    assert request("GET", f"/films/{ALIEN_ID}", 200)["id"] == ALIEN_ID
    path = f"/watchlist/{USER_ID}"
    assert request("GET", path, 200) == []
    first = request("POST", path + "/add", 201, {"film_id": ALIEN_ID})
    assert first["public"] is False
    request("POST", path + "/add", 409, {"film_id": ALIEN_ID, "public": True})
    request("POST", path + "/add", 404, {"film_id": MISSING_ID})
    request("POST", path + "/add", 400, {"film_id": 42})
    request("POST", path + "/add", 400, {"film_id": ZODIAC_ID, "public": "false"})
    assert request("POST", path + "/add", 201, {"film_id": ZODIAC_ID, "public": True})["public"] is True
    if app is not None:
        # Controlled persisted timestamps make this demo independent of clock resolution.
        with app.app_context():
            WatchlistEntry.query.filter_by(user_id=USER_ID, film_id=ALIEN_ID).one().date_added = datetime(2026, 1, 1)
            WatchlistEntry.query.filter_by(user_id=USER_ID, film_id=ZODIAC_ID).one().date_added = datetime(2026, 1, 2)
            db.session.commit()
    listing = request("GET", path, 200)
    assert [film["title"] for film in listing] == ["Zodiac", "Alien"]
    assert [film["public"] for film in listing] == [True, False]
    request("DELETE", path + "/remove", 200, {"film_id": ALIEN_ID})
    request("DELETE", path + "/remove", 404, {"film_id": ALIEN_ID})
    assert [film["id"] for film in request("GET", path, 200)] == [ZODIAC_ID]
    # An explicit False on re-add must also survive the HTTP round trip.
    assert request("POST", path + "/add", 201, {"film_id": ALIEN_ID, "public": False})["public"] is False
    request("DELETE", path + "/remove", 200, {"film_id": ALIEN_ID})
    request("DELETE", path + "/remove", 200, {"film_id": ZODIAC_ID})
    assert request("GET", path, 200) == []
    print("PASS: live HTTP add, duplicate, missing film, UUID validation, visibility, order, removal, and cleanup")
    print("Visibility is sharing metadata; this starter has no authentication or access filtering.")


class QuietRequestHandler(WSGIRequestHandler):
    def log(self, type, message, *args):
        pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare", action="store_true", help="Create a fresh recording DB and print PowerShell startup commands")
    parser.add_argument("--base-url", help="Exercise an app.py server started with a fresh --prepare database")
    args = parser.parse_args()
    if args.prepare:
        directory = Path(__file__).resolve().parent / "instance"
        directory.mkdir(exist_ok=True)
        path = directory / f"recording-{uuid4().hex}.db"
        app = prepare_database(path)
        with app.app_context():
            db.session.remove()
            db.engine.dispose()
        print("Run these PowerShell commands in this repository:")
        print(f"$env:DATABASE_URL = 'sqlite:///{path.as_posix()}'")
        print(r".\.venv\Scripts\python.exe app.py")
        print(f"Demo user UUID: {USER_ID}")
        return
    if args.base_url:
        exercise(args.base_url.rstrip("/"))
        return
    with tempfile.TemporaryDirectory(prefix="cinelog-demo-") as temporary:
        app = prepare_database(Path(temporary) / "demo.db")
        server = make_server("127.0.0.1", 0, app, request_handler=QuietRequestHandler)
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            print("CineLog: isolated live HTTP demo (fresh SQLite database)")
            exercise(f"http://127.0.0.1:{server.server_port}", app)
        finally:
            server.shutdown()
            thread.join(timeout=5)
            server.server_close()
            with app.app_context():
                db.session.remove()
                db.engine.dispose()


if __name__ == "__main__":
    main()
