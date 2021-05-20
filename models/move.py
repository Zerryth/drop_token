from typing import Dict, Union
from werkzeug.exceptions import BadRequest

COLUMN = "column"
PLAYER = "player"
TYPE = "type"
MOVE = "MOVE"
MoveAsDict = Dict[str, Union[str, int]]


class Move:
    def __init__(self, player: str, type_: str, column: int = None):
        self._validate(column, player, type_)

        self.type = type_
        self.player = player
        self.column = column

    def as_dict(self) -> MoveAsDict:
        return {
            TYPE: self.type,
            PLAYER: self.player,
            COLUMN: self.column
        }

    def _validate(self, column: int, player: str, type_: str):
        if type_ == MOVE and type(column) != int:
            raise BadRequest("Move failed: missing or invalid 'column'")
