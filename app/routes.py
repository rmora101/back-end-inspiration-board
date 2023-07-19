from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card


boards_bp = Blueprint("boards", __name__, url_prefix="/boards")
card_bp = Blueprint("cards", __name__, url_prefix="/cards")


'''  VALIDATE CARD AND BOARD ID FIRST '''

def validate_item(model, item_id):
    try:
        item_id = int(item_id)
    except ValueError:
        return abort(make_response({
            "details": f"Invalid ID: {item_id}"}, 400))
    
    return model.query.get_or_404(item_id)


'''  BOARD SPECIFIC ROUTES '''

@boards_bp.route("", methods=["POST"])
def create_boards():
    request_body = request.get_json()
    new_board = Board(title=request_body["title"], 
                      owner=request_body["owner"])

    db.session.add(new_board)
    db.session.commit()

    return {"details": f'New board successfully created'}, 201 


@boards_bp.route("", methods=["GET"])
def get_all_boards():
    all_boards = Board.query.all()
    boards_response = []
    for board in all_boards:
        boards_response.append(board.to_dict())

    return jsonify(boards_response), 200


@boards_bp.route("/<board_id>", methods=["DELETE"])
def delete_board(board_id):
    board = validate_item(Board, board_id)

    db.session.delete(board)
    db.session.commit()

    return {"details": f'Board {board_id} successfully deleted'}, 200 


'''  CARD SPECIFIC ROUTES '''

@boards_bp.route("/<board_id>/cards", methods=["GET"])
def get_cards_from_board(board_id):
    card_response = []
    board = validate_item(Board, board_id)

    for card in board.cards:
        card_response.append(card.to_dict())

    return jsonify(card_response), 200


@boards_bp.route("/<board_id>/cards", methods=["POST"])
def make_new_card(board_id):
    board = validate_item(Board, board_id)
    request_body = request.get_json()

    new_card = Card(message=request_body["message"],
                    board=board)

    db.session.add(new_card) 
    db.session.commit()

    return {"details": f'New card successfully created'}, 200 


@card_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = validate_item(Card, card_id)

    db.session.delete(card)
    db.session.commit()

    return {"details": f"Card {card_id} successfully deleted"}, 200


@card_bp.route("/<card_id>", methods=["PATCH"])
def update_card_likes(card_id):
    card = validate_item(Card, card_id)

    request_data = request.get_json()
    card.likes_count = request_data["likes_count"]

    db.session.commit()

    return {"details": f"Card {card_id}'s likes successfully updated"}, 200