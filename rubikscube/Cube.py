import random
import time
from tkinter import *

PX, PY = 1, 1


class CubeSim:

    def __init__(self):
        self.root = Tk()
        self.root.title("Rubik's Cube")
        self.root['bg'] = 'grey'
        self.colors = ['white', 'orange', 'green', 'red', 'blue', 'yellow']
        self.faces = ['U', 'L', 'F', 'R', 'B', 'D']
        self.corners = [0, 0, 0, 2, 2, 2, 2, 0]
        self.edges = [0, 1, 1, 2, 2, 1, 1, 0]

        H, W = 2, 4
        self.cube = []
        for i in range(6):
            self.cube.append([])
            for j in range(3):
                self.cube[i].append([])
                for k in range(3):
                    self.cube[i][j].append(Label(self.root, height=H, width=W, bg=self.colors[i], relief='raised', borderwidth=2))

        self.root.bind('e', self.keyPressed)
        self.root.bind('r', self.keyPressed)
        self.root.bind('a', self.keyPressed)
        self.root.bind('s', self.keyPressed)
        self.root.bind('d', self.keyPressed)
        self.root.bind('f', self.keyPressed)
        self.root.bind('g', self.keyPressed)
        self.root.bind('h', self.keyPressed)
        self.root.bind('j', self.keyPressed)
        self.root.bind('k', self.keyPressed)
        self.root.bind('c', self.keyPressed)
        self.root.bind('v', self.keyPressed)

        t = "Use e,r,a,s,d,f,g,h,j,k,c,v to turn the cube"
        l = Label(self.root, bg='grey', height=2, width=31, text=t, font=("Arial", 14))
        l.grid(row=8, column=6, columnspan=6)

        self.speedVar = IntVar()

        self.buttons = Frame(self.root, height=445, width=120)
        self.buttons.grid(row=0, column=14, rowspan=11)

        Label(self.root, height=1, width=13, bg='grey').grid(row=10, column=3, columnspan=3)

        e = Button(self.root, text='Exit', height=3, width=11, command=self.root.destroy)
        e.grid(row=11, column=3, columnspan=3)

    def display(self):
        # displaying cube
        for i in range(3):
            for j in range(3):
                self.cube[0][i][j].grid(row=i, column=3+j, padx=PX, pady=PY)

        for i in range(1, 5):
            for j in range(3):
                for k in range(3):
                    self.cube[i][j][k].grid(row=3+j, column=((i-1)*3)+k, padx=PX, pady=PY)

        for i in range(3):
            for j in range(3):
                self.cube[5][i][j].grid(row=6+i, column=3+j, padx=PX, pady=PY)

        Label(self.root, height=22, width=5, bg='grey').grid(row=0, column=13, rowspan=9)

        # displaying self.buttons
        H, W = 2, 1
        u = Button(self.buttons, height=H, width=W, text='U', command=lambda: self.turn('U'))
        u.grid(row=0, column=0, padx=PX, pady=PY)

        ua = Button(self.buttons, height=H, width=W, text="U'", command=lambda: self.turn("U'"))
        ua.grid(row=0, column=1, padx=PX, pady=PY)

        l = Button(self.buttons, height=H, width=W, text='L', command=lambda: self.turn('L'))
        l.grid(row=1, column=0, padx=PX, pady=PY)

        la = Button(self.buttons, height=H, width=W, text="L'", command=lambda: self.turn("L'"))
        la.grid(row=1, column=1, padx=PX, pady=PY)

        f = Button(self.buttons, height=H, width=W, text='F', command=lambda: self.turn('F'))
        f.grid(row=2, column=0, padx=PX, pady=PY)

        fa = Button(self.buttons, height=H, width=W, text="F'", command=lambda: self.turn("F'"))
        fa.grid(row=2, column=1, padx=PX, pady=PY)

        r = Button(self.buttons, height=H, width=W, text='R', command=lambda: self.turn('R'))
        r.grid(row=3, column=0, padx=PX, pady=PY)

        ra = Button(self.buttons, height=H, width=W, text="R'", command=lambda: self.turn("R'"))
        ra.grid(row=3, column=1, padx=PX, pady=PY)

        b = Button(self.buttons, height=H, width=W, text='B', command=lambda: self.turn('B'))
        b.grid(row=4, column=0, padx=PX, pady=PY)

        ba = Button(self.buttons, height=H, width=W, text="B'", command=lambda: self.turn("B'"))
        ba.grid(row=4, column=1, padx=PX, pady=PY)

        d = Button(self.buttons, height=H, width=W, text='D', command=lambda: self.turn('D'))
        d.grid(row=5, column=0, padx=PX, pady=PY)

        da = Button(self.buttons, height=H, width=W, text="D'", command=lambda: self.turn("D'"))
        da.grid(row=5, column=1, padx=PX, pady=PY)

    def keyPressed(self, event):
        m = ''
        if event.char == 'e':
            m = 'U'
        elif event.char == 'r':
            m = "U'"
        elif event.char == 'a':
            m = 'L'
        elif event.char == 's':
            m = "L'"
        elif event.char == 'd':
            m = 'F'
        elif event.char == 'f':
            m = "F'"
        elif event.char == 'g':
            m = 'R'
        elif event.char == 'h':
            m = "R'"
        elif event.char == 'j':
            m = 'B'
        elif event.char == 'k':
            m = "B'"
        elif event.char == 'c':
            m = 'D'
        elif event.char == 'v':
            m = "D'"

        self.turn(m)

    def speed_slider(self):
        sl = Scale(self.root, variable=self.speedVar, orient=HORIZONTAL, from_=100, to=0, sliderlength=15, width=16)
        sl['length'] = 125
        sl.grid(row=6, column=9, columnspan=3)
        sl.set(60)

        l = Label(self.root, bg='grey', height=2, width=13, text='Change speed', font=('Arial', 15))
        l.grid(row=7, column=9, columnspan=3)

    def scramble(self):
        scr = Button(self.root, text='Scramble', height=1, width=6, command=self.gen_scramble)
        scr.grid(row=0, column=8, columnspan=2)

    def gen_scramble(self):
        length = 25
        sc = ''
        pm = ''
        suf = ['', "'", '2']
        for i in range(length):
            m = self.faces[random.randint(0, 5)]
            while m == pm:
                m = self.faces[random.randint(0, 5)]
            sc += m
            sc += suf[random.randint(0, 2)]
            sc += ' '
            pm = m

        print('Scramble: ' + sc)
        print()

        sclabel1 = Label(self.root, bg='grey', text=sc[0:(len(sc)-1)//2], height=2, width=27)
        sclabel1.grid(row=1, column=6, columnspan=6)
        sclabel2 = Label(self.root, bg='grey', text=sc[(len(sc)-1)//2:], height=2, width=27)
        sclabel2.grid(row=2, column=6, columnspan=6)

        self.turns(sc)

    def input_box(self):
        ib = Entry(self.root, width=12, relief='groove')
        ib.grid(row=6, column=6, columnspan=3, padx=PX, pady=PY)

        ent = Button(self.root, text='Enter moves', height=2, width=10, command=lambda: self.enter(ib, ib.get()))
        ent.grid(row=7, column=6, columnspan=3)

    def enter(self, ib, m):
        ib.delete(0, len(m))
        self.turns(m)

    def revMoves(self, m, s=False):
        m = m[::-1]
        rm = ''

        i = 0
        while i < len(m):
            if self.ismove(m[i]):
                rm += m[i] + "' "
            else:
                if m[i] == "'":
                    rm += m[i+1] + ' '
                    i += 1
                elif m[i] == "2":
                    rm += m[i+1] + '2 '
                    i += 1

            i += 1

        if s:
            return rm
        else:
            self.turns(rm)

    def turns(self, m):
        for i in range(len(m)):
            if self.ismove(m[i]):
                if i != (len(m)-1):
                    if m[i+1] == "'":
                        self.turn(m[i]+m[i+1])
                        i += 2
                    elif m[i+1] == "2":
                        self.turn(m[i])
                        self.turn(m[i])
                        i += 2
                    else:
                        self.turn(m[i])
                else:
                    self.turn(m[i])
                self.show()
                time.sleep(0.01 + ((100 - self.speedVar.get())/100)/2)

        self.show()

    def show(self):
        for i in range(6):
            for j in range(3):
                for k in range(3):
                    self.cube[i][j][k].update()

    def ismove(self, m):
        if m.isupper():
            if m.isalpha():
                if m in self.faces:
                    return True

        return False

    def turn(self, m):
        face = self.faces.index(m[0])
        no = 1
        if len(m) > 1:
            no = 3

        for i in range(no):
            # turning face
            cl = []
            el = []
            for i in range(0, 8, 2):
                cl.append(self.cube[face][self.corners[i]][self.corners[i+1]]['bg'])
                el.append(self.cube[face][self.edges[i]][self.edges[i+1]]['bg'])

            cl = cl[3:] + cl[:3]
            el = el[3:] + el[:3]

            for i in range(0, 8, 2):
                self.cube[face][self.corners[i]][self.corners[i+1]]['bg'] = cl[i//2]
                self.cube[face][self.edges[i]][self.edges[i+1]]['bg'] = el[i//2]

            # surrounding sides
            if face == 0:
                # U
                u = [4, 3, 2, 1]
                for i in range(3):
                    a = self.cube[4][0][i]['bg']
                    self.cube[4][0][i]['bg'] = self.cube[1][0][i]['bg']
                    b = self.cube[3][0][i]['bg']
                    self.cube[3][0][i]['bg'] = a
                    a = self.cube[2][0][i]['bg']
                    self.cube[2][0][i]['bg'] = b
                    self.cube[1][0][i]['bg'] = a

            elif face == 1:
                # L
                l = [0, 2, 5, 4]
                for i in range(3):
                    a = self.cube[0][i][0]['bg']
                    self.cube[0][i][0]['bg'] = self.cube[4][2-i][2]['bg']
                    b = self.cube[2][i][0]['bg']
                    self.cube[2][i][0]['bg'] = a
                    a = self.cube[5][i][0]['bg']
                    self.cube[5][i][0]['bg'] = b
                    self.cube[4][2-i][2]['bg'] = a

            elif face == 2:
                # F
                f = [0, 3, 5, 1]
                for i in range(3):
                    a = self.cube[0][2][i]['bg']
                    self.cube[0][2][i]['bg'] = self.cube[1][2-i][2]['bg']
                    b = self.cube[3][i][0]['bg']
                    self.cube[3][i][0]['bg'] = a
                    a = self.cube[5][0][2-i]['bg']
                    self.cube[5][0][2-i]['bg'] = b
                    self.cube[1][2-i][2]['bg'] = a

            elif face == 3:
                # R
                r = [0, 4, 5, 2]
                for i in range(3):
                    a = self.cube[0][i][2]['bg']
                    self.cube[0][i][2]['bg'] = self.cube[2][i][2]['bg']
                    b = self.cube[4][2-i][0]['bg']
                    self.cube[4][2-i][0]['bg'] = a
                    a = self.cube[5][i][2]['bg']
                    self.cube[5][i][2]['bg'] = b
                    self.cube[2][i][2]['bg'] = a

            elif face == 4:
                # B
                b = [0, 1, 5, 3]
                for i in range(3):
                    a = self.cube[0][0][i]['bg']
                    self.cube[0][0][i]['bg'] = self.cube[3][i][2]['bg']
                    b = self.cube[1][2-i][0]['bg']
                    self.cube[1][2-i][0]['bg'] = a
                    a = self.cube[5][2][2-i]['bg']
                    self.cube[5][2][2-i]['bg'] = b
                    self.cube[3][i][2]['bg'] = a

            elif face == 5:
                # D
                d = [2, 3, 4, 1]
                for i in range(3):
                    a = self.cube[2][2][i]['bg']
                    self.cube[2][2][i]['bg'] = self.cube[1][2][i]['bg']
                    b = self.cube[3][2][i]['bg']
                    self.cube[3][2][i]['bg'] = a
                    a = self.cube[4][2][i]['bg']
                    self.cube[4][2][i]['bg'] = b
                    self.cube[1][2][i]['bg'] = a


if __name__ == "__main__":
    obj = CubeSim()
    obj.display()
    obj.speed_slider()
    obj.input_box()
    obj.scramble()

    def sol():
        from solver import SolAlg
        solObj = SolAlg(obj.cube, obj)
        solObj.solve(solBut)
    solBut = Button(obj.buttons, text='Solve', height=2, width=6, command=sol)
    solBut.grid(row=6, column=0, columnspan=20)
    obj.root.mainloop()

