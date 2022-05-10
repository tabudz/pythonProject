from display.chessboard import *
from tkinter import *


class MiniMax:
    cas = Canvas()
    chess_board = ChessBoard(cas, 9)
    score_x = 0
    score_y = 0

    def __init__(self, chess_board):
        self.chess_board = chess_board

    def weight(self, x):
        t = min(x, self.chess_board.line) % self.chess_board.line
        if t:
            return 4 ** (t - 1)
        else:
            return 0

    def value_function(self, x, y):
        if y:
            return 1 - 2 ** (-x / y)
        else:
            return 1

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

    def update_deg(self, i, j):
        status = self.chess_board.box_array[i][j].status
        score_1 = 0
        score_2 = 0
        x = i - 1
        y = j - 1
        count_nw = 1
        count_se = 1
        x_nw = -1
        y_nw = -1
        t = 0
        continuous = 1
        while x >= 0 and y >= 0:
            space = 0
            if self.chess_board.box_array[x][y].status == status:
                if continuous:
                    score_1 -= self.weight(self.chess_board.box_array[x][y].deg_se)
                    self.chess_board.box_array[x][y].deg_se = 0
                    self.chess_board.box_array[i][j].deg_nw = 0
                    count_nw += 1
                else:
                    x_nw = x
                    y_nw = y
                    break
            if self.chess_board.box_array[x][y].status == 0:
                continuous = 0
                space += 1
                if space == 2:
                    x_nw = x + 2
                    y_nw = y + 2
                    t = 1
                    break
            if self.chess_board.box_array[x][y].status == - status:
                if space:
                    x_nw = x + 2
                    y_nw = y + 2
                    t = 1
                else:
                    score_2 -= self.weight(self.chess_board.box_array[x][y].deg_se)
                    self.chess_board.box_array[x][y].deg_se = 0
                    self.chess_board.box_array[i][j].deg_nw = 0
                break
            x -= 1
            y -= 1

        x = i + 1
        y = j + 1
        continuous = 1
        while x < self.chess_board.box and y < self.chess_board.box:
            space = 0
            if self.chess_board.box_array[x][y].status == status:
                if continuous:
                    score_1 = self.weight(self.chess_board.box_array[x][y].deg_nw)
                    self.chess_board.box_array[x][y].deg_nw = 0
                    self.chess_board.box_array[i][j].deg_se = 0
                    count_se += 1
                else:
                    score_1 -= self.weight(self.chess_board.box_array[x - 2][y - 2].deg_se)
                    self.chess_board.box_array[x - 2][y - 2].deg_se = self.chess_board.box_array[x][y].deg_se + count_nw
                    score_1 += self.weight(self.chess_board.box_array[x - 2][y - 2].deg_se)
                    break
            if self.chess_board.box_array[x][y].status == 0:
                continuous = 0
                space += 1
                if space >= 2:
                    score_1 -= self.weight(self.chess_board.box_array[x][y].deg_se)
                    self.chess_board.box_array[x - 2][y - 2].deg_se = count_nw + count_se - 1
                    score_1 += self.weight(count_nw + count_se - 1)
                    break
            if self.chess_board.box_array[x][y].status == - status:
                if space == 0:
                    score_2 -= self.weight(self.chess_board.box_array[x][y].deg_nw)
                    self.chess_board.box_array[x][y].deg_nw = 0
                    self.chess_board.box_array[i][j].deg_se = 0
                else:
                    self.chess_board.box_array[i][j].deg_se = count_nw + count_se - 1
                    score_1 += self.weight(count_nw + count_se - 1)
                break
            x += 1
            y += 1
        if x_nw >= 0:
            if t:
                score_1 -= self.weight(self.chess_board.box_array[x_nw][y_nw].deg_nw)
                self.chess_board.box_array[x_nw][y_nw].deg_nw = count_nw + count_se - 1
                score_1 += self.weight(count_nw + count_se - 1)
            else:
                score_1 -= self.weight(self.chess_board.box_array[x_nw][y_nw].deg_se)
                self.chess_board.box_array[x_nw][y_nw].deg_se = self.chess_board.box_array[x_nw][y_nw].deg_se + count_se
                score_1 += self.weight(self.chess_board.box_array[x_nw][y_nw].deg_se)

        x = i + 1
        y = j - 1
        count_ne = 1
        count_sw = 1
        x_ne = -1
        y_ne = -1
        t = 0
        continuous = 1
        while x < self.chess_board.box and y >= 0:
            space = 0
            if self.chess_board.box_array[x][y].status == status:
                if continuous:
                    score_1 -= self.weight(self.chess_board.box_array[x][y].deg_sw)
                    self.chess_board.box_array[x][y].deg_sw = 0
                    self.chess_board.box_array[i][j].deg_ne = 0
                    count_ne += 1
                else:
                    x_ne = x
                    y_ne = y
                    break
            if self.chess_board.box_array[x][y].status == 0:
                continuous = 0
                space += 1
                if space == 2:
                    x_ne = x - 2
                    y_ne = y + 2
                    t = 1
                    break
            if self.chess_board.box_array[x][y].status == - status:
                if space:
                    x_ne = x - 2
                    y_ne = y + 2
                    t = 1
                else:
                    score_2 -= self.weight(self.chess_board.box_array[x][y].deg_sw)
                    self.chess_board.box_array[x][y].deg_sw = 0
                    self.chess_board.box_array[i][j].deg_ne = 0
                break
            x += 1
            y -= 1

        x = i - 1
        y = j + 1
        continuous = 1
        while x >= 0 and y < self.chess_board.box:
            space = 0
            if self.chess_board.box_array[x][y].status == status:
                if continuous:
                    score_1 -= self.weight(self.chess_board.box_array[x][y].deg_se)
                    self.chess_board.box_array[x][y].deg_ne = 0
                    self.chess_board.box_array[i][j].deg_sw = 0
                    count_sw += 1
                else:
                    score_1 -= self.weight(self.chess_board.box_array[x + 2][y - 2].deg_sw)
                    self.chess_board.box_array[x + 2][y - 2].deg_sw = self.chess_board.box_array[x][y].deg_ne + count_ne
                    score_1 += self.weight(self.chess_board.box_array[x - 2][y - 2].deg_sw)
                    break
            if self.chess_board.box_array[x][y].status == 0:
                continuous = 0
                space += 1
                if space >= 2:
                    score_1 -= self.weight(self.chess_board.box_array[x + 2][y - 2].deg_se)
                    self.chess_board.box_array[x + 2][y - 2].deg_sw = count_ne + count_sw - 1
                    score_1 += self.weight(count_ne + count_sw - 1)
                    break
            if self.chess_board.box_array[x][y].status == - status:
                if space == 0:
                    score_2 -= self.weight(self.chess_board.box_array[x][y].deg_ne)
                    self.chess_board.box_array[x][y].deg_ne = 0
                    self.chess_board.box_array[i][j].deg_sw = 0
                else:
                    self.chess_board.box_array[i][j].deg_sw = count_ne + count_sw - 1
                    score_1 += self.weight(count_ne + count_sw - 1)
                break
            x -= 1
            y += 1
        if x_ne >= 0:
            if t:
                score_1 -= self.weight(self.chess_board.box_array[x_ne][y_ne].deg_ne)
                self.chess_board.box_array[x_ne][y_ne].deg_ne = count_ne + count_sw - 1
                score_1 += self.weight(count_ne + count_sw - 1)
            else:
                score_1 -= self.weight(self.chess_board.box_array[x_ne][y_ne].deg_sw)
                self.chess_board.box_array[x_ne][y_ne].deg_sw = self.chess_board.box_array[x_ne][y_ne].deg_sw + count_sw
                score_1 += self.weight(self.chess_board.box_array[x_ne][y_ne].deg_sw)

        x = i - 1
        count_w = 1
        count_e = 1
        x_w = -1
        t = 0
        continuous = 1
        while x >= 0:
            space = 0
            if self.chess_board.box_array[x][j].status == status:
                if continuous:
                    score_1 -= self.weight(self.chess_board.box_array[x][j].deg_e)
                    self.chess_board.box_array[x][j].deg_e = 0
                    self.chess_board.box_array[i][j].deg_w = 0
                    count_w += 1
                else:
                    x_w = x
                    break
            if self.chess_board.box_array[x][j].status == 0:
                continuous = 0
                space += 1
                if space == 2:
                    x_w = x + 2
                    t = 1
                    break
            if self.chess_board.box_array[x][j].status == - status:
                if space:
                    x_w = x + 2
                    t = 1
                else:
                    score_2 -= self.weight(self.chess_board.box_array[x][j].deg_e)
                    self.chess_board.box_array[x][j].deg_e = 0
                    self.chess_board.box_array[i][j].deg_w = 0
                break
            x -= 1

        x = i + 1
        continuous = 1
        while x < self.chess_board.box:
            space = 0
            if self.chess_board.box_array[x][j].status == status:
                if continuous:
                    score_1 -= self.weight(self.chess_board.box_array[x][j].deg_w)
                    self.chess_board.box_array[x][j].deg_w = 0
                    self.chess_board.box_array[i][j].deg_e = 0
                    count_w += 1
                else:
                    score_1 -= self.weight(self.chess_board.box_array[x - 2][j].deg_e)
                    self.chess_board.box_array[x - 2][j].deg_e = self.chess_board.box_array[x][j].deg_w + count_w
                    score_1 += self.weight(self.chess_board.box_array[x - 2][j].deg_e)
                    break
            if self.chess_board.box_array[x][y].status == 0:
                continuous = 0
                space += 1
                if space >= 2:
                    score_1 -= self.weight(self.chess_board.box_array[x - 2][j].deg_e)
                    self.chess_board.box_array[x - 2][j].deg_e = count_w + count_e - 1
                    score_1 += self.weight(count_w + count_e - 1)
                    break
            if self.chess_board.box_array[x][j].status == - status:
                if space == 0:
                    score_2 -= self.weight(self.chess_board.box_array[x][j].deg_w)
                    self.chess_board.box_array[x][j].deg_w = 0
                    self.chess_board.box_array[i][j].deg_e = 0
                else:
                    self.chess_board.box_array[i][j].deg_e = count_w + count_e - 1
                    score_1 += self.weight(count_w + count_e - 1)
                break
            x += 1
        if x_w >= 0:
            if t:
                score_1 -= self.weight(self.chess_board.box_array[x_w][j].deg_w)
                self.chess_board.box_array[x_w][j].deg_w = count_w + count_e - 1
                score_1 += self.weight(count_w + count_e - 1)
            else:
                score_1 -= self.weight(self.chess_board.box_array[x_w][j].deg_e)
                self.chess_board.box_array[x_w][j].deg_e = self.chess_board.box_array[x_w][j].deg_e + count_e
                score_1 += self.weight(self.chess_board.box_array[x_w][j].deg_e)

        y = j - 1
        count_n = 1
        count_s = 1
        y_n = -1
        t = 0
        continuous = 1
        while y >= 0:
            space = 0
            if self.chess_board.box_array[i][y].status == status:
                if continuous:
                    score_1 -= self.weight(self.chess_board.box_array[i][y].deg_s)
                    self.chess_board.box_array[i][y].deg_s = 0
                    self.chess_board.box_array[i][j].deg_n = 0
                    count_n += 1
                else:
                    y_n = y
                    break
            if self.chess_board.box_array[i][y].status == 0:
                continuous = 0
                space += 1
                if space == 2:
                    y_n = y + 2
                    t = 1
                    break
            if self.chess_board.box_array[i][y].status == - status:
                if space:
                    y_n = y + 2
                    t = 1
                else:
                    score_2 -= self.weight(self.chess_board.box_array[i][y].deg_s)
                    self.chess_board.box_array[i][y].deg_s = 0
                    self.chess_board.box_array[i][j].deg_n = 0
                break
            y -= 1

        y = j + 1
        continuous = 1
        while y < self.chess_board.box:
            space = 0
            if self.chess_board.box_array[i][y].status == status:
                if continuous:
                    score_1 -= self.weight(self.chess_board.box_array[i][y].deg_n)
                    self.chess_board.box_array[i][y].deg_n = 0
                    self.chess_board.box_array[i][j].deg_s = 0
                    count_s += 1
                else:
                    score_1 -= self.weight(self.chess_board.box_array[i][y - 2].deg_s)
                    self.chess_board.box_array[i][y - 2].deg_s = self.chess_board.box_array[i][y - 2].deg_s + count_n
                    score_1 -= self.weight(self.chess_board.box_array[i][y - 2].deg_s)
                    break
            if self.chess_board.box_array[i][y].status == 0:
                continuous = 0
                space += 1
                if space >= 2:
                    score_1 -= self.weight(self.chess_board.box_array[i][y - 2].deg_s)
                    self.chess_board.box_array[i][y - 2].deg_s = count_n + count_s - 1
                    score_1 += self.weight(self.chess_board.box_array[i][y - 2].deg_s)
                    break
            if self.chess_board.box_array[i][y].status == - status:
                if space == 0:
                    score_2 -= self.weight(self.chess_board.box_array[i][y].deg_n)
                    self.chess_board.box_array[i][y].deg_n = 0
                    self.chess_board.box_array[i][j].deg_s = 0
                else:
                    self.chess_board.box_array[i][j].deg_s = count_n + count_s - 1
                    score_1 += self.weight(self.chess_board.box_array[i][j].deg_s)
                break
            y += 1
        if y_n >= 0:
            if t:
                score_1 -= self.weight(self.chess_board.box_array[i][y_n].deg_n)
                self.chess_board.box_array[i][y_n].deg_n = count_n + count_s - 1
                score_1 += self.weight(self.chess_board.box_array[i][y_n].deg_n)
            else:
                score_1 -= self.weight(self.chess_board.box_array[i][y_n].deg_s)
                self.chess_board.box_array[i][y_n].deg_s = self.chess_board.box_array[i][y_n] + count_s
                score_1 += self.weight(self.chess_board.box_array[i][y_n].deg_s)

        return score_1, score_2

    def return_value(self, i, j):
        status = self.chess_board.box_array[i][j].status
        score_1 = 0
        score_2 = 0
        x = i - 1
        y = j - 1
        count_nw = 1
        count_se = 1
        count_o_nw = 0
        x_nw = -1
        y_nw = -1
        t = 0
        continuous = 1
        while x >= 0 and y >= 0:
            space = 0
            if self.chess_board.box_array[x][y].status == status:
                if continuous:
                    count_nw += 1
                else:
                    x_nw = x
                    y_nw = y
                    break
            if self.chess_board.box_array[x][y].status == 0:
                continuous = 0
                space += 1
                if space == 2:
                    x_nw = x + 2
                    y_nw = y + 2
                    t = 1
                    break
            if self.chess_board.box_array[x][y].status == - status:
                continuous = 0
                if space:
                    x_nw = x + 2
                    y_nw = y + 2
                    t = 1
                else:
                    count_o_nw += 1
            x -= 1
            y -= 1

        x = i + 1
        y = j + 1
        continuous = 1
        while x < self.chess_board.box and y < self.chess_board.box:
            space = 0
            if self.chess_board.box_array[x][y].status == status:
                if continuous:
                    score_1 = self.weight(self.chess_board.box_array[x][y].deg_nw)
                    self.chess_board.box_array[x][y].deg_nw = 0
                    self.chess_board.box_array[i][j].deg_se = 0
                    count_se += 1
                else:
                    score_1 -= self.weight(self.chess_board.box_array[x - 2][y - 2].deg_se)
                    self.chess_board.box_array[x - 2][y - 2].deg_se = self.chess_board.box_array[x][y].deg_se + count_nw
                    score_1 += self.weight(self.chess_board.box_array[x - 2][y - 2].deg_se)
                    break
            if self.chess_board.box_array[x][y].status == 0:
                continuous = 0
                space += 1
                if space >= 2:
                    score_1 -= self.weight(self.chess_board.box_array[x][y].deg_se)
                    self.chess_board.box_array[x - 2][y - 2].deg_se = count_nw + count_se - 1
                    score_1 += self.weight(count_nw + count_se - 1)
                    break
            if self.chess_board.box_array[x][y].status == - status:
                if space == 0:
                    score_2 -= self.weight(self.chess_board.box_array[x][y].deg_nw)
                    self.chess_board.box_array[x][y].deg_nw = 0
                    self.chess_board.box_array[i][j].deg_se = 0
                else:
                    self.chess_board.box_array[i][j].deg_se = count_nw + count_se - 1
                    score_1 += self.weight(count_nw + count_se - 1)
                break
            x += 1
            y += 1
        if x_nw >= 0:
            if t:
                score_1 -= self.weight(self.chess_board.box_array[x_nw][y_nw].deg_nw)
                self.chess_board.box_array[x_nw][y_nw].deg_nw = count_nw + count_se - 1
                score_1 += self.weight(count_nw + count_se - 1)
            else:
                score_1 -= self.weight(self.chess_board.box_array[x_nw][y_nw].deg_se)
                self.chess_board.box_array[x_nw][y_nw].deg_se = self.chess_board.box_array[x_nw][y_nw].deg_se + count_se
                score_1 += self.weight(self.chess_board.box_array[x_nw][y_nw].deg_se)

    def update_value(self, i, j):


