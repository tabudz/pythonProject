from algorithm.minimaxbasic import MiniMaxBasic
from tkinter import *

from display.chessboard import ChessBoard

tk = Tk()
cas = Canvas(tk, height=300, width=400)
cas.pack()
box = 9
chess_board = ChessBoard(cas, box)
mini_max = MiniMaxBasic(chess_board)
depth = 5
x_min, y_min = mini_max.chess_board.box - 1, mini_max.chess_board.box - 1
x_max, y_max = 0, 0


def click(event):
    i, j = mini_max.chess_board.check(event.x, event.y)
    if mini_max.chess_board.box_array[i][j].status == 0:
        x, y = mini_max.mini_max(i, j, depth, True, x_min, y_min, x_max, y_max)
        mini_max.chess_board.click(cas, i, j)
        mini_max.chess_board.click(cas, x, y)


cas.bind_all('<Button-1>', click)
tk.mainloop()
