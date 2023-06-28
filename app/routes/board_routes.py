from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
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

