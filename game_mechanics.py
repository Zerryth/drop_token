import numpy as np
from werkzeug.exceptions import BadRequest
from models.move import Move

EMPTY_SPACE = 0
PLAYER1 = 1
PLAYER2 = 2
WINNING_CONNECTION = 4
AT_LEAST_4TH_ROW = WINNING_CONNECTION - 1
QUIT = "QUIT"


class GameMechanics:
    def __init__(self, columns: int = 4, rows: int = 4):
        self.columns: int = columns
        self.rows: int = rows
        self.board: [[int]] = [
            [0 for c in range(self.columns)] for r in range(self.rows)
        ]
        self.game_over: bool = False
        self.turn: int = 0

    def play_console_version(self):
        while not self.game_over:
            if self._is_player1_turn(self.turn):
                column = int(
                    input(f"Player 1 make your selection (0 - {self.columns})")
                )
                self._ensure_is_valid_location(column)
                row = self._get_next_open_row(column)

                self.drop_piece2(column, row, PLAYER1)
                self._check_for_winner2(column, row, PLAYER1)

            else:
                column = int(
                    input(f"Player 2 make your selection (0 - {self.columns})")
                )
                self._ensure_is_valid_location(column)
                row = self._get_next_open_row(column)

                self.drop_piece2(column, row, PLAYER2)
                self._check_for_winner2(column, row, PLAYER2)

            self.turn += 1
            self.print_board()

    def drop_piece2(self, column, row, piece):
        self.board[row][column] = piece

    def drop_piece(self, move: Move):
        piece = self._get_piece_from_player_id(move.player)
        column = move.column
        row = self._get_next_open_row(column)
        self.board[row][column] = piece
        return (column, row)

    def player_has_won(self, column, row, player) -> bool:
        piece = self._get_piece_from_player_id(player)
        if self.is_winning_move(column, row, piece):
            self.game_over = True
            return True

        return False

    def _check_for_winner2(self, column, row, player):
        if self.is_winning_move(column, row, player):
            print(f"Player {player} Wins!!!")
            self.game_over = True

    def _is_player1_turn(self, turn_count: int) -> bool:
        return turn_count % 2 == 0

    def _ensure_is_valid_location(self, column):
        if not column < self.columns:
            raise ValueError

        return self.board[len(self.board) - 1][column] == 0

    def _get_next_open_row(self, column):
        for row in range(self.rows):
            try:
                if self.board[row][column] == EMPTY_SPACE:
                    return row
            except IndexError:
                raise BadRequest(
                    "Invalid column. Cannot move to column {column}")

    def print_board(self):
        print(np.flip(self.board, 0))

    def is_winning_move(self, column, row, piece):
        if self._has_horizontal_win(column, row, piece):
            return True

        if self._has_vertical_win(column, row, piece):
            return True

        if self._has_diagonal_win(column, row, piece):
            return True

        return False

    def _has_horizontal_win(self, column, row, piece):
        count = 1

        count += self._count_matching_pieces_right(column, row, piece)
        if (count >= WINNING_CONNECTION):
            return True

        count += self._count_matching_pieces_left(column, row, piece)

        return count >= WINNING_CONNECTION

    def _has_vertical_win(self, column: int, row: int, piece: int) -> bool:
        if not row >= AT_LEAST_4TH_ROW:
            return False

        count = 1
        count += self._count_matching_pieces_below(column, row, piece)

        return count >= WINNING_CONNECTION

    def _has_diagonal_win(self, column: int, row: int, piece: int) -> bool:
        count = 1

        count += self._count_matching_pieces_to_lower_left(column, row, piece)
        if (count >= WINNING_CONNECTION):
            return True

        count += self._count_matching_pieces_to_upper_right(column, row, piece)
        if (count >= WINNING_CONNECTION):
            return True

        count += self._count_matching_pieces_to_lower_right(column, row, piece)
        if (count >= WINNING_CONNECTION):
            return True

        count += self._count_matching_pieces_to_upper_left(column, row, piece)

        return count >= WINNING_CONNECTION

    def _count_matching_pieces_right(self, column: int, row: int, piece: int) -> int:
        matches = 0
        offset = 1
        while (matches < WINNING_CONNECTION and self._is_valid_horizontal_position(column, offset)):
            if not (self.board[row][column + offset] == piece):
                break
            matches += 1
            offset += 1

        return matches

    def _count_matching_pieces_left(self, column: int, row: int, piece: int) -> int:
        matches = 0
        offset = -1
        while (matches < WINNING_CONNECTION and self._is_valid_horizontal_position(column, offset)):
            if not (self.board[row][column + offset] == piece):
                break
            matches += 1
            offset -= 1

        return matches

    def _count_matching_pieces_below(self, column: int, row: int, piece: int) -> int:
        matches = 0
        offset = -1
        while (matches < WINNING_CONNECTION and self._is_valid_vertical_position(row, offset)):
            if (self.board[row + offset][column] != piece):
                break
            matches += 1
            offset -= 1

        return matches

    def _count_matching_pieces_to_upper_right(self, column: int, row: int, piece: int) -> int:
        matches = 0
        offset = 1
        while (
            matches < WINNING_CONNECTION and
            self._is_valid_position(column, row, offset, offset)
        ):
            if (self.board[row + offset][column + offset] != piece):
                break
            matches += 1
            offset += 1

        return matches

    def _count_matching_pieces_to_lower_left(self, column: int, row: int, piece: int) -> int:
        matches = 0
        offset = -1
        while (
            matches < WINNING_CONNECTION and
            self._is_valid_position(column, row, offset, offset)
        ):
            if self.board[row + offset][column + offset] != piece:
                break
            matches += 1
            offset -= 1

        return matches

    def _count_matching_pieces_to_lower_right(self, column: int, row: int, piece: int) -> int:
        matches = 0
        offset = 1
        while (
            matches < WINNING_CONNECTION and
            self._is_valid_position(column, row, offset, offset * -1)
        ):
            if self.board[row - offset][column + offset] != piece:
                break
            matches += 1
            offset += 1

        return matches

    def _count_matching_pieces_to_upper_left(self, column: int, row: int, piece: int) -> int:
        matches = 0
        offset = 1
        while (matches < WINNING_CONNECTION and self._is_valid_position(column, row, offset * -1, offset)):
            if self.board[row + offset][column - offset] != piece:
                break
            matches += 1
            offset += 1

        return matches

    def _is_valid_position(self, column: int, row: int, column_offset: int, row_offset: int):
        return (
            self._is_valid_horizontal_position(column, column_offset) and
            self._is_valid_vertical_position(row, row_offset)
        )

    def _is_valid_horizontal_position(self, column: int, offset: int) -> bool:
        offset_position = column + offset
        return offset_position >= 0 and offset_position < self.columns

    def _is_valid_vertical_position(self, row: int, offset: int) -> bool:
        offset_position = row + offset
        return offset_position >= 0 and offset_position < self.rows

    def _get_piece_from_player_id(self, player):
        '''
        Determine what value player's token (piece) will be based off of player ID.
        Player ID is in format "player<number>". Example: "player1"
        '''
        if int(player[-1]) == PLAYER1:
            return PLAYER1
        else:
            return PLAYER2


if __name__ == "__main__":
    drop_token_game = GameMechanics()
    drop_token_game.play_console_version()
