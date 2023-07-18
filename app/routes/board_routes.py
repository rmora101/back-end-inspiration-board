from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card
from .card_routes import validate_item

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

@boards_bp.route("", methods=["POST"])
def create_boards():
    request_body = request.get_json()
    new_board = Board(title=request_body["title"], 
                      owner=request_body["owner"])

    db.session.add(new_board)
    db.session.commit()

    return make_response(f"Board id:{new_board.board_id} created, 201")

@boards_bp.route("", methods=["GET"])
def get_all_boards():
    all_boards = Board.query.all()
    boards_response = []
    for board in all_boards:
        boards_response.append(board.to_dict())

    return jsonify(boards_response), 200

@boards_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id):
    board = validate_item(Board, board_id)
    
    return {"board": board.to_dict()}, 200

'''board and card routes below'''
@boards_bp.route("/<board_id>/cards", methods=["GET"])
def get_cards_from_board(board_id):
    response = []
    board = validate_item(Board, board_id)
    # board_cards = card.query.all(board_id)

    for card in board.cards:
        response.append(card.to_dict())

    return jsonify(response), 200
    # return {
    #     "id": goal.goal_id,
    #     "title": goal.title,
    #     "tasks": response
    # }, 200

@boards_bp.route("/<board_id>/cards", methods=["POST"])
def make_new_card(board_id):
    board = validate_item(Board, board_id)
    request_body = request.get_json()


    new_card = Card(
        message=request_body["message"],
        likes_count=request_body["likes_count"],
        board = board
    )

    db.session.add(new_card) 
    db.session.commit()

    return jsonify("new card created"), 200
    # return {
    #     "id": board.board_id,
    #     "card_ids": request_data["card_ids"]
    # }, 200