from typing import Dict
from werkzeug.exceptions import BadRequest, NotFound, Gone, Conflict
from models.move import Move
from models.move_response import MoveResponse
from game_mechanics import GameMechanics

PLAYERS = "players"
COLUMNS = "columns"
ROWS = "rows"
STATE = "state"
DONE = "DONE"
IN_PROGRESS = "IN_PROGRESS"
PLAYER1 = "player1"
PLAYER2 = "player2"
WINNER = "winner"


class Game:
    def __init__(self, config: object):
        self._validate(config)

        self.id_: int = 0
        self.players: [str] = config[PLAYERS]
        self.columns: int = config[COLUMNS]
        self.rows: int = config[ROWS]
        self.moves: [Move] = []
        self.mechanics: GameMechanics = GameMechanics(self.columns, self.rows)
        self.board: [[int]] = self.mechanics.board
        self.turn: str = PLAYER1
        self.status: str = IN_PROGRESS
        self.winner: str = None

    def get_state(self) -> Dict[str, object]:
        state = {
            PLAYERS: self.players,
            STATE: self.status
        }

        if self.winner:
            state[WINNER] = self.winner

        return state

    def execute(self, move: Move) -> str:
        player = move.player
        self._validate_player(player)
        (column, row) = self.mechanics.drop_piece(move)
        self.moves.append(move)
        if self.mechanics.player_has_won(column, row, player):
            self.status = DONE
            self.winner = player
        self._end_players_turn(player)

        return f"{self.id_}/moves/{len(self.moves) - 1}"

    def player_quits(self, move: Move):
        player = move.player
        self._validate_player(player)
        self._validate_state()
        self.moves.append(move)
        self.players.remove(player)

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
            raise NotFound(
                f"Could not find player of id '{player}' in game '{self.id_}'")

        if (self.turn != player):
            raise Conflict(
                "Invalid move. Player '{player}' attempted a move during the turn of {self.turn}"
            )

    def _validate_state(self):
        if self.get_state()[STATE] == DONE:
            raise Gone(
                "Game has already finished. Cannot remove player from done games."
            )

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

    def _end_players_turn(self, player):
        index = self.players.index(player)
        # If we have reachd the end of our players list,
        # Then we loop back to the beginning of the players list
        # to find the current player's turn
        if not index < len(self.players) - 1:
            self.turn = self.players[0]
        else:
            # Simply point to the next player in the players list,
            # if we are not at the end
            self.turn = self.players[index + 1]
