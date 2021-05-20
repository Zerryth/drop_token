import json
from typing import Dict, Union
from flask import jsonify
from werkzeug.exceptions import NotFound
from game import Game
from game_options import GameOptions

GAME_ID_PREFIX = "gameid"


class Dashboard:
    def __init__(self):
        self.games = []

    def create_game(self, data: Union[str, bytes, bytearray]) -> Dict[str, str]:
        game: Game = json.loads(data, object_hook=lambda config: Game(config))
        game.id_ = self.create_game_id()
        self.games.append(game)

        return jsonify(gameId=game.id_)

    def post_move(self):
        pass

    def get_game_state(self, game_id: str) -> object:
        game = self.find_game(game_id)
        if not (game):
            raise NotFound(
                "Could not find game of given id. Failed to get game state.")

        return game.get_state()

    def find_game(self, game_id: str) -> Game:
        for game in self.games:
            if game.id_ == game_id:
                return game

        return None

    def add_games(self, games: [Game]):
        for game in games:
            self.games.append(game)

    def create_game_id(self):
        return f"{GAME_ID_PREFIX}{len(self.games) + 1}"

    def get_games(self):
        return jsonify(games=[game.id_ for game in self.games])
