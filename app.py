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
    return "Malformed request", 400


@app.route("/drop_token/<int:game_id>")
def get_state(game_id):
    return {
        "players": ["player1", "player2"],
        "state": "IN_PROGRESS",
        "game_id": f"{game_id} -- REMEMBER TO DELETE ME!",
    }


@app.route("/drop_token", methods=["GET", "POST"])
def get_games():
    if request.method == "POST":
        req_json = request.get_json()
        return dashboard.create_game(), 200
    else:
        return dashboard.get_games(), 200


@app.route("/<name>")
def hello(name):
    return f"Hello, {name}!"


@app.route("/")
def hello_world():
    # games = database["games"].append(Game())
    # games_count = len(database["games"])
    # return f"<p>database count {games_count} </p>"
    return "home"


# TODO - put all the homework APIs / routes here, even with hardcoded values
# then continue reading documentation as needed


if __name__ == "__main__":
    app.run(debug=True)
