"""
Collection of common operations on board addresses.
"""

from typing import Optional, List

# the rows on the board
NUMBERS = "01234"

# the rows on the board if the column is a or f
NUMBERS_AF = "123"

# the columns on the board
LETTERS = "abcdef"

# all possible board addresses
possible_pos = [
    "a1",
    "a2",
    "a3",
    "b0",
    "b1",
    "b2",
    "b3",
    "b4",
    "c1",
    "c2",
    "c3",
    "c4",
    "d1",
    "d2",
    "d3",
    "d4",
    "e1",
    "e2",
    "e3",
    "e4",
    "f1",
    "f2",
    "f3",
]


def to_indices(addr: str) -> tuple:
    """
    Convert a position address to array indices.
    For example, "a1" will be converted to (0, 1).
    """
    letter = LETTERS.index(addr[0])
    number = int(addr[1])

    if number == 0:
        return (1, 0)  # return b0 (origin position)

    return letter, number


def is_valid(addr: str):
    """Checks if the given address is valid."""
    if isinstance(addr, str) and len(addr) == 2:
        # b0 is the only valid addr in row 0
        if int(addr[1]) == 0 and addr[0] != "b":
            return False
        # check for columns A and F
        if addr[0] in "af" and addr[1] in NUMBERS_AF:
            return True
        # check for the other columns
        if addr[0] in "bcde" and addr[1] in NUMBERS:
            return True
    return False


def get_displacement(addr_a: str, addr_b: str):
    """
    Gets the displacement between two addresses.

    The difference is returned as a tuple with the
    X (letter) and Y (number) components of the difference.
    """

    # convert address of both positions into x and y components
    x1, y1 = to_indices(addr_a)
    x2, y2 = to_indices(addr_b)

    if y1 == 0 and y2 == 0:  # special case if we are in row 0
        return (0, 0)

    # special case if one address is in row 0 and
    # both addresses are in columns b-e
    if (x1 in [1, 2, 3, 4] and x2 in [1, 2, 3, 4]) and (y2 == 0 or y1 == 0):
        return (0, y2 - y1)

    return (x2 - x1, y2 - y1)


def is_adjacent(addr_a: str, addr_b: str):
    """Checks if two addresses are adjacent."""

    # automatically return false if either pos is invalid
    if not is_valid(addr_a) or not is_valid(addr_b):
        # print('Not valid positions')
        return False

    diff = get_displacement(addr_a, addr_b)

    # print(f"{addr_a} -> {addr_b}: {diff}")

    # gets the magnitude of the X and Y components of the
    # difference, then adds them together.
    # this sum can only be 1 if the diff is
    # (0, 1), (1, 0), (0, -1), (0, 1)
    # which is true if the positions are adjacent.
    return (abs(diff[0]) + abs(diff[1])) == 1


def get_adjacent_addrs(addr: str) -> List[str]:
    """
    Return a list of positions adjacent to this one.
    """
    adjacent_addrs: List[str] = []

    # special case if this position is in row 0
    if addr[1] == "0":
        adjacent_addrs.extend(("b1", "c1", "d1", "e1"))

    else:
        # iterate through every position and check for adjacency
        for let in LETTERS:
            for num in NUMBERS:
                test_addr = let + num
                if is_adjacent(addr, test_addr):
                    adjacent_addrs.append(test_addr)

    return adjacent_addrs


def move_towards(addr_from: str, addr_to: str, steps=1):
    """
    Move the start address towards the end address by a number of steps.
    If there are more steps than spaces between the two addresses,
    then the returned address will be past the end address.

    Only works if the two addresses are in the same row or same column.
    """
    disp = get_displacement(addr_from, addr_to)
    if disp[0] and disp[1]:  # both components are non-zero
        raise ValueError("addresses not in same row or same column")

    if steps == 0:
        return addr_from

    col, row = to_indices(addr_from)

    if row == 0:  # special case for origin
        col = to_indices(addr_to)[0]
    else:
        if disp[0] > 0:
            col += steps
        elif disp[0] < 0:
            col -= steps

    if disp[1] > 0:
        row += steps
    elif disp[1] < 0:
        row -= steps

    # set column to b if in row 0
    if row == 0:
        col = 1

    try:
        return str(LETTERS[col]) + str(NUMBERS[row])
    except IndexError:
        return None


def move(addr: str, dx: int, dy: int) -> Optional[str]:
    """
    Translate the address of this position by
    dx columns and dy rows and return the resulting address.

    If the new address does not exist, then None is returned.
    """
    col, row = to_indices(addr)

    if row != 0:  # don't change y if it is in row 0 (origin position)
        row += dy
    col += dx

    try:
        return str(LETTERS[col]) + str(NUMBERS[row])
    except IndexError:
        return None
