from tkinter import *
from Minimax import minimax
# add option to increase or decrease depth/difficulty of ai

H, W = 80, 80


class con4:
    def __init__(self, ai):
        self.ai = ai
        self.pos = []

        self.root = Tk()
        self.root.title('Connect 4')

        self.turns = {'blue': 'yellow', 'yellow': 'blue'}
        self.turn = 'blue'
        
        self.cnv = Canvas(self.root, height=H*6, width=W*7, bg='light blue')
        self.cnv.grid(row=0, column=0)

        self.coins = []
        
        for i in range(6):
            self.coins.append([])
            self.pos.append([])
            for j in range(7):
                self.coins[i].append(0)
                self.pos[i].append(0)
                self.cnv.create_oval(j*H, i*W, (j*H)+H, (i*W)+W, fill='white')
        
        e = Button(self.root, text='Exit', height=3, width=5, command=self.root.destroy)
        e.grid(row=2, column=0)

        self.mn = 0
        self.dropping = False

        self.root.bind('<Button-1>', self.click)

    def click(self, e):
        if not self.dropping:
            c = e.x//H
            print(c)
            print()

            if self.coins[0][c] == 0:
                move = [self.cnv.create_oval(c*W, 0, (c*W)+W, H, fill=self.turn), self.turn]
                self.drop(c, move)
                self.mn += 1

                end = False
                if self.mn >= 7:
                    if self.checkWin(self.turn):
                        self.root.unbind('<Button-1>')
                        end = True
                        Label(self.root, text=self.turn + ' won!!', height=3, width=30).grid(row=1, column=0)
                self.turn = self.turns[self.turn]
                self.dropping = False

                if self.ai and (not end):
                    # blue = maximizing Player and yellow = minimizing Player ig
                    aimove = minimax(self.pos, 5, -10, 10, False, True)
                    print()
                    print('score', aimove[0])
                    print('aimove', aimove[1])
                    for row in range(6):
                        for col in range(7):
                            if aimove[1][row][col] != self.pos[row][col]:
                                move = [self.cnv.create_oval(col*W, 0, (col*W)+W, H, fill=self.turn), self.turn]
                                self.drop(col, move)
                                self.mn += 1

                                if self.mn >= 7:
                                    if self.checkWin(self.turn):
                                        self.root.unbind('<Button-1>')
                                        Label(self.root, text=self.turn + ' won!!', height=3, width=30).grid(row=1,
                                                                                                             column=0)
                                self.turn = self.turns[self.turn]
                                self.dropping = False
                                break
                        else:
                            continue
                        break

    def checkWin(self, side):
        for r in range(len(self.pos)):
            for c in range(len(self.pos[r])):
                if self.pos[r][c] == side:
                    # check if connected to 4 on
                    # down
                    # right
                    # downright and downleft
                    if c <= 3:
                        for rs in range(c+1, c+4):
                            if self.pos[r][rs] != side:
                                break
                        else:
                            self.cnv.create_rectangle(c*H, r*H, (c*H)+(4*H), (r*H)+H, outline='red')
                            return True

                    if r <= 2:
                        for ds in range(r+1, r+4):
                            if self.pos[ds][c] != side:
                                break
                        else:
                            self.cnv.create_rectangle(c*H, r*H, (c*H)+H, (r*H)+(4*H), outline='red')
                            return True

                        if c <= 3:
                            for dr in range(1, 4):
                                if self.pos[r+dr][c+dr] != side:
                                    break
                            else:
                                self.cnv.create_line((c*H)+(H//2), r*H, c*H, (r*H)+(H//2), fill='red')
                                self.cnv.create_line((c*H)+(H//2), r*H, (c*H)+(4*H), (r*H)+(3*H)+(H//2), fill='red')
                                self.cnv.create_line((c*H)+(4*H), (r*H)+(3*H)+(H//2), (c*H)+(3*H)+(H//2), (r*H)+(4*H), fill='red')
                                self.cnv.create_line(c*H, (r*H)+(H//2), (c*H)+(3*H)+(H//2), (r*H)+(4*H), fill='red')
                                return True

                        if c >= 3:
                            for dl in range(-1, -4, -1):
                                if self.pos[r-dl][c+dl] != side:
                                    break
                            else:
                                self.cnv.create_line((c*H)+(H//2), r*H, (c*H)+H, (r*H)+(H//2), fill='red')
                                self.cnv.create_line((c*H)+(H//2), r*H, (c*H)-(3*H), (r*H)+(3*H)+(H//2), fill='red')
                                self.cnv.create_line((c*H)-(3*H), (r*H)+(3*H)+(H//2), (c*H)-(2*H)-(H//2), (r*H)+(4*H), fill='red')
                                self.cnv.create_line((c*H)+H, (r*H)+(H//2), (c*H)-(2*H)-(H//2), (r*H)+(4*H), fill='red')
                                return True

        return False

    def drop(self, c, move):
        # pps has to be divisible with H
        self.dropping = True
        pps = 10
        for i in range(1, 6):
            if self.coins[i][c] == 0:
                for f in range(H//pps):
                    self.cnv.move(move[0], 0, pps)
                    self.cnv.update()
            else:
                self.coins[i-1][c] = move
                self.pos[i-1][c] = move[1]
                break

            if i == 5:
                self.coins[5][c] = move
                self.pos[5][c] = move[1]

        print()
        for r in self.pos:
            for j in r:
                print(j, end=' ')
            print()
        print()


if __name__ == '__main__':

    def start(ai):
        root.destroy()
        obj = con4(ai)
        obj.root.mainloop()

    root = Tk()
    root.title('Connect 4')

    q = Label(root, text='Would you like to play against the AI or another player?', height=3, width=40)
    q.grid(row=0, column=0, columnspan=2)

    aib = Button(root, text='AI', height=4, width=20, command=lambda:start(True))
    aib.grid(row=1, column=0)

    apb = Button(root, text='Another player', height=4, width=20, command=lambda:start(False))
    apb.grid(row=1, column=1)

    root.mainloop()
    #
    # pos = []
    # for i in range(6):
    #     pos.append([])
    #     for j in range(7):
    #         pos[i].append(0)
    #
    # for a in range(4):
    #     pos[5][a] = 'blue'
    #
    # print(checkWin(pos, False))
