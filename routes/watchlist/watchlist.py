"""
routes/watchlist.py — CineLog (feature/watchlist branch)

Endpoints for the watchlist feature.
"""

from flask import Blueprint, jsonify, request
from uuid import UUID
from services.watchlist_service import (
    add_to_watchlist,
    get_watchlist,
    AlreadyInWatchlistError,
    remove_from_watchlist,
    NotInWatchlistError,
)
from services.collection_service import FilmNotFoundError

watchlist_bp = Blueprint("watchlist", __name__)


def _parse_film_id(data):
    """Validate the post-refactor API contract and normalize UUID spelling."""
    if not isinstance(data, dict) or "film_id" not in data:
        raise ValueError("film_id is required")
    if not isinstance(data["film_id"], str):
        raise ValueError("film_id must be a UUID string")
    try:
        return str(UUID(data["film_id"]))
    except ValueError:
        raise ValueError("film_id must be a UUID string") from None


@watchlist_bp.route("/<user_id>", methods=["GET"])
def view_watchlist(user_id):
    """GET /watchlist/<user_id> — Return the user's watchlist."""
    films = get_watchlist(user_id)
    return jsonify(films)


@watchlist_bp.route("/<user_id>/add", methods=["POST"])
def add_film(user_id):
    """
    POST /watchlist/<user_id>/add

    Body: { "film_id": "<uuid>" }
    """
    data = request.get_json()
    try:
        film_id = _parse_film_id(data)
        entry = add_to_watchlist(user_id=user_id, film_id=film_id)
        return jsonify(entry.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except FilmNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except AlreadyInWatchlistError as e:
        return jsonify({"error": str(e)}), 409


@watchlist_bp.route("/<user_id>/remove", methods=["DELETE"])
def remove_film(user_id):
    """DELETE /watchlist/<user_id>/remove with body {"film_id": "<uuid>"}."""
    data = request.get_json()
    try:
        film_id = _parse_film_id(data)
        remove_from_watchlist(user_id=user_id, film_id=film_id)
        return jsonify({"message": "Removed from watchlist"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except NotInWatchlistError as e:
        return jsonify({"error": str(e)}), 404
