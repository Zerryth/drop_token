from typing import Dict
from werkzeug.exceptions import BadRequest, NotFound, Gone
from models.move import Move
from models.move_response import MoveResponse

PLAYERS = "players"
COLUMNS = "columns"
ROWS = "rows"
STATE = "state"
DONE = "DONE"
IN_PROGRESS = "IN_PROGRESS"


class Game:
    def __init__(self, config: object):
        self._validate(config)

        self.id_ = 0
        self.players = config[PLAYERS]
        self.columns = config[COLUMNS]
        self.rows = config[ROWS]
        self.moves = []

    def get_state(self) -> Dict[str, object]:
        return {
            PLAYERS: self.players,
            STATE: IN_PROGRESS  # TODO remove hard-coding
            # TODO create determine winner logic
        }

    def execute(self, move: Move) -> str:
        self._validate_player(move.player)
        self.moves.append(move)

        return f"{self.id_}/moves/{len(self.moves) - 1}"

    def player_quits(self, player: str):
        if self.get_state()[STATE] == DONE:
            raise Gone(
                "Game has already finished. Cannot remove player from done games."
            )

        try:
            self.players.remove(player)
        except ValueError:
            raise NotFound(
                f"Could not find player '{player}' in game '{self.id_}'"
            )

    def _validate(self, config):
        if not self._has_list_of_players(config):
            raise BadRequest(
                "Game creation failed: missing or invalid 'players' in config"
            )

        if not self._has_valid_columns(config):
            raise BadRequest(
                "Game creation failed: 'columns' must be an integer greater than 0 in config"
            )

        if not self._has_valid_rows(config):
            raise BadRequest(
                "Game creation failed: 'columns' must be an integer greater than 0 in config"
            )

    def _validate_player(self, player: str):
        try:
            self.players.index(player)
        except ValueError:
            raise NotFound(f"Could not find player of id '{player}'")

    def _has_list_of_players(self, config: object) -> bool:
        if (
            PLAYERS in config and
            isinstance(config[PLAYERS], list) and
            all(isinstance(name, str) for name in config[PLAYERS])
        ):
            return True

        return False

    def _has_valid_columns(self, config) -> bool:
        if COLUMNS in config and type(config[COLUMNS]) is int and config[COLUMNS] > 0:
            return True

        return False

    def _has_valid_rows(self, config) -> bool:
        if ROWS in config and type(config[ROWS]) is int and config[ROWS] > 0:
            return True

        return False
