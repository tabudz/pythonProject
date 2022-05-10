from math import floor


class ChessBox:
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    status = 0
    back_ground = "white"
    border = "black"
    deg_nw = 0
    deg_n = 0
    deg_ne = 0
    deg_e = 0
    deg_se = 0
    deg_s = 0
    deg_sw = 0
    deg_w = 0
    score = 0

    def __init__(self, x1, y1, x2, y2, cas):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.status = 0
        self.shape = []
        cas.create_rectangle(x1, y1, x2, y2, outline=self.border, fill=self.back_ground)

    def draw_chess(self, cas, turn):
        if self.status == 0:
            d = (self.x2 - self.x1) / 4
            if turn == -1:
                self.shape.append(cas.create_oval(self.x1 + d, self.y1 + d, self.x2 - d, self.y2 - d))
                self.status = -1
            else:
                self.shape.append(cas.create_line(self.x1 + d, self.y1 + d, self.x2 - d, self.y2 - d))
                self.shape.append(cas.create_line(self.x2 - d, self.y1 + d, self.x1 + d, self.y2 - d))
                self.status = 1
            turn = -turn
        return turn

    def delete_chess(self, cas):
        if self.status == -1:
            cas.delete(self.shape[-1])
        if self.status == 1:
            cas.delete(self.shape[-1])
            cas.delete(self.shape[-2])
        self.status = 0

    def update_score(self):
        self.score = floor(4 ** (self.deg_n - 1)) + floor(4 ** (self.deg_s - 1)) + floor(4 ** (self.deg_w - 1)) + floor(4 ** (self.deg_e - 1)) + \
                     floor(4 ** (self.deg_nw - 1)) + floor(4 ** (self.deg_ne - 1)) + floor(4 ** (self.deg_sw - 1)) + floor(4 ** (self.deg_se - 1))

