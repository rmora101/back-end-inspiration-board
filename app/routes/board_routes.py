from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board

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
        new_board = {
            "board_id": board.board_id,
            "title": board.title,
            # "owner": board.owner
        }
        boards_response.append(new_board)

    return jsonify(boards_response), 200

@boards_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id):
    board = Board.query.get(board_id)

    board_data = {
            "board_id": board.board_id,
            "title": board.title
    }
    
    return jsonify(board_data), 200

