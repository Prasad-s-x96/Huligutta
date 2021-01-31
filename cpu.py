"""
Contains functions relating to
generating moves given a board.
"""
import random
from huligutta import Board
from typing import Optional


def compute_tiger_move(board: Board) -> Optional[tuple]:
    """Compute a move as the Tiger.

    If a move was found, a tuple is returned containing the
    start and end positions if a piece needs to be moved,
    or a tuple containing a position if a piece needs to be placed.
    """

    # Randomize tiger positions
    tiger_list = board.get_all_tiger_positions()
    if len(tiger_list) < 3:
        # place tigers
        empty_list = board.get_all_empty_positions()
        empty_pos_choice = random.choice(empty_list)
        return (empty_pos_choice.address,)
    else:
        # move tiger
        if len(board.get_tiger_possible_moves()) == 0:
            return None  # cannot do a move

        move_choice = None

        # try to find a capturing move first
        # XXX: makes it difficult for CPU goats to win
        # for tiger_pos in tiger_list:
        #     capturing_moves = tiger_pos.piece.get_capturing_moves()
        #     if capturing_moves:
        #         tiger_pos_choice = tiger_pos
        #         move_choice = random.choice(capturing_moves)
        #         break

        # find a random move
        while move_choice is None:
            tiger_pos_choice = random.choice(tiger_list)
            valid_moves = tiger_pos_choice.piece.get_valid_moves()
            if valid_moves:
                move_choice = random.choice(valid_moves)

        return (tiger_pos_choice.address, move_choice)


def compute_goat_move(board: Board) -> Optional[tuple]:
    """Compute a move as the Goat.

    If a move was found, a tuple is returned containing the
    start and end positions if a piece needs to be moved,
    or a tuple containing a position if a piece needs to be placed.
    """

    # list of goats that are about to be captured
    danger_goats = board.get_tiger_capturing_moves()

    goat_list = board.get_all_goat_positions()
    tiger_list = board.get_all_tiger_positions()

    if len(tiger_list) < 3:
        # skip this turn, wait until all tigers are placed
        return None
    elif not board.is_all_goats_placed:
        # place a goat
        # ------------
        if danger_goats:
            # choose a position that saves a goat
            landing_pos, goat_pos = random.choice(danger_goats)
            pos_choice = landing_pos
        else:
            # try to choose a position that blocks a tiger
            pos_choice = None
            empty_list = board.get_all_empty_positions()

            for pos in empty_list:
                if board.is_pos_blocking(pos.address) and board.is_pos_safe(
                    pos.address
                ):
                    pos_choice = pos
                    break

            # if cannot find a blocking move, choose a random position
            if pos_choice is None:
                pos_choice = random.choice(empty_list)

        if pos_choice:
            return (pos_choice.address,)
        else:
            return None

    else:
        # move goat
        # ---------
        goat_pos_choice = None
        move_choice = None

        if danger_goats:
            # try to move the goat in danger somewhere else
            landing_pos, goat_pos = random.choice(danger_goats)
            goat_pos_choice = goat_pos
            move_choice = random.choice(goat_pos.piece.get_valid_moves())
        else:
            # try to find a safe move
            for goat_pos in goat_list:
                # this goat is blocking a tiger, try to find another one
                if board.is_pos_blocking(goat_pos.address):
                    continue

                for move in goat_pos.piece.get_valid_moves():
                    if board.is_pos_safe(move):
                        goat_pos_choice = goat_pos
                        move_choice = move
                        break

        # if couldn't find a goat yet, pick one at random
        if goat_pos_choice is None:
            goat_pos_choice = random.choice(goat_list)

        # if couldn't find a move yet, pick one at random
        if move_choice is None:
            valid_moves = goat_pos_choice.piece.get_valid_moves()
            if valid_moves:
                move_choice = random.choice(valid_moves)

        if move_choice:
            return (goat_pos_choice.address, move_choice)
        else:
            return None
