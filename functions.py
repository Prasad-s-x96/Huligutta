"""
file: functions.py
Description: Statistical and other helper functions
"""

__author__ = "Clyde James Felix"
__email__ = "cjfelix.hawaii.edu"
__status__ = "Dev"

from huligutta import Board
from itertools import combinations
from copy import deepcopy
import networkx as nx
from networkx.algorithms import bipartite
import random
import numpy as np

log_file = "dataset/data.txt"


def optimal_stalemate(pos1, pos2, pos3):
    """
    Returns the least amount of goats required to stalemate the tigers and the
    board at the end of the game
    """

    # Clear Board
    board = Board()

    board.place_tiger(pos1)
    board.place_tiger(pos2)
    board.place_tiger(pos3)

    tiger_positions = pos1, pos2, pos3

    positions = board.positions

    for tiger_addr in tiger_positions:

        tiger_pos = board.get_pos(tiger_addr)
        tiger: Tiger = tiger_pos.piece

        # place goats in all positions adjacent to the tiger
        for adj_pos in tiger_pos.get_adjacent_positions():
            if adj_pos.is_empty():
                adj_pos.place_goat()

        # place goats in all capturing positions
        for capturing_addr in tiger.get_capturing_moves():
            board.place_goat(capturing_addr)

    num_goats = board.num_pieces()[1]

    return num_goats, board


def stalemate(pos1, pos2, pos3):
    # function: determines the optimal stalemates
    # input: position of the three tigers
    # return: board position that stalemates the tigers (with the min number of goats)

    positions = {
        "b0": (),
        "a1": (),
        "a2": (),
        "a3": (),
        "b1": (),
        "b2": (),
        "b3": (),
        "b4": (),
        "c1": (),
        "c2": (),
        "c3": (),
        "c4": (),
        "d1": (),
        "d2": (),
        "d3": (),
        "d4": (),
        "e1": (),
        "e2": (),
        "e3": (),
        "e4": (),
        "f1": (),
        "f2": (),
        "f3": (),
    }

    positions[pos1] = "X"
    positions[pos2] = "X"
    positions[pos3] = "X"
    tigers = [pos1, pos2, pos3]
    # print('DEBUG: args ', args)

    for tiger in tigers:
        ## Blocks the adjacents
        # print('DEBUG: args[tiger]', tiger)
        # print('DEBUG: Position(args[tiger][0],args[tiger][1]).get_neighbors() ',Position(tiger[0],tiger[1]).get_neighbors())
        for neighbor in Position(tiger[0], tiger[1]).get_neighbors():
            if positions[neighbor] == () and neighbor in possible_pos:
                positions[neighbor] = "O"
            capture = Piece(tiger).secondAdjacent(neighbor)
            if (
                Piece(tiger).secondAdjacent(neighbor) != None
                and positions[capture] == ()
            ):
                positions[capture] = "O"

    ## Blocks the captures
    # if Position(tiger[0],tiger[1]).get_captures() != None:

    #     for capture in Position(tiger[0],tiger[1]).get_captures():
    #         print('capturing at: ', capture)
    #             positions[capture] = 'O'

    positions = positions
    numGoats = len(goatPositions(positions))
    ## Display the minimum number of goats
    # print('Number of goats:',numGoats)
    # Board().printBoard()
    return numGoats, positions


def edit_distance(board: Board) -> int:
    # Determines the edit distance between the board positions and the stalemate positions
    # input: board positions
    # return: edit distance value

    tigers = board.get_all_tiger_positions()
    numGoats = len(board.get_all_goat_positions())

    _, stalemate_board = optimal_stalemate(
        tigers[0].address, tigers[1].address, tigers[2].address
    )
    # _, stalematePositions = stalemate(tigers[0], tigers[1], tigers[2])
    possible_pos = board.get_all_addresses()
    # Initializing Bipartite graph
    B = nx.Graph()
    B.add_nodes_from(list(range(23)), bipartite=0)
    B.add_nodes_from(possible_pos, bipartite=1)

    # Populate graph
    for i, pos in enumerate(possible_pos):
        for stalematePos in stalemate_board.get_all_positions():

            # print('DEBUG: pos ', pos, ' stalematePos ',stalematePos)
            # print('DEBUG: possible_pos[pos] ', boardPosition[possible_pos[pos]], ' stalematePositions[stalematePos] ', stalematePositions[stalematePos])
            # print('DEBUG: pos ', possible_pos[pos], ' stalematePos ',stalematePos)
            # print(10 - num_moves(pos,stalematePos))
            if (
                board.get_pos(stalematePos.address).is_goat()
                and stalematePos.is_goat()
            ):

                # print('stalematePos',stalematePos, 'weight',10 - num_moves(possible_pos[pos],stalematePos))
                B.add_edge(
                    i,
                    stalematePos,
                    weight=-10 + num_moves(pos, stalematePos.address),
                )
            # elif boardPosition[possible_pos[pos]] == stalematePositions[stalematePos] and possible_pos[pos] == stalematePos:
            #     B.add_edge(pos,stalematePos, weight = -1e20)
            else:
                B.add_edge(i, stalematePos.address, weight=1e20)

    # Bipartite Max Matching
    # print(B.edges(data=True))

    maxMatching = bipartite.minimum_weight_full_matching(B)
    # print(maxMatching)
    Sum = 0
    # Collect sum of weights
    n = 0
    for key, item in maxMatching.items():
        if n == 23:
            break
        # # print(B.get_edge_data(key,item)['weight'])
        if board.get_pos(possible_pos[key]).is_goat():
            Sum = Sum + num_moves(possible_pos[key], item)
        # print(Sum)
        n = n + 1

    return Sum


