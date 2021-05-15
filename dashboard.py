import json
from flask import jsonify
from game import Game
from game_options import GameOptions

GAME_ID_PREFIX = "gameid"


class Dashboard:
    def __init__(self):
        self.games = []

    def create_game(self, data):
        game = json.loads(data, object_hook=lambda config: Game(config))
        game.id_ = self.create_game_id()
        self.games.append(game)

        return jsonify(gameId=game.id_)

    def add_games(self, games: [Game]):
        for game in games:
            self.games.append(game)

    def create_game_id(self):
        return f"{GAME_ID_PREFIX}{len(self.games) + 1}"

    def get_games(self):
        return jsonify(games=[game.id_ for game in self.games])
