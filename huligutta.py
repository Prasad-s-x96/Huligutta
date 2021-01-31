"""
file: huligutta.py
Description: Board functionalities
"""

__author__ = "Clyde James Felix"
__email__ = "cjfelix.hawaii.edu"
__status__ = "Dev"


from typing import List, Union, Optional
import address


class Board:
    """
    Represents the game board.

    In Huligutta, there are six columns a-f, and five rows 0-4.
    In the columns a and f, rows 0 and 4 do not exist.
    The position in row 0 is shared by columns b-e.
    """

    def __init__(self):

        # the position shared by columns b-e
        self.origin = ()

        # columns a-f

        self.a = {1: (), 2: (), 3: ()}
        self.b = {0: self.origin, 1: (), 2: (), 3: (), 4: ()}
        self.c = {0: self.origin, 1: (), 2: (), 3: (), 4: ()}
        self.d = {0: self.origin, 1: (), 2: (), 3: (), 4: ()}
        self.e = {0: self.origin, 1: (), 2: (), 3: (), 4: ()}
        self.f = {1: (), 2: (), 3: ()}

        # a 2D array of positions (column-major)
        self.positions = [self.a, self.b, self.c, self.d, self.e, self.f]

        # the number of captured goats
        self.num_captured = 0

        # the number of moves made
        self.num_moves = 0

        # if True, then 15 goats have been placed at one point
        self.is_all_goats_placed = False

        self.clear()

    def clear(self):
        """
        Reset the board.
        """
        self.positions = {}
        for let in address.LETTERS:  # iterate through columns
            self.positions[let] = {}

            for num in address.NUMBERS:  # iterate through rows
                addr = let + num
                # check if this position ID is valid
                if address.is_valid(addr):
                    if num == 0:
                        pos = Position(self, "b0")
                    else:
                        pos = Position(self, addr)

                    self.positions[let][int(num)] = pos

        # also reset the number of captured pieces
        self.num_captured = 0
        self.num_moves = 0
        self.is_all_goats_placed = False

        # print("the board has been cleared")

    def print_board(self):
        """
        Print the board.
        """
        a, b, c, d, e, f = self.positions.values()
        num_tigers, num_goats = self.num_pieces()

        print(f"\t*\t*\t{ b[0] }\t*\t*\t")
        print(f"{ a[1] }\t{ b[1] }\t{ c[1] }\t\t{ d[1] }\t{ e[1] }\t{ f[1] }")
        print(f"{ a[2] }\t{ b[2] }\t{ c[2] }\t\t{ d[2] }\t{ e[2] }\t{ f[2] }")
        print(f"{ a[3] }\t{ b[3] }\t{ c[3] }\t\t{ d[3] }\t{ e[3] }\t{ f[3] }")
        print(f"\t{ b[4] }\t{ c[4] }\t\t{ d[4] }\t{ e[4] }")

        print(f"tigers: {num_tigers}, goats: {num_goats}")
        print(f"captured goats: {self.num_captured}")

    def num_pieces(self) -> tuple:
        """Get the number of Tigers and Goats."""

        num_tigers, num_goats = 0, 0

        for col in self.positions.values():
            for pos in col.values():
                if type(pos) is tuple:
                    continue
                if isinstance(pos.piece, Tiger):
                    num_tigers += 1
                if isinstance(pos.piece, Goat):
                    num_goats += 1

        return num_tigers, num_goats

    def get_pos(self, addr: str) -> "Position":
        """Get a Position by its address."""

        # i, j = _address_to_indices(addr)
        return self.positions[addr[0]][int(addr[1])]

    def get_all_positions(self) -> List["Position"]:
        """Get a flattened list of board positions.

        For a 2D list of positions, use self.position.
        """
        flat_positions = [
            j for i in self.positions.values() for j in i.values()
        ]
        # filter out non-positions
        flat_positions = [
            pos for pos in flat_positions if type(pos) is Position
        ]
        return flat_positions

    def get_all_goat_positions(self) -> List["Position"]:
        return [pos for pos in self.get_all_positions() if pos.is_goat()]

    def get_all_tiger_positions(self) -> List["Position"]:
        return [pos for pos in self.get_all_positions() if pos.is_tiger()]

    def get_all_empty_positions(self) -> List["Position"]:
        return [pos for pos in self.get_all_positions() if pos.is_empty()]

    def get_all_addresses(self) -> List[str]:
        return address.possible_pos

    def get_piece(self, addr: str) -> Optional["Piece"]:
        """Get the Piece at a position.

        If there is no piece at the given position, then None
        is returned.
        """
        piece = self.get_pos(addr).piece
        if isinstance(piece, Piece):
            return piece
        else:
            return None

    def get_tiger_possible_moves(self) -> List:
        """
        Get all the possible moves the tigers can make.

        Does not include placing new tigers.

        Moves are returned as a list of tuples, where
        each tuple has the starting address and end address.
        """
        moves = []
        for pos in self.get_all_positions():
            if pos.is_tiger():
                addr_from = pos.address
                for addr_to in pos.piece.get_valid_moves():
                    moves.append((addr_from, addr_to))

        return moves

    def get_tiger_capturing_moves(self) -> List[tuple]:
        """
        Get all the capturing moves the tigers can make.

        Returns a list of tuples of tiger landing positions and goat positions.
        """
        tuples: List[tuple] = []
        for pos in self.get_all_tiger_positions():
            for landing_pos, goat_pos in pos.piece._get_capturing_positions():
                tuples.append((landing_pos, goat_pos))

        return tuples

    def get_goat_possible_moves(self) -> List:
        """
        Get all the possible moves the tigers can make.

        Does not include placing new tigers.

        Moves are returned as a list of tuples, where
        each tuple has the starting address and end address.
        """
        moves = []
        for pos in self.get_all_positions():
            if pos.is_goat():
                addr_from = pos.address
                for addr_to in pos.piece.get_valid_moves():
                    moves.append((addr_from, addr_to))

        return moves

    def is_pos_safe(self, addr: str) -> bool:
        """Checks if a goat in this position could be captured."""
        for tiger_pos in self.get_all_tiger_positions():
            if tiger_pos.piece.can_capture_pos(addr):
                return False

        return True

    def is_pos_blocking(self, addr: str) -> bool:
        """Checks if a goat in this position blocks the movement
        of a tiger."""
        for tiger_pos in self.get_all_tiger_positions():
            if tiger_pos.is_adjacent(self.get_pos(addr)):
                return True

        return False

    def place_tiger(self, addr: str):
        """Place a Tiger at the position by its address."""
        self.get_pos(addr).place_tiger()

    def place_goat(self, addr: str):
        """Place a Goat at the position by its address."""
        self.get_pos(addr).place_goat()
        if len(self.get_all_goat_positions()) >= 15:
            self.is_all_goats_placed = True

    def clear_pos(self, addr: str):
        """Clear the position by its address."""
        self.get_pos(addr).clear()

    def move_piece(self, addr_from: str, addr_to: str) -> Optional[str]:
        """Move a piece between two positions by its address.
        Returns the notation of the move if the move was successful."""

        pos_from = self.get_pos(addr_from)
        pos_to = self.get_pos(addr_to)
        piece = pos_from.piece

        if isinstance(piece, Piece):
            res = piece.move(pos_to)
            # print(f"moved {piece} from {addr_from} to {addr_to}")
            if res:
                self.num_moves += 1

            return res

        return None


