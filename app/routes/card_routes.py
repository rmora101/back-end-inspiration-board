from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)
card_bp = Blueprint("cards", __name__, url_prefix="/cards")

@card_bp.route("", methods=["GET"])
def get_all_cards():
    response = []
    cards = Card.query.all()

    for card in cards:
        new_card = {
            "card_id": card.card_id,
            "message": card.message,
            "likes_count": card.likes_count
        }
        response.append(new_card)

    return jsonify(response), 200