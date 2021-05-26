import numpy as np
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from random import randrange, shuffle, choice
import cProfile

class Board:
    rows = 9
    cols = 9
    loc = [0, 0]

    def __init__(self, difficulty):
        self.solution, self.array = self.populate(difficulty)

    def populate(self, difficulty):
        """
        Populates Board object with random Sudoku puzzle.

        Returns
        -------
        arr
            The 2D array containing the numbers associated with
            the Sudoku puzzle.
        """
        arr = np.empty((Board.rows, Board.cols, 1), dtype=int)
        temp = np.arange(1,10)
        shuffle(temp)
        arr[0] = temp
        arr[1] = np.roll(temp, -3)
        arr[2] = np.roll(arr[1], -3)
        for i in range(3, 9, 3): # could have an issue with non-multiples of 3
            arr[i] = np.roll(arr[i-1], -1)
            arr[i+1] = np.roll(arr[i], -3)
            arr[i+2] = np.roll(arr[i+1], -3)

        solution = np.copy(arr)

        index_arr = np.arange(0, Board.cols)
        for i in range(Board.rows):
            for _ in range(difficulty):
                # find index of random element
                rem = choice(index_arr)
                temp = arr[i][rem]
                # try deleting random element
                self.remove_number(arr, i, rem)
                # if puzzle is no longer solvable
                # --> re-add the element
                temp_arr = np.copy(arr)
                if not self.solve(temp_arr):
                    self.add_number(arr, temp, i, rem)
        return solution, arr

    def add_number(self, arr, num, i, j):
        arr[i, j] = num
    
    def remove_number(self, arr, i, j):
        arr[i, j] = 0

    def clear_board(self):
        self.array.clear()

    def find_empty(self, arr):
        """
        Updates pointer to location on board
        if a square is empty (value is zero).

        Returns
        -------
        bool
            True if empty square. False if no square is empty.
        """
        for i in range(Board.rows):
            for j in range(Board.cols):
                if arr[i][j] == 0:
                    Board.loc = [i, j]
                    return True
        return False

    def valid(self, arr, num):
        # Checking row for duplicate number
        for i in range(Board.rows):
            if arr[Board.loc[0]][i] == num and Board.loc[1] != i:
                return False
        # Checking column for duplicate number
        for j in range(Board.cols):
            if arr[j][Board.loc[1]] == num and Board.loc[0] != j:
                return False
        # Checking box for duplicate number
        for i in range(Board.loc[0] // 3, Board.loc[0] // 3 + 3):
            for j in range(Board.loc[1] // 3, Board.loc[1] // 3 + 3):
                if arr[i][j] == num and Board.loc != [i, j]:
                    return False
        return True

    def solve(self, arr):
        if not self.find_empty(arr):
            return True
        for num in range(1, 10):
            if self.valid(arr, num):
                self.add_number(arr, num, Board.loc[0], Board.loc[1])
                if self.solve(arr):
                    return True
                self.remove_number(arr, Board.loc[0], Board.loc[1])
        return False
        
    def print(self, arr):
        formatted_array = ""
        for i in range(Board.rows):
            if i % 3 == 0 and i != 0:
                formatted_array += "- - - - - - - - - - - -\n"
            for j in range(Board.cols):
                if j % 3 == 0 and j != 0:
                    formatted_array += str(" | ")
                formatted_array += str(arr[i][j])
                formatted_array += " "
            formatted_array += "\n"
        print(formatted_array)
        return formatted_array


def main():
    board = Board(50)

    pos = [0, 0]
    layout = [
        [sg.Text("Manual vs. Automatic Entry: "), sg.Slider(range=(0,1), resolution=1, disable_number_display=True, orientation='h', size=(5, 10), default_value=0, enable_events=True, key="-MAN-")],
        [sg.Frame("Sudoku Puzzle",
        [
            [sg.Input(str(board.array[0][0]), key="00", size=(1, 1)), sg.Input(str(board.array[0][1]), key="01", size=(1, 1)), sg.Input(str(board.array[0][2]), key="02", size=(1, 1)), sg.Text(" | "), sg.Input(str(board.array[0][3]), key="03", size=(1, 1)), sg.Input(str(board.array[0][4]), key="04", size=(1, 1)), sg.Input(str(board.array[0][5]), key="05", size=(1, 1)), sg.Text(" | "), sg.Input(str(board.array[0][6]), key="06", size=(1, 1)), sg.Input(str(board.array[0][7]), key="07", size=(1, 1)), sg.Input(str(board.array[0][8]), key="08", size=(1, 1))],
            [sg.Input(str(board.array[1][0]), key="10", size=(1, 1)), sg.Input(str(board.array[1][1]), key="11", size=(1, 1)), sg.Input(str(board.array[1][2]), key="12", size=(1, 1)), sg.Text(" | "), sg.Input(str(board.array[1][3]), key="13", size=(1, 1)), sg.Input(str(board.array[1][4]), key="14", size=(1, 1)), sg.Input(str(board.array[1][5]), key="15", size=(1, 1)), sg.Text(" | "), sg.Input(str(board.array[1][6]), key="16", size=(1, 1)), sg.Input(str(board.array[1][7]), key="17", size=(1, 1)), sg.Input(str(board.array[1][8]), key="18", size=(1, 1))],
            [sg.Input(str(board.array[2][0]), key="20", size=(1, 1)), sg.Input(str(board.array[2][1]), key="21", size=(1, 1)), sg.Input(str(board.array[2][2]), key="22", size=(1, 1)), sg.Text(" | "), sg.Input(str(board.array[2][3]), key="23", size=(1, 1)), sg.Input(str(board.array[2][4]), key="24", size=(1, 1)), sg.Input(str(board.array[2][5]), key="25", size=(1, 1)), sg.Text(" | "), sg.Input(str(board.array[2][6]), key="26", size=(1, 1)), sg.Input(str(board.array[2][7]), key="27", size=(1, 1)), sg.Input(str(board.array[2][8]), key="28", size=(1, 1))],
            [sg.Text("-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --")],
            [sg.Input(str(board.array[3][0]), key="30", size=(1, 1)), sg.Input(str(board.array[3][1]), key="31", size=(1, 1)), sg.Input(str(board.array[3][2]), key="32", size=(1, 1)), sg.Text(" | "), sg.Input(str(board.array[3][3]), key="33", size=(1, 1)), sg.Input(str(board.array[3][4]), key="34", size=(1, 1)), sg.Input(str(board.array[3][5]), key="35", size=(1, 1)), sg.Text(" | "), sg.Input(str(board.array[3][6]), key="36", size=(1, 1)), sg.Input(str(board.array[3][7]), key="37", size=(1, 1)), sg.Input(str(board.array[3][8]), key="38", size=(1, 1))],
            [sg.Input(str(board.array[4][0]), key="40", size=(1, 1)), sg.Input(str(board.array[4][1]), key="41", size=(1, 1)), sg.Input(str(board.array[4][2]), key="42", size=(1, 1)), sg.Text(" | "), sg.Input(str(board.array[4][3]), key="43", size=(1, 1)), sg.Input(str(board.array[4][4]), key="44", size=(1, 1)), sg.Input(str(board.array[4][5]), key="45", size=(1, 1)), sg.Text(" | "), sg.Input(str(board.array[4][6]), key="46", size=(1, 1)), sg.Input(str(board.array[4][7]), key="47", size=(1, 1)), sg.Input(str(board.array[4][8]), key="48", size=(1, 1))],
            [sg.Input(str(board.array[5][0]), key="50", size=(1, 1)), sg.Input(str(board.array[5][1]), key="51", size=(1, 1)), sg.Input(str(board.array[5][2]), key="52", size=(1, 1)), sg.Text(" | "), sg.Input(str(board.array[5][3]), key="53", size=(1, 1)), sg.Input(str(board.array[5][4]), key="54", size=(1, 1)), sg.Input(str(board.array[5][5]), key="55", size=(1, 1)), sg.Text(" | "), sg.Input(str(board.array[5][6]), key="56", size=(1, 1)), sg.Input(str(board.array[5][7]), key="57", size=(1, 1)), sg.Input(str(board.array[5][8]), key="58", size=(1, 1))],
            [sg.Text("-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --")],
            [sg.Input(str(board.array[6][0]), key="60", size=(1, 1)), sg.Input(str(board.array[6][1]), key="61", size=(1, 1)), sg.Input(str(board.array[6][2]), key="62", size=(1, 1)), sg.Text(" | "), sg.Input(str(board.array[6][3]), key="63", size=(1, 1)), sg.Input(str(board.array[6][4]), key="64", size=(1, 1)), sg.Input(str(board.array[6][5]), key="65", size=(1, 1)), sg.Text(" | "), sg.Input(str(board.array[6][6]), key="66", size=(1, 1)), sg.Input(str(board.array[6][7]), key="67", size=(1, 1)), sg.Input(str(board.array[6][8]), key="68", size=(1, 1))],
            [sg.Input(str(board.array[7][0]), key="70", size=(1, 1)), sg.Input(str(board.array[7][1]), key="71", size=(1, 1)), sg.Input(str(board.array[7][2]), key="72", size=(1, 1)), sg.Text(" | "), sg.Input(str(board.array[7][3]), key="73", size=(1, 1)), sg.Input(str(board.array[7][4]), key="74", size=(1, 1)), sg.Input(str(board.array[7][5]), key="75", size=(1, 1)), sg.Text(" | "), sg.Input(str(board.array[7][6]), key="76", size=(1, 1)), sg.Input(str(board.array[7][7]), key="77", size=(1, 1)), sg.Input(str(board.array[7][8]), key="78", size=(1, 1))],
            [sg.Input(str(board.array[8][0]), key="80", size=(1, 1)), sg.Input(str(board.array[8][1]), key="81", size=(1, 1)), sg.Input(str(board.array[8][2]), key="82", size=(1, 1)), sg.Text(" | "), sg.Input(str(board.array[8][3]), key="83", size=(1, 1)), sg.Input(str(board.array[8][4]), key="84", size=(1, 1)), sg.Input(str(board.array[8][5]), key="85", size=(1, 1)), sg.Text(" | "), sg.Input(str(board.array[8][6]), key="86", size=(1, 1)), sg.Input(str(board.array[8][7]), key="87", size=(1, 1)), sg.Input(str(board.array[8][8]), key="88", size=(1, 1))],
        ]
        )],
        [sg.Text("Last Position: ( " + str(pos[0]) + ", " + str(pos[1]) + " )", key="-POSITION-")],
    ]

    window = sg.Window('Sudoku', layout, location=(500, 500))

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break


        # If event triggered for any position
            # If new number is same as number in solution
                # Change new number color to green
            # Else
                # Change new number color to red

        # If board is full and solution is correct
            # Send popup with timestamp and congratulations message

main()

# if __name__ == "__main__":
#     cProfile.run("main()")

#     layout = [
#         [sg.Table(board.array, justification="center", key="-BOARD-", visible_column_map=[True]*Board.cols)],
#         [sg.Text("Row: " + str(pos[0]) + "\n" + "Column: " + str(pos[1]), key="-POSITION-")],
#     ]
#
#     window = sg.Window('Sudoku', layout)
#
#     while True:
#         event, values = window.read()
#         if event == sg.WIN_CLOSED:
#             break
#         if event == "-BOARD-":
#             window["-POSITION-"].update("Row: " + str(values["-BOARD-"]) + "\n" + "Column: " + str(pos[1]))