class Position:
    """
    Represents a position on the board, identified
    with a letter and number i.e. "a1".

    A position can contain either empty space, a Tiger, or a Goat.
    """

    def __init__(self, board: Board, addr: str):

        # a reference to the board
        self.board = board

        # the position address
        self.address = addr

        # the piece currently in this position
        self.piece: Union[tuple, Piece] = ()

        try:
            assert address.is_valid(self.address) is True

        except AssertionError as e:
            print("Tried initializing position with invalid address")
            raise e

    def is_empty(self) -> bool:
        return self.piece == ()

    def is_goat(self) -> bool:
        return type(self.piece) is Goat

    def is_tiger(self) -> bool:
        return type(self.piece) is Tiger

    def set_piece(self, piece: Union[tuple, "Piece"]):
        """Place a piece into this position."""
        self.piece = piece

    def clear(self):
        """Delete any piece from this position."""
        # FIXME: have None represent an empty piece instead?
        self.set_piece(())

    def place_tiger(self):
        self.set_piece(Tiger(self.board, self))
        # print(f"a tiger has been placed at {self.address}")

    def place_goat(self):
        self.set_piece(Goat(self.board, self))
        # print(f"a goat has been placed at {self.address}")

    def get_adjacent_positions(self) -> List["Position"]:
        adjacent_addrs = address.get_adjacent_addrs(self.address)
        return [self.board.get_pos(addr) for addr in adjacent_addrs]

    def is_adjacent(self, pos_to: "Position") -> bool:
        """
        Checks if this position is adjacent to the given position.
        """
        return address.is_adjacent(self.address, pos_to.address)

    def __str__(self):
        if self.is_empty():
            return "-"
        else:
            return str(self.piece)


class Piece:
    """
    Represents a piece that can occupy any position on the board.
    """

    def __init__(self, board: Board, pos: Position):
        # the board this piece is on
        self.board = board

        # the current position this piece is in
        self.pos = pos

    def get_valid_moves(self) -> List[str]:
        """
        Get a list of all addresses this piece can move to.
        """
        valid_moves = []
        for pos in self.pos.get_adjacent_positions():
            if pos.is_empty():
                valid_moves.append(pos.address)

        return valid_moves

    def move(self, target_pos: Position) -> Optional[str]:
        """
        Move this piece to a new position.

        Returns notation of the move if the move was successful.
        """

        if self.pos.is_adjacent(target_pos) and target_pos.is_empty():
            self.pos.set_piece(())
            # will place a Tiger if called from inside a Tiger,
            # and ditto for Goats
            target_pos.set_piece(type(self)(self.board, target_pos))
            return f"{self.pos.address},\t{target_pos.address}"

        print(f"unable to move this piece to {target_pos.address}")
        return None

    def get_next_adjacent_pos(
        self, target_pos: Position
    ) -> Optional[Position]:
        """
        Return the next adjacent position after the target position. This is
        used for the Tiger capturing logic.

        For example, if this piece is in a1 and the target position is b1,
        then the next adjacent position will be c1.

        If the target position is not adjacent, None is returned.
        If the next adjacent position does not exist, or is not empty,
        then None is returned.
        """

        if not self.pos.is_adjacent(target_pos):
            return None

        landing_addr = address.move_towards(
            self.pos.address, target_pos.address, 2
        )

        if landing_addr:
            new_pos = self.board.get_pos(landing_addr)
            if not new_pos.is_empty():
                return None

            return new_pos

        return None


