from werkzeug.exceptions import BadRequest

FAILED_GAME_CREATION = "Failed to create Game. Config must have a valid attribute:"
PLAYERS = "players"
COLUMNS = "columns"
ROWS = "rows"
DONE = "DONE"
IN_PROGRESS = "IN_PROGRESS"


class Game:
    def __init__(self, config: object):
        self.validate(config)

        self.id_ = 0
        self.players = config[PLAYERS],
        self.columns = config[COLUMNS],
        self.rows = config[ROWS]

    def validate(self, config):
        if not self.has_list_of_players(config):
            raise BadRequest(
                "Game creation failed: invalid 'players' in config")

        if not self.has_valid_columns(config):
            raise BadRequest(
                "Game creation failed: 'columns' must be an integer greater than 0 in config")

        if not self.has_valid_rows(config):
            raise BadRequest(
                "Game creation failed: 'columns' must be an integer greater than 0 in config")

    def get_state(self):
        state = {
            PLAYERS: self.players,
            "state": IN_PROGRESS  # TODO remove hard-coding,
        }

    def has_list_of_players(self, config: object) -> bool:
        if (
            PLAYERS in config and
            isinstance(config[PLAYERS], list) and
            all(isinstance(name, str) for name in config[PLAYERS])
        ):
            return True

        return False

    def has_valid_columns(self, config):
        if COLUMNS in config and type(config[COLUMNS]) is int and config[COLUMNS] > 0:
            return True

        return False

    def has_valid_rows(self, config):
        if ROWS in config and type(config[ROWS]) is int and config[ROWS] > 0:
            return True

        return False

    # Note buggy behavior from  of BadRequest from werkzeug.exceptions:
    # for some reason 'description' returns None when trying to use string interpolation
    # We therefore can't use this method, however it could've saved us minor duplication
    def create_failed_game_creation_message(self, attribute):
        f"{FAILED_GAME_CREATION} {attribute}"
