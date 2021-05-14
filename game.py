from werkzeug.exceptions import BadRequest
from game_options import GameOptions

PLAYER_PREFIX = "player"


class Game:
    def __init__(self, game_id, options=GameOptions()):
        if not (game_id and options):
            raise BadRequest(
                "Malformed request -- game_id and options are required")

        if not (game_id and options):
            pass

        self.id_ = game_id
        self.players = [
            self.create_player(number_id) for number_id in range(options.player_count)
        ]
        self.columns = options.columns
        self.rows = options.rows

    def add_players(self, count):
        for number_id in range(count + 1):
            self.players.append(self.create_player(number_id))

    def create_player(self, number_id):
        return f"{PLAYER_PREFIX}{number_id}"
