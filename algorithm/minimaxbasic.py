from display.chessboard import *
from tkinter import *


class MiniMaxBasic:
    chess_board = ChessBoard(Canvas(), 0)
    scoreX = 0
    scoreY = 0

    def __init__(self, chess_board):
        self.chess_board = chess_board

    def alpha_beta(self, i, j, depth, a, b, maximum, x_min, y_min, x_max, y_max):
        x_node = i
        y_node = j
        x_min_1 = max(0, min(x_min, i - 2))
        y_min_1 = max(0, min(y_min, i - 2))
        x_max_1 = min(self.chess_board.box - 1, max(x_max, i + 2))
        y_max_1 = min(self.chess_board.box - 1, max(y_max, j + 2))
        res = self.chess_board.check_win(i, j)
        self.chess_board.fake_click(i, j)
        if res == -self.chess_board.turn or depth == 0:
            self.chess_board.fake_delete_chess(i, j)
            return -res, x_node, y_node
        if maximum:
            end = 0
            for m in range(x_min_1, x_max_1 + 1):
                for n in range(y_min_1, y_max_1 + 1):
                    if self.chess_board.box_array[m][n].status == 0:
                        end = 1
                        temp = self.alpha_beta(m, n, depth - 1, a, b, False, x_min_1, y_min_1, x_max_1, y_max_1)[0]
                        if temp > a:
                            a = temp
                            x_node = m
                            y_node = n
                        if a >= b:
                            end = 2
                            break
                if end == 2:
                    break
            if end:
                self.chess_board.fake_delete_chess(i, j)
                return a, x_node, y_node
        else:
            end = 0
            for m in range(x_min_1, x_max_1 + 1):
                for n in range(y_min_1, y_max_1 + 1):
                    if self.chess_board.box_array[m][n].status == 0:
                        end = 1
                        temp = self.alpha_beta(m, n, depth - 1, a, b, True, x_min_1, y_min_1, x_max_1, y_max_1)[0]
                        if temp < b:
                            b = temp
                            x_node = m
                            y_node = n
                        if a >= b:
                            end = 2
                            break
                if end == 2:
                    break
            if end:
                self.chess_board.fake_delete_chess(i, j)
                return b, x_node, y_node
        self.chess_board.fake_delete_chess(i, j)
        return 0, x_node, y_node

    def mini_max(self, i, j, depth, maximum, x_min, y_min, x_max, y_max):
        return self.alpha_beta(i, j, depth, -2, 2, maximum, x_min, y_min, x_max, y_max)[-2:]

