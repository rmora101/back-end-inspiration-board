from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card


card_bp = Blueprint("cards", __name__, url_prefix="/cards")

def validate_item(model, item_id):
    try:
        item_id = int(item_id)
    except ValueError:
        return abort(make_response({"message": f"invalid id: {item_id}"}, 400))
    
    return model.query.get_or_404(item_id)


@card_bp.route("", methods=["GET"])
def get_all_cards():
    response = []
    cards = Card.query.all()

    for card in cards:
        response.append(card.to_dict())

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
def delete_card(card_id):
    card = validate_item(Card, card_id)

    db.session.delete(card)
    db.session.commit()

    return {"details": f'Card {card_id} successfully deleted'}, 200


@card_bp.route("/<card_id>", methods=["PATCH"])
def update_card_likes(card_id):
    card = validate_item(Card, card_id)

    request_data = request.get_json()
    card.likes_count = request_data["likes_count"]

    db.session.commit()
    return {"details": f"Card {card_id}'s likes successfully updated"}, 200