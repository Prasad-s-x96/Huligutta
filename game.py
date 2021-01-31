"""
Huligutta (Goats and Tigers)
file: game.py
Description: GUI of the game using TKinter
"""

__author__ = "Clyde James Felix"
__email__ = "cjfelix.hawaii.edu"
__status__ = "Dev"

from tkinter import *
from tkinter import messagebox
import os
import numpy as np
import sys
import time
from huligutta import Board
from functions import *
from PIL import ImageTk, Image
from random import randint, choice, sample
from sys import platform
import cpu

# GAME VARIABLES
# ==============

DELAY = 0.1  # how long it takes for the CPU to make a move (in seconds)

# Game mode:
# Uncomment to choose the game mode

# MODE = 'pvp'          # Player vs. Player
# MODE = "goatPlayer"  # You are Goat
MODE = "tigerPlayer"  # You are tiger
# MODE = "cpu"  # CPU vs. CPU

# Board parts

numPosition = 23
if platform == "darwin":
    # Mac
    boardSize = 500
    fontSize = 15
    buttonStyle = 30
elif platform == "win32" or platform == "cygwin":
    # Windows
    boardSize = 500
    fontSize = 12
    buttonStyle = 0
elif platform == "linux":
    # Linux
    boardSize = 500
    fontSize = 12
    buttonStyle = 0

boardSize = 500

