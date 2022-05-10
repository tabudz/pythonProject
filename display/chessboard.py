from display.chessbox import *


class ChessBoard:
    x = 30
    y = 30
    length = 30
    box = 9
    box_array = []
    line = 5
    turn = 1
    history = []

    def __init__(self, cas, box):
        self.box = box
        for i in range(self.box):
            row = []
            for j in range(self.box):
                x = self.x + i * self.length
                y = self.y + j * self.length
                row.append(ChessBox(x, y, x + self.length, y + self.length, cas))
            self.box_array.append(row)

    def check(self, x, y):
        i = (x - self.x) // self.length
        j = (y - self.y) // self.length
        return i, j

    def click(self, cas, i, j):
        if i in range(self.box) and j in range(self.box):
            turn = self.box_array[i][j].draw_chess(cas, self.turn)
            if turn != 0:
                self.turn = turn

    def check_win(self, i, j):
        temp1 = 0
        i1 = i - 1
        j1 = j
        while i1 >= 0:
            if self.box_array[i1][j1].status == self.turn:
                temp1 += 1
                i1 -= 1
            else:
                break
        i1 = i + 1
        while i1 < self.box:
            if self.box_array[i1][j1].status == self.turn:
                temp1 += 1
                i1 += 1
            else:
                break
        temp2 = 0
        i1 = i
        j1 = j - 1
        while j1 >= 0:
            if self.box_array[i1][j1].status == self.turn:
                temp2 += 1
                j1 -= 1
            else:
                break
        j1 = j + 1
        while j1 < self.box:
            if self.box_array[i1][j1].status == self.turn:
                temp2 += 1
                j1 += 1
            else:
                break
        temp3 = 0
        i1 = i - 1
        j1 = j - 1
        while i1 >= 0 and j1 >= 0:
            if self.box_array[i1][j1].status == self.turn:
                temp3 += 1
                i1 -= 1
                j1 -= 1
            else:
                break
        i1 = i + 1
        j1 = j + 1
        while i1 < self.box and j1 < self.box:
            if self.box_array[i1][j1].status == self.turn:
                temp3 += 1
                i1 += 1
                j1 += 1
            else:
                break
        temp4 = 0
        i1 = i - 1
        j1 = j + 1
        while i1 >= 0 and j1 < self.box:
            if self.box_array[i1][j1].status == self.turn:
                temp4 += 1
                i1 -= 1
                j1 += 1
            else:
                break
        i1 = i + 1
        j1 = j - 1
        while i1 < self.box and j1 >= 0:
            if self.box_array[i1][j1].status == self.turn:
                temp4 += 1
                i1 += 1
                j1 -= 1
            else:
                break
        count = max(temp1, temp2, temp3, temp4)
        return (count == self.line - 1) * self.turn

    def fake_click(self, i, j):
        if i in range(self.box) and j in range(self.box) and self.box_array[i][j].status == 0:
            self.box_array[i][j].status = self.turn
            self.turn = -self.turn

    def fake_delete_chess(self, i, j):
        self.box_array[i][j].status = 0
        self.turn = -self.turn

    def delete_chess(self, cas, i, j):
        self.box_array[i][j].delete_chess(cas)
        self.turn = -self.turn
