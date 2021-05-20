import json
from werkzeug.exceptions import BadRequest, NotFound
from flask import Flask, request, jsonify
from game import Game
from dashboard import Dashboard
from game_options import GameOptions

app = Flask(__name__)

dashboard = Dashboard()


@app.errorhandler(BadRequest)
def handle_bad_request(err):
    return f"Malformed request. {err.description}", 400


@app.errorhandler(NotFound)
def handle_not_found(err):
    return f"Not found. {err.description}", 404


@app.route("/drop_token/<game_id>/moves/<int:move_number>", methods=["GET"])
def get_move(game_id, move_number):
    return dashboard.get_move(game_id, move_number), 200


@app.route("/drop_token/<game_id>/moves", methods=["GET"])
def get_moves(game_id):
    return dashboard.get_moves(game_id, request.args), 200


@app.route("/drop_token/<game_id>/<player_id>", methods=["POST"])
def post_move(game_id, player_id):
    return dashboard.post_move(request.data, game_id, player_id), 200


@app.route("/drop_token/<game_id>/<player_id>", methods=["DELETE"])
def player_quits(game_id, player_id):
    dashboard.player_quits(game_id, player_id)
    return "OK. Player successfully quit.", 202


@app.route("/drop_token/<game_id>")
def get_state(game_id):
    return dashboard.get_game_state(game_id), 200


@app.route("/drop_token", methods=["GET", "POST"])
def get_games():
    if request.method == "POST":
        return dashboard.create_game(request.data), 200
    else:
        return dashboard.get_games(), 200


@app.route("/")
def hello_world():
    return "<h1>Drop Token 98point6</h1"


if __name__ == "__main__":
    app.run(debug=True)
