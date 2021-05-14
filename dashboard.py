from flask import jsonify
from game import Game
from game_options import GameOptions

GAME_PREFIX = "gameid"


class Dashboard:
    def __init__(self):
        self.games = []

    def create_game(self, options=GameOptions()):
        game = Game(self.create_game_id(), options)
        print(
            f"{game.id_}: players count {len(game.players)}, columns {game.columns}, rows {game.rows}"
        )
        self.games.append(game)
        return jsonify(gameId=game.id_)

    def add_games(self, games: [Game]):
        for game in games:
            self.games.append(game)

    def create_game_id(self):
        return f"{GAME_PREFIX}{len(self.games) + 1}"

    def get_games(self):
        return jsonify(games=[game.id_ for game in self.games])
