from tkinter import messagebox
from display.chessboard import *
from tkinter import *


tk = Tk()
cas = Canvas(tk, height=500, width=600)
cas.pack()
chessBoard = ChessBoard(cas)


def click(event):
    i, j = chessBoard.check(event.x, event.y)
    if chessBoard.box_array[i][j].status == 0:
        check = chessBoard.check_win(i, j)
        chessBoard.click(cas, i, j)
        if check == 1:
            messagebox.showinfo("Game over", "Player 1 win")
        if check == -1:
            messagebox.showinfo("Game over", "Player 2 win")
    else:
        chessBoard.delete_chess(cas, i, j)


cas.bind_all('<Button-1>', click)
tk.mainloop()