def num_moves(pos1, pos2):
    # Input: i,j indices in the position graph
    # Output: number of moves from start posiiton to end position
    dist = 0
    alphabet = " abcdef"

    startX = pos1[0]
    startY = pos1[1]
    endX = pos2[0]
    endY = pos2[1]

    # print('pos1 ', pos1)
    # print('pos2 ', pos2)
    # print('endX ',alphabet.index(endX) )
    # print('endY ',int(endY))
    # print('startX ',alphabet.index(startX) )
    # print('startY ',int(startY))

    if pos1 == pos2:
        return 0
    else:
        if pos1 == "b0":
            if endX in "bcde":
                startX = endX
            elif endX == "a":
                startX = "b"
            elif endX == "f":
                startX = "e"
        elif pos2 == "b0":
            if startX in "bcde":
                endX = startX
            elif startX == "a":
                endX = "b"
            elif startX == "f":
                endX = "e"
        return abs((int(endY) - int(startY))) + abs(
            (alphabet.index(endX) - alphabet.index(startX))
        )


def board2mat(board):
    # '': not applicable

    # Initialize matrix
    mat = [[None for i in range(6)] for j in range(5)]

    # Populate values into the matrix
    mat[0][1] = mat[0][2] = mat[0][3] = mat[0][4] = board[0]["origin"]

    for i in range(len(board) - 1):
        for j in board[i + 1]:
            mat[j][i] = board[i + 1][j]
    return np.array(mat, dtype=object)


def flatten(mat):
    return np.array(mat, dtype=object).reshape(30)


def unflatten(flat_mat):
    return np.array(flat_mat, dtype=object).reshape(5, 6)


def printBoard(positions):
    print("\t*\t*\t" + str(positions["b0"]) + "\t*\t*\t")
    print(
        str(positions["a1"])
        + "\t"
        + str(positions["b1"])
        + "\t"
        + str(positions["c1"])
        + "\t\t"
        + str(positions["d1"])
        + "\t"
        + str(positions["e1"])
        + "\t"
        + str(positions["f1"])
    )
    print(
        str(positions["a2"])
        + "\t"
        + str(positions["b2"])
        + "\t"
        + str(positions["c2"])
        + "\t\t"
        + str(positions["d2"])
        + "\t"
        + str(positions["e2"])
        + "\t"
        + str(positions["f2"])
    )
    print(
        str(positions["a3"])
        + "\t"
        + str(positions["b3"])
        + "\t"
        + str(positions["c3"])
        + "\t\t"
        + str(positions["d3"])
        + "\t"
        + str(positions["e3"])
        + "\t"
        + str(positions["f3"])
    )
    print(
        "\t"
        + str(positions["b4"])
        + "\t"
        + str(positions["c4"])
        + "\t\t"
        + str(positions["d4"])
        + "\t"
        + str(positions["e4"])
    )


def tigerPositions(positions):
    return [key for key, item in positions.items() if item == "X"]


def goatPositions(positions):
    return [key for key, item in positions.items() if item == "O"]


def emptyPositions(positions):
    return [key for key, item in positions.items() if item == ()]


def printAndLog(text):
    print(text)
    with open(log_file, "a") as file:
        file.write(text + "\n")


def textCount(text):

    # Count how many times a text appears in the log.txt file
    i = 0
    with open(log_file) as search:
        for line in search:
            line = line.rstrip()
            if text in line:
                i = i + 1
    return i


# if __name__ == "__main__":
# Board().clearBoard()
# Tiger('b3').place()
# Tiger('d3').place()
# Tiger('a2').place()
# Goat('a1').place()
# Goat('f1').place()
# Goat('f2').place()
# Goat('b2').place()
# Goat('b1').place()

# Board().printBoard()
# tigers = tigerPositions(Board().boardPositions)
# print(tigers)
# _,staleMate = stalemate(tigers[0],tigers[1],tigers[2])
# printBoard(staleMate)
# possible_pos = list(Board().boardPositions.keys())
# # print(possible_pos)
# print(edit_distance(Board().boardPositions))

