import json
from werkzeug.exceptions import BadRequest
from flask import Flask, request, jsonify
from game import Game
from dashboard import Dashboard
from game_options import GameOptions

app = Flask(__name__)

dashboard = Dashboard()


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return f"Malformed request. {e.description}", 400


@app.route("/drop_token/<game_id>/<player_id>", methods=["POST"])
def post_move(game_id, player_id):
    return "MOVE POSTED", 200


@app.route("/drop_token/<game_id>")
def get_state(game_id):
    return dashboard.get_game_state(game_id), 200


@app.route("/drop_token", methods=["GET", "POST"])
def get_games():
    if request.method == "POST":
        return dashboard.create_game(request.data), 200
    else:
        return dashboard.get_games(), 200


@app.route("/<name>")
def hello(name):
    return f"Hello, {name}!"


@app.route("/")
def hello_world():
    return "<h1>Drop Token 98point6</h1"


if __name__ == "__main__":
    app.run(debug=True)
