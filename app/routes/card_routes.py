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


@card_bp.route("", methods=["POST"])
def create_cards():
    request_body = request.get_json()
    new_card = Card(message=request_body["message"], 
                    likes_count=request_body["likes_count"])

    db.session.add(new_card)
    db.session.commit()

    return make_response(f"Card id:{new_card.card_id} created, 201")

@card_bp.route("/<card_id>", methods=["DELETE"])
def delete_cards(card_id):
    card = Card.query.get_or_404(card_id)

    db.session.delete(card)
    db.session.commit()

    return {"details": f'Card {card_id} successfully deleted'}, 200