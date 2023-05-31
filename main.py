from tkinter import *
import time
import random
from piece import Piece
from playsound import playsound
# import PyObjC
import threading

# add
# decrease self.wait as score increases

# bugs
# game doesn't end properly(pieces pile on the same top lines for a second before ending)
# sometimes late in the game, lines don't clear properly

H, W = 20, 10
scl = 35


class Tetris:
    def __init__(self, ai=False):
        self.root = Tk()
        self.root.title('Tetris')
        
        self.wait = 0.3
        self.oldwait = 0

        self.ai = ai

        self.heldPiece = 0

        self.game = Canvas(self.root, height=H*scl, width=W*scl)
        self.game.grid(row=0, column=3)

        Label(self.root, height=13, width=4).grid(row=0, column=2)
        self.info = Frame(self.root, height=17, width=13)
        self.info.grid(row=0, column=1)
        self.holdLabel = Frame(self.info, height=80, width=80, highlightbackground='grey', highlightthickness=5)
        self.holdLabel.grid(row=8, column=0)
        Label(self.root, height=13, width=4).grid(row=0, column=0)

        self.grid = []
        for i in range(H):
            self.grid.append([])
            for j in range(W):
                self.game.create_rectangle(j*scl, i*scl, (j*scl)+scl, (i*scl)+scl, fill='black', outline='grey')
                self.grid[i].append(0)

        e = Button(self.root, text='Exit', height=3, width=7, command=self.root.destroy)
        e.grid(row=1, column=3)

        # if not ai:
        yoff = int(self.root.winfo_screenwidth()/2 - self.root.winfo_reqwidth())
        self.root.geometry('+{}+{}'.format(yoff, 0))

        p = random.randint(0, 6)
        print(p)
        self.current = Piece(p, self.grid, self.game, scl)
        self.pieces = []
        self.piecesimg = []
        p = self.rannum(self.current.p)
        for i in range(4):
            self.pieces.append(Piece(p, self.grid, self.game, scl))
            p = self.rannum(self.pieces[i].p)
            self.piecesimg.append(Frame(self.info, height=80, width=80, highlightbackground='black', highlightthickness=3))
            self.piecesimg[i].grid(row=i*2, column=0)
            self.makeimg(self.pieces[i], self.piecesimg[i])
            Label(self.info, height=3, width=7).grid(row=(i*2)+1, column=0)

        self.bind()
        self.root.bind("<KeyPress>", self.down)
        self.root.bind("<KeyRelease-Down>", self.release)

        self.current.show()

        # playsound('tetris_theme.m4a', False)

    def rannum(self, n):
        r = random.randint(0, 6)
        while r == n:
            r = random.randint(0, 6)
        return r

    def makeimg(self, p, pframe):
        if p.p == 0:
            Label(pframe, height=1, width=2, bg=p.color).grid(row=0, column=0)
            Label(pframe, height=1, width=2, bg=p.color).grid(row=0, column=1)
            Label(pframe, height=1, width=2, bg=p.color).grid(row=0, column=2)
            Label(pframe, height=1, width=2, bg=p.color).grid(row=0, column=3)
        elif p.p == 1:
            Label(pframe, height=1, width=2, bg=p.color).grid(row=0, column=0)
            Label(pframe, height=1, width=2, bg=p.color).grid(row=0, column=1)
            Label(pframe, height=1, width=2, bg=p.color).grid(row=1, column=0)
            Label(pframe, height=1, width=2, bg=p.color).grid(row=1, column=1)
        elif p.p == 2:
            Label(pframe, height=1, width=2, bg=p.color).grid(row=0, column=1)
            Label(pframe, height=1, width=2, bg=p.color).grid(row=1, column=0)
            Label(pframe, height=1, width=2, bg=p.color).grid(row=1, column=1)
            Label(pframe, height=1, width=2, bg=p.color).grid(row=1, column=2)
        elif p.p == 3:
            Label(pframe, height=1, width=2, bg=p.color).grid(row=0, column=0)
            Label(pframe, height=1, width=2, bg=p.color).grid(row=0, column=1)
            Label(pframe, height=1, width=2, bg=p.color).grid(row=1, column=1)
            Label(pframe, height=1, width=2, bg=p.color).grid(row=2, column=1)
        elif p.p == 4:
            Label(pframe, height=1, width=2, bg=p.color).grid(row=0, column=1)
            Label(pframe, height=1, width=2, bg=p.color).grid(row=1, column=1)
            Label(pframe, height=1, width=2, bg=p.color).grid(row=2, column=1)
            Label(pframe, height=1, width=2, bg=p.color).grid(row=2, column=0)
        elif p.p == 5:
            Label(pframe, height=1, width=2, bg=p.color).grid(row=0, column=0)
            Label(pframe, height=1, width=2, bg=p.color).grid(row=1, column=0)
            Label(pframe, height=1, width=2, bg=p.color).grid(row=1, column=1)
            Label(pframe, height=1, width=2, bg=p.color).grid(row=2, column=1)
        elif p.p == 6:
            Label(pframe, height=1, width=2, bg=p.color).grid(row=0, column=1)
            Label(pframe, height=1, width=2, bg=p.color).grid(row=1, column=1)
            Label(pframe, height=1, width=2, bg=p.color).grid(row=1, column=0)
            Label(pframe, height=1, width=2, bg=p.color).grid(row=2, column=0)
        # for block in p.body:
        #     Label(pframe, height=3, width=5, bg=p.color, relief=SOLID).grid(row=block[1], column=p.x-block[0])

    def delimg(self, pframe):
        for w in pframe.winfo_children():
            w.destroy()

    def newPiece(self):
        self.unbind()
        self.current = self.pieces[0]
        self.current.show()
        self.bind()
        for p in range(1, len(self.pieces)):
            self.pieces[p-1] = self.pieces[p]
            self.delimg(self.piecesimg[p-1])
            self.makeimg(self.pieces[p-1], self.piecesimg[p-1])
        r = self.rannum(self.pieces[2].p)
        self.pieces[3] = Piece(r, self.grid, self.game, scl)
        self.delimg(self.piecesimg[3])
        self.makeimg(self.pieces[3], self.piecesimg[3])

    def holdPiece(self, event):
        for b in self.current.shape:
            self.game.delete(b)
        if self.heldPiece != 0:
            pn = self.current.p
            self.unbind()
            self.current = self.heldPiece
            self.current.show()
            self.bind()
            self.heldPiece = Piece(pn, self.grid, self.game, scl)
            self.delimg(self.holdLabel)
        else:
            self.heldPiece = Piece(self.current.p, self.grid, self.game, scl)
            self.newPiece()
        self.makeimg(self.heldPiece, self.holdLabel)
        
    def unbind(self):
        if not self.ai:
            self.root.unbind("<Left>")
            self.root.unbind("<Right>")
            self.root.unbind("<space>")
            self.root.unbind("z")
            self.root.unbind("<Up>")

    def bind(self):
        if not self.ai:
            self.root.bind("<Left>", self.current.move_left)
            self.root.bind("<Right>", self.current.move_right)
            self.root.bind("<space>", self.current.drop)
            self.root.bind("z", self.current.rotate_left)
            self.root.bind("<Up>", self.current.rotate_right)
            self.root.bind("c", self.holdPiece)

    def down(self, event):
        if event.keysym == 'Down':
            self.oldwait = self.wait
            self.wait = 0.05

    def release(self, event):
        self.wait = self.oldwait

    def start(self):
        while 1:
            u = self.current.update()
            if u == 0:
                self.newPiece()
                for row in self.grid:
                    for b in row:
                        if b != 0:
                            print(1, end=' ')
                        else:
                            print(0, end=' ')
                    print()
                print()
            elif u == -1:
                self.root.destroy()
                print('game over')

            self.game.update()
            time.sleep(self.wait)


def loopTheme():
    while True:
        playsound('tetris_theme.m4a')
        playsound('tetris_theme.m4a')
        playsound('b_theme.m4a')
        playsound('b_theme.m4a')
        playsound('c_theme.m4a')
        playsound('c_theme.m4a')


if __name__ == '__main__':
    theme = threading.Thread(target=loopTheme)
    theme.daemon = True
    theme.start()
    obj = Tetris()
    obj.start()
    obj.root.mainloop()
