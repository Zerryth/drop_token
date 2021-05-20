import json
from typing import Dict, Union
from flask import jsonify, Response
# from werkzeug.datastructures import ImmutableDict
from werkzeug.exceptions import NotFound
from game import Game
from game_options import GameOptions
from models.move import Move, MoveAsDict
from models.move_response import MoveResponse

GAME_ID_PREFIX = "gameid"
COLUMN = "column"
START = "start"
UNTIL = "until"


class Dashboard:
    def __init__(self):
        self.games = []

    def get_games(self) -> Response:
        return jsonify(games=[game.id_ for game in self.games])

    def create_game(self, data: Union[str, bytes, bytearray]) -> Response:
        game: Game = json.loads(data, object_hook=lambda config: Game(config))
        game.id_ = self._create_game_id()
        self.games.append(game)

        return jsonify(gameId=game.id_)

    def post_move(self, data: bytes, game_id: str, player_id: str) -> Response:
        # TODO check if we need to use "type" prop of Move at all here
        move: Move = json.loads(
            data, object_hook=lambda d: Move(d[COLUMN], player_id)
        )
        game = self._find_game(game_id)
        move_res = game.execute(move)

        return jsonify(move=move_res)

    def get_game_state(self, game_id: str) -> object:
        game = self._find_game(game_id)

        return game.get_state()

    def get_move(self, game_id: str, move_number: int):
        game: Game = self._find_game(game_id)

        try:
            move: Move = game.moves[move_number]
            return move.as_dict()
        except IndexError:
            raise NotFound(
                f"Could not find move '{move_number}' in game '{game_id}'"
            )

    def get_moves(self, game_id: str, req_args):
        game: Game = self._find_game(game_id)
        all_moves: [MoveAsDict] = [
            move.as_dict() for move in game.moves
        ]
        moves = self._handle_optional_moves_args(all_moves, req_args)

        return jsonify(moves=moves)

    def player_quits(self, game_id: str, player_id: str):
        game: Game = self._find_game(game_id)
        game.player_quits(player_id)

    def _find_game(self, game_id: str) -> Game:
        target_game = None
        for game in self.games:
            if game.id_ == game_id:
                target_game = game
                break

        if not target_game:
            raise NotFound(
                f"Could not find game of id '{game_id}'"
            )

        return target_game

    def _create_game_id(self) -> str:
        return f"{GAME_ID_PREFIX}{len(self.games) + 1}"

    def _handle_optional_moves_args(self, moves, args):
        if not START in args and not UNTIL in args:
            return moves
        if START in args and UNTIL in args:
            start = int(args[START])
            until = int(args[UNTIL]) + 1
            return moves[start:until]
        if UNTIL in args and not START in args:
            until = int(args[UNTIL]) + 1
            return moves[:until]
        if START in args and not UNTIL in args:
            start = int(args[START])
            return moves[start:]