board = Board()
board.clear()

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
root = os.path.abspath("images")
# Game modes:
class Main:
    def __init__(self, mode):

        img_tiger_path = root + "/tiger.gif"
        img_goat_path = root + "/goat.gif"

        self.window = Tk()
        self.window.title("Huligutta (Goats & Tigers)")
        self.window.geometry(str(boardSize) + "x" + str(boardSize + 20))
        self.window.resizable(0, 0)
        # self.window.tk_focusFollowsMouse()
        # self.window.tk.call('tk', 'scaling', 17)

        # assets
        # ------------------------------------------------------------------------------

        self.img_tiger = PhotoImage(file=img_tiger_path).subsample(2, 2)
        self.img_goat = PhotoImage(file=img_goat_path).subsample(2, 2)
        self.canvas = Canvas(self.window, width=boardSize, height=boardSize)

        # flags
        # ------------------------------------------------------------------------------

        # if False, stop the program
        self.is_running = True

        # For self.turn, Goat: False, Tiger: True
        self.turn = (
            False  # TODO: make this a number or string for readability?
        )
        self.initialize_board()
        self.canvas.pack()

        # if true, will move a piece to the next clicked empty space
        self.is_moving_piece = False
        # the address of the piece to move, if not blank
        self.moving_from_pos = ""

        self.turntext = StringVar()
        self.numGoats = StringVar()
        self.goatsEatentext = StringVar()
        self.selectedBtn = StringVar()
        self.goatEaten = 0
        self.goatCount = 0
        self.moveCount = 0
        self.moveCount_prev = 0

        # canvas items
        # ------------------------------------------------------------------------------

        self.turnDisp = Label(
            self.window,
            font=("Helvetica", fontSize),
            textvariable=self.turntext,
        ).place(x=boardSize - 100, y=25)
        self.selectedDisp = Label(
            self.window,
            font=("Helvetica", fontSize),
            textvariable=self.selectedBtn,
        ).place(x=boardSize - 100, y=50)
        self.goatDisp = Label(
            self.window,
            font=("Helvetica", fontSize),
            textvariable=self.numGoats,
        ).place(x=10, y=25)
        self.goatEatenDisp = Label(
            self.window,
            font=("Helvetica", fontSize),
            textvariable=self.goatsEatentext,
        ).place(x=10, y=50)
        self.update_canvas()
        self.reportBugbtn = Button(
            self.window, text="Report Bug", command=lambda: self.report_bug()
        ).place(x=70, y=boardSize - 15, anchor=CENTER)

        # Buttons
        # self.btn1  = Button(self.window, bd=buttonStyle,command=lambda : self.button_position('b0')).place(x=boardSize/2,y=boardSize/10,height=30,width=30,anchor=CENTER)
        # self.btn2  = Button(self.window, bd=buttonStyle,command=lambda : self.button_position('a1')).place(x=boardSize/10,y=boardSize/2 - 70,height=30,width=30,anchor=CENTER)
        # self.btn3  = Button(self.window, bd=buttonStyle,command=lambda : self.button_position('a2')).place(x=boardSize/10,y=boardSize/2,height=30,width=30,anchor=CENTER)
        # self.btn4  = Button(self.window, bd=buttonStyle,command=lambda : self.button_position('a3')).place(x=boardSize/10,y=boardSize/2 + 70,height=30,width=30,anchor=CENTER)
        # self.btn5  = Button(self.window, bd=buttonStyle,command=lambda : self.button_position('b1')).place(x=boardSize/2 - 65,y=boardSize/2 - 70,height=30,width=30,anchor=CENTER)
        # self.btn6  = Button(self.window, bd=buttonStyle,command=lambda : self.button_position('b2')).place(x=boardSize/2- 100,y=boardSize/2,height=30,width=30,anchor=CENTER)
        # self.btn7  = Button(self.window, bd=buttonStyle,command=lambda : self.button_position('b3')).place(x=boardSize/2-135,y=boardSize/2+70,height=30,width=30,anchor=CENTER)
        # self.btn8  = Button(self.window, bd=buttonStyle,command=lambda : self.button_position('b4')).place(x=boardSize/10,y=boardSize - boardSize/10,height=30,width=30,anchor=CENTER)
        # self.btn9  = Button(self.window, bd=buttonStyle,command=lambda : self.button_position('c1')).place(x=boardSize/2 - 25,y=boardSize/2 - 70,height=30,width=30,anchor=CENTER)
        # self.btn10 = Button(self.window, bd=buttonStyle,command=lambda : self.button_position('c2')).place(x=boardSize/2 - 38,y=boardSize/2,height=30,width=30,anchor=CENTER)
        # self.btn11 = Button(self.window, bd=buttonStyle,command=lambda : self.button_position('c3')).place(x=boardSize/2 - 53,y=boardSize/2 + 70,height=30,width=30,anchor=CENTER)
        # self.btn12 = Button(self.window, bd=buttonStyle,command=lambda : self.button_position('c4')).place(x= boardSize/2 - 80,y=boardSize - boardSize/10,height=30,width=30,anchor=CENTER)
        # self.btn13 = Button(self.window, bd=buttonStyle,command=lambda : self.button_position('d1')).place(x=boardSize/2 + 25,y=boardSize/2 - 70,height=30,width=30,anchor=CENTER)
        # self.btn14 = Button(self.window, bd=buttonStyle,command=lambda : self.button_position('d2')).place(x=boardSize/2 + 38,y=boardSize/2,height=30,width=30,anchor=CENTER)
        # self.btn15 = Button(self.window, bd=buttonStyle,command=lambda : self.button_position('d3')).place(x=boardSize/2 + 53,y=boardSize/2 + 70,height=30,width=30,anchor=CENTER)
        # self.btn16 = Button(self.window, bd=buttonStyle,command=lambda : self.button_position('d4')).place(x=boardSize/2 + 80,y=boardSize - boardSize/10,height=30,width=30,anchor=CENTER)
        # self.btn17 = Button(self.window, bd=buttonStyle,command=lambda : self.button_position('e1')).place(x=boardSize/2 + 65,y=boardSize/2 - 70,height=30,width=30,anchor=CENTER)
        # self.btn18 = Button(self.window, bd=buttonStyle,command=lambda : self.button_position('e2')).place(x=boardSize/2+100,y=boardSize/2,height=30,width=30,anchor=CENTER)
        # self.btn19 = Button(self.window, bd=buttonStyle,command=lambda : self.button_position('e3')).place(x=boardSize/2 + 135,y=boardSize/2 + 70,height=30,width=30,anchor=CENTER)
        # self.btn20 = Button(self.window, bd=buttonStyle,command=lambda : self.button_position('e4')).place(x=boardSize - boardSize/10,y=boardSize - boardSize/10,height=30,width=30,anchor=CENTER)
        # self.btn21 = Button(self.window, bd=buttonStyle,command=lambda : self.button_position('f1')).place(x=boardSize-boardSize/10,y=boardSize/2 - 70,height=30,width=30,anchor=CENTER)
        # self.btn22 = Button(self.window, bd=buttonStyle,command=lambda : self.button_position('f2')).place(x=boardSize-boardSize/10,y=boardSize/2,height=30,width=30,anchor=CENTER)
        # self.btn23 = Button(self.window, bd=buttonStyle,command=lambda : self.button_position('f3')).place(x=boardSize-boardSize/10,y=boardSize/2 + 70,height=30,width=30,anchor=CENTER)

    def destroy(self):
        """Stop the program."""
        autorestart = True
        if autorestart:
            self.start()
        else:
            self.window.destroy()
            self.is_running = False

    def initialize_board(self):
        # Draws the board
        self.canvas.create_rectangle(
            boardSize / 10,
            boardSize / 2 - 70,
            boardSize - boardSize / 10,
            boardSize / 2 + 70,
        )
        self.canvas.create_line(
            boardSize / 10,
            boardSize / 2,
            boardSize - boardSize / 10,
            boardSize / 2,
        )
        self.canvas.create_line(
            boardSize / 2,
            boardSize / 10,
            boardSize / 10,
            boardSize - boardSize / 10,
        )
        self.canvas.create_line(
            boardSize / 2,
            boardSize / 10,
            boardSize - boardSize / 10,
            boardSize - boardSize / 10,
        )
        self.canvas.create_line(
            boardSize / 10,
            boardSize - boardSize / 10,
            boardSize - boardSize / 10,
            boardSize - boardSize / 10,
        )
        self.canvas.create_line(
            boardSize / 2,
            boardSize / 10,
            boardSize / 2 - 80,
            boardSize - boardSize / 10,
        )
        self.canvas.create_line(
            boardSize / 2,
            boardSize / 10,
            boardSize / 2 + 80,
            boardSize - boardSize / 10,
        )

        printAndLog("========================")
        attempts = textCount("Attempts: ")
        printAndLog("Attempts: " + str(attempts))
        printAndLog("Game Mode: " + MODE)
        printAndLog("========================")

    def button_position(self, pos):
        """
        Called when a position button is clicked.
        """
        # Moves pieces in clicks

        # print('###### Debug ######')
        # print('location:', self.moving_from_pos)
        # print('Position clicked: ', pos)

        # Handles how goat positions move
        self.moveCount_prev = self.moveCount

        if MODE == "pvp":
            self.pvpMode(pos)
            self.update_canvas()
        elif MODE == "goatPlayer":
            self.goatMode(pos)
        elif MODE == "tigerPlayer":
            self.tigerMode(pos)

        if self.moveCount_prev != self.moveCount:
            self.update_game()
            self.log_data()
        self.window.mainloop()

    def pvpMode(self, pos):

        # How goats move
        if self.turn == False:

            if Position(pos[0], pos[1]).content() == "X":
                print("You must select any empty or goat positions")
            elif (
                Position(pos[0], pos[1]).content() == ()
                and self.is_moving_piece == False
            ):
                if self.goatCount < 15:
                    Goat(pos).place()
                    self.update_buttons(pos, self.img_goat)
                    self.window.update()
                    self.turn = True
                else:
                    print("exceeded goats amount")

            elif Position(pos[0], pos[1]).content() == "O":
                if self.goatCount == 15:
                    if pos == self.moving_from_pos:
                        self.is_moving_piece = not self.is_moving_piece
                        # print('Debug: self.is_moving_piece ',self.is_moving_piece)
                    # Select valid position to move
                    elif self.is_moving_piece == False:
                        self.is_moving_piece = True
                        self.moving_from_pos = pos
                else:
                    print("Goats can only be moved if 15 goats are placed")
            else:

                if Goat(self.moving_from_pos).move(pos) == 1:
                    self.update_buttons(pos, self.img_goat)
                    self.window.update()
                    self.is_moving_piece = False
                    self.moving_from_pos = ""
                    self.turn = True
                    self.moveCount = self.moveCount + 1
            pass

        # How tigers move
        elif self.turn == True:
            # print('DEBUG: location',self.moving_from_pos)

            # print('DEBUG: possible moves',Piece(pos).possibleMoves())
            if (
                Position(pos[0], pos[1]).content() != "X"
                and self.is_moving_piece == False
            ):
                print("You must select any current tiger positions")

            elif Position(pos[0], pos[1]).content() == "X":
                if pos == self.moving_from_pos:
                    self.is_moving_piece = not self.is_moving_piece
                elif (
                    self.moving_from_pos == ""
                    or self.is_moving_piece == False
                    or pos != self.moving_from_pos
                ):
                    self.is_moving_piece = True
                    self.moving_from_pos = pos

            elif (
                Position(pos[0], pos[1]).content() == ()
                and self.is_moving_piece == True
            ):
                # print('DEBUG: location',self.moving_from_pos)
                # print('DEBUG: secondAdjacent',Piece(self.moving_from_pos).secondAdjacent(pos))
                # print('DEBUG: Adjacent',Piece(self.moving_from_pos).adjacent(pos))
                # print('DEBUG: possiblemoves 2 ', Piece(self.moving_from_pos).possibleMoves())
                if (
                    pos
                    in Position(
                        self.moving_from_pos[0], self.moving_from_pos[1]
                    ).get_neighbors()
                ):
                    tigerMoveFlag = Tiger(self.moving_from_pos).move(pos)

                    if tigerMoveFlag == 1:
                        self.is_moving_piece = False
                        self.moving_from_pos = ""
                        self.turn = False
                        self.moveCount = self.moveCount + 1
                        return

                # TODO: error on capture message when Tiger moves to corner (i.e Tiger move to e4)
                elif pos in Tiger(self.moving_from_pos).possibleMoves():
                    if Tiger(self.moving_from_pos).capture(pos) == 1:

                        self.goatEaten = self.goatEaten + 1
                        self.is_moving_piece = False
                        self.moving_from_pos = ""
                        self.turn = False
                        self.moveCount = self.moveCount + 1

                else:
                    print("Error on capture")
                    self.is_moving_piece = False
                    self.moving_from_pos = ""
                    self.turn = True
        self.update_canvas()

    def goatMode(self, addr: str):
        """
        Called when a player clicks a button in player goat vs. CPU tiger mode.
        """

        if self.turn == True:
            return

        pos = board.get_pos(addr)
        if pos.is_tiger():
            # clicked on a tiger; ignore
            print("You must select any empty or goat positions")
        elif pos.is_empty() and self.is_moving_piece == False:
            # clicked on an empty space
            if self.goatCount < 15:
                board.place_goat(addr)
                self.update_buttons(addr, self.img_goat)
                self.window.update()
                self.turn = True
            else:
                print("exceeded goats amount")
        elif pos.is_goat():
            # clicked on a goat
            if self.goatCount == 15:
                if addr == self.moving_from_pos:
                    self.is_moving_piece = not self.is_moving_piece
                    # print('Debug: self.is_moving_piece ',self.is_moving_piece)
                # Select valid position to move
                elif self.is_moving_piece == False:
                    self.is_moving_piece = True
                    self.moving_from_pos = pos
            else:
                print("Goats can only be moved if 15 goats are placed")
        else:
            # clicked on an empty space after clicking on a goat
            if self.move_piece(self.moving_from_pos.address, pos.address):
                self.is_moving_piece = False
                self.moving_from_pos = ""
                self.turn = True
                self.moveCount = self.moveCount + 1

        self.update_canvas()
        self.update_game()

        time.sleep(DELAY)
        self.do_cpu_tiger_move()

        self.turn = False
        self.update_canvas()

    def tigerMode(self, addr: str):
        """
        Called when a player clicks a button in CPU goat vs. player tiger mode.
        """

        if self.turn == False:
            return

        pass_turn = True  # if true, pass turn over to goats after this fn
        num_tigers = len(board.get_all_tiger_positions())

        pos = board.get_pos(addr)
        # print('DEBUG: possible moves',Piece(pos).possibleMoves())

        if not self.is_moving_piece:  # select piece at the clicked position

            if num_tigers < 3 and pos.is_empty():
                # place tiger
                self.place_tiger(pos.address)
            elif pos.is_tiger():
                # prepare to move tiger
                self.is_moving_piece = True
                self.moving_from_pos = pos
                pass_turn = False

        else:  # move piece to the clicked position
            valid_moves = self.moving_from_pos.piece.get_valid_moves()
            capturing_moves = self.moving_from_pos.piece.get_capturing_moves()

            is_capturing_move = True if addr in capturing_moves else False

            if addr in valid_moves:

                # print('DEBUG: location',self.moving_from_pos)
                # print('DEBUG: secondAdjacent',Piece(self.moving_from_pos).secondAdjacent(pos))
                # print('DEBUG: Adjacent',Piece(self.moving_from_pos).adjacent(pos))
                # print('DEBUG: possiblemoves 2 ', Piece(self.moving_from_pos).possibleMoves())

                if board.move_piece(self.moving_from_pos.address, addr):
                    if is_capturing_move:
                        self.goatEaten = self.goatEaten + 1
                    self.is_moving_piece = False
                    self.moveCount = self.moveCount + 1

                else:
                    print("Error on capture")

                self.is_moving_piece = False
                self.moving_from_pos = ""

        self.update_game()
        self.update_canvas()

        # do CPU goat move
        if pass_turn:
            self.turn = False
            self.do_cpu_goat_move()
            self.turn = True
            self.update_canvas()

    def do_cpu_tiger_move(self):
        """Have the computer do a move as the Tiger."""

        time.sleep(DELAY)
        if self.turn == True:
            move = cpu.compute_tiger_move(board)
            if move:
                if len(move) == 1:  # place tiger
                    self.place_tiger(move[0])
                if len(move) == 2:  # move tiger
                    self.move_piece(move[0], move[1])

        self.update_game()

    def do_cpu_goat_move(self):
        """Have the computer do a move as the Goat."""

        time.sleep(DELAY)
        if self.turn == False and len(board.get_all_tiger_positions()) == 3:
            move = cpu.compute_goat_move(board)
            if move:
                if len(move) == 1:  # place goat
                    self.place_goat(move[0])
                if len(move) == 2:  # move goat
                    self.move_piece(move[0], move[1])

        self.update_game()

    def process_turn_cpu(self):
        """Process a turn for a CPU vs. CPU game."""

        self.turn = True
        self.do_cpu_tiger_move()
        self.turn = False
        self.do_cpu_goat_move()

        # self.log_data()
        if self.is_running:
            self.process_turn_cpu()

    def process_turn_goat(self):
        """Process a turn for a player goat vs. CPU tiger."""

        self.turn = True
        self.do_cpu_tiger_move()
        self.do_cpu_tiger_move()
        self.do_cpu_tiger_move()

        self.turn = False

    def move_piece(self, from_addr: str, to_addr: str) -> bool:
        """Move a piece on the board and log it.
        If the move is successful, returns True."""
        notation = board.move_piece(from_addr, to_addr)
        if notation:
            printAndLog(notation)
        return bool(notation)

    def place_goat(self, addr: str):
        """Place a piece on the board and log it."""
        board.place_goat(addr)
        printAndLog(f"G{addr}")

    def place_tiger(self, addr: str):
        """Place a piece on the board and log it."""
        board.place_tiger(addr)
        printAndLog(f"T{addr}")

    def update_game(self):
        """Update the screen."""

        if not self.is_running:
            return  # don't attempt to update

        numGoats = 0

        # update GUI buttons

        for pos in board.get_all_positions():
            if pos.is_empty():
                self.update_buttons(pos.address, "")
            elif pos.is_goat():
                numGoats = numGoats + 1
                self.update_buttons(pos.address, self.img_goat)
            else:
                self.update_buttons(pos.address, self.img_tiger)

        possibleMovesCount = len(board.get_tiger_possible_moves())
        # print("possible tiger moves: %s" % possibleMovesCount)

        num_tigers, num_goats = board.num_pieces()
        num_captured = board.num_captured

        self.goatCount = numGoats

        self.update_canvas()

        # win condition for goats
        if num_tigers == 3 and possibleMovesCount == 0:
            printAndLog(f"Goats win ({board.num_moves} moves)")
            messagebox.showinfo("Game Over", "Goat wins")
            self.destroy()

        # win condition for tigers
        elif num_captured == 5:
            printAndLog(f"Tigers win ({board.num_moves} moves)")
            # messagebox.showinfo("Game Over", "Tiger wins")
            self.destroy()

    def log_data(self):
        """
        Logs important information about the state of the board.
        """
        printAndLog("Move: " + str(self.moveCount))
        printAndLog("--------------------")
        printAndLog("Goats: " + str(self.goatCount))
        tigers = board.get_all_tiger_positions()
        printAndLog("Tigers positions: " + str(tigers))
        editDistance = edit_distance(board)
        printAndLog("Edit distance: " + str(editDistance))

    def update_canvas(self):
        """Updates any canvas items based on the state of the board."""

        self.numGoats.set(
            "Number of goats: %s" % len(board.get_all_goat_positions())
        )
        self.goatsEatentext.set("Goats eaten: %s" % board.num_captured)

        # if a piece was selected, display it
        if self.is_moving_piece:
            self.selectedBtn.set("Selected: %s" % self.moving_from_pos.address)
        else:
            self.selectedBtn.set("")

        # displays turn as text in the window
        if self.turn:
            self.turntext.set("Turn: Tiger")
        else:
            self.turntext.set("Turn: Goat")

        # also update the window
        self.window.update()

    def update_buttons(self, pos, img):
        # change the images of the board pieces

        screen_positions = {
            "b0": (boardSize / 2, boardSize / 10),
            "a1": (boardSize / 10, boardSize / 2 - 70),
            "a2": (boardSize / 10, boardSize / 2),
            "a3": (boardSize / 10, boardSize / 2 + 70),
            "b1": (boardSize / 2 - 65, boardSize / 2 - 70),
            "b2": (boardSize / 2 - 100, boardSize / 2),
            "b3": (boardSize / 2 - 135, boardSize / 2 + 70),
            "b4": (boardSize / 10, boardSize - boardSize / 10),
            "c1": (boardSize / 2 - 25, boardSize / 2 - 70),
            "c2": (boardSize / 2 - 38, boardSize / 2),
            "c3": (boardSize / 2 - 53, boardSize / 2 + 70),
            "c4": (boardSize / 2 - 80, boardSize - boardSize / 10),
            "d1": (boardSize / 2 + 25, boardSize / 2 - 70),
            "d2": (boardSize / 2 + 38, boardSize / 2),
            "d3": (boardSize / 2 + 53, boardSize / 2 + 70),
            "d4": (boardSize / 2 + 80, boardSize - boardSize / 10),
            "e1": (boardSize / 2 + 65, boardSize / 2 - 70),
            "e2": (boardSize / 2 + 100, boardSize / 2),
            "e3": (boardSize / 2 + 135, boardSize / 2 + 70),
            "e4": (boardSize - boardSize / 10, boardSize - boardSize / 10),
            "f1": (boardSize - boardSize / 10, boardSize / 2 - 70),
            "f2": (boardSize - boardSize / 10, boardSize / 2),
            "f3": (boardSize - boardSize / 10, boardSize / 2 + 70),
        }

        _ = Button(
            self.window,
            image=img,
            bd=buttonStyle,
            command=lambda: self.button_position(pos),
        ).place(
            x=screen_positions[pos][0],
            y=screen_positions[pos][1],
            height=30,
            width=30,
            anchor=CENTER,
        )

    def report_bug(self):
        printAndLog("Bug reporting...")
        print("What to include for the report:")
        print("What happened?")
        print("What operating system you are running?")
        reason = input("Type the reason for the bug:")
        printAndLog("Bug reported \nReason: " + reason)

    def start(self):
        # Sets up the game window
        # Tiger's initial positions

        # Uncomment to start official game
        # board.place_tiger("b0")
        # board.place_tiger("c1")
        # board.place_tiger("d1")

        # Uncomment to randomize initial positions
        # numOpenPositions = random.randint(3, 18)
        # numGoatsPlaced = numOpenPositions - 3
        # moves = random.sample(possible_pos, k=numOpenPositions)
        # randomTigerPositions = random.sample(moves, k=3)

        # for tiger_pos in randomTigerPositions:
        #     board.place_tiger(tiger_pos)
        #     moves.remove(str(tiger_pos))

        # for goat_pos in moves:
        #     board.place_goat(goat_pos)

        #########################################################

        board.clear()
        self.turn = True

        if MODE == "tigerPlayer":
            pass
        elif MODE == "goatPlayer":
            self.do_cpu_tiger_move()
            self.do_cpu_tiger_move()
            self.do_cpu_tiger_move()
            self.turn = False
        elif MODE == "cpu":
            self.process_turn_cpu()  # starts a loop that runs both CPU moves

        self.update_game()
        self.window.mainloop()


if __name__ == "__main__":

    game = Main(MODE)
    game.start()