class Tiger(Piece):
    """
    Represents a Tiger piece, symbolized with an "X".

    During their turn, Tigers can move to an adjacent empty position,
    or can capture an adjacent Goat piece by jumping over it into
    the next empty position.

    If there is no empty position to land on behind a Goat, the Tiger
    cannot move over it and the Goat cannot be captured
    (the Goat is considered "safe").
    """

    def move(self, target_pos: Position):

        # check if moving to target_pos is a capturing move
        capturing_moves = self._get_capturing_positions()
        for landing_pos, goat_pos in capturing_moves:
            if target_pos.address == landing_pos.address:
                if self.capture(goat_pos):
                    return (
                        f"{self.pos.address},\t"
                        + f"x{goat_pos.address},\t"
                        + f"{landing_pos.address}"
                    )
                else:
                    return None

        # call the move method from Piece
        return super().move(target_pos)

    def _get_capturing_positions(self) -> List[tuple]:
        """
        Returns a list of tuples of landing positions and goat positions
        where moving to the landing position will capture the goat.
        """
        # a list of positions where moving to it will capture a piece
        capturing_moves: List[tuple] = []

        # a list of capturing moves that are impossible to do
        impossibles = [
            "a1",
            "a3",
            "b4",
            "f1",
            "f3",
            "b0",
            "c0",
            "d0",
            "e0",
            "e4",
            "f4",
            "a4",
        ]

        # check adjacent positions and check if they're goats
        for goat_pos in self.pos.get_adjacent_positions():
            if isinstance(goat_pos.piece, Goat):

                landing_addr = self.can_capture_pos(goat_pos.address)

                if landing_addr:
                    # add a tuple of address and goat position
                    capturing_moves.append(
                        (self.board.get_pos(landing_addr), goat_pos)
                    )

        return [i for i in capturing_moves if i[0] not in impossibles]

    def can_capture_pos(self, addr: str) -> Optional[str]:
        """
        Checks if this tiger can capture a goat placed at a
        specific position.

        If it can, then the landing position is returned.
        """
        pos = self.board.get_pos(addr)

        if not self.pos.is_adjacent(pos):
            return None

        # check adjacent positions to the goat
        for empty_pos in pos.get_adjacent_positions():
            if empty_pos is self.pos:
                continue

            delta = address.get_displacement(
                self.pos.address, empty_pos.address
            )
            if delta not in [(0, 2), (2, 0), (0, -2), (-2, 0)]:
                continue

            if empty_pos.is_empty():
                return empty_pos.address

        return None

    def get_capturing_moves(self) -> List[str]:
        """
        Get a list of addresses where moving there will capture
        a goat.
        """
        pos_tuples = self._get_capturing_positions()
        return [tup[0].address for tup in pos_tuples]

    def get_valid_moves(self) -> List[str]:
        # combine capturing moves and valid moves
        valid_moves = super().get_valid_moves()
        valid_moves.extend(self.get_capturing_moves())
        return valid_moves

    def capture(self, target_pos: Position) -> bool:
        # the position where the Tiger will land
        landing_pos = self.get_next_adjacent_pos(target_pos)

        if not landing_pos:
            print(
                "cannot capture: cannot find landing position ("
                + self.pos.address
                + " -> "
                + target_pos.address
                + ")"
            )
            return False

        if not isinstance(target_pos.piece, Goat):
            print("cannot capture: move does not capture a Goat")
            return False

        if not isinstance(self.pos.piece, Tiger):  # shouldn't happen
            print("cannot capture: this piece is not a Tiger")
            return False

        self.pos.set_piece(())  # old position of tiger
        target_pos.set_piece(())  # captured goat piece
        landing_pos.set_piece(
            Tiger(self.board, landing_pos)
        )  # new position of tiger

        self.board.num_captured += 1  # increment captured pieces
        # print(f"the goat at {target_pos.address} has been captured")

        return True

    def __str__(self):
        return "X"  # the string representation of this piece


class Goat(Piece):
    """
    Represents a Goat piece, symbolized by an "O".

    During their turn, a Goat may move to any adjacent empty position.
    Unlike Tigers, Goats cannot capture pieces.
    """

    def __str__(self):
        return "O"  # the string representation of this piece
