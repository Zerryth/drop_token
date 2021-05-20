from typing import Dict, Union
from werkzeug.exceptions import BadRequest

COLUMN = "column"
PLAYER = "player"
TYPE = "type"
MoveAsDict = Dict[str, Union[str, int]]


class Move:
    def __init__(self, column: int, player: str, type_: str = "MOVE"):
        self._validate(column, player)

        self.type = type_
        self.player = player
        self.column = column

    def as_dict(self) -> MoveAsDict:
        return {
            TYPE: self.type,
            PLAYER: self.player,
            COLUMN: self.column
        }

    def _validate(self, column: int, player: str):
        if type(column) != int:
            raise BadRequest("Move failed: missing or invalid 'column'")
