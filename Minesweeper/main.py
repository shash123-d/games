from tkinter import *
import random

H, W = 2, 2
LH, LW = H, W + 3

diff = 1
if diff == 0:
    X, Y = 10, 10
    nmines = 10
elif diff == 1:
    X, Y = 16, 16
    nmines = 40
elif diff == 2:
    X, Y = 30, 16
    nmines = 99
# custom
# x, y = 
# mines = 


class Minesweeper:
    def __init__(self):
        self.root = Tk()
        self.root.title('Minesweeper')
        if diff == 0:
            self.root.geometry('540x530')
        elif diff == 1:
            self.root.geometry('864x789')
        # self.root['bg'] = 'white'

        self.game = Frame(self.root)
        self.game.grid(row=0, column=0)

        self.field = []
        self.dirt = []
        for i in range(Y):
            self.dirt.append([])
            self.field.append([])
            for j in range(X):
                self.field[i].append(Label(self.game, height=LH, width=LW, text=0))
                self.dirt[i].append(Button(self.game, height=H, width=W, command=lambda i=i, j=j: self.click(i, j)))
                self.dirt[i][j].grid(row=i, column=j)
        self.setfield()

        self.root.bind('<Button-2>', self.flag)

        self.over = False

        e = Button(self.root, text='Exit', height=2, width=4, command=self.root.destroy)
        e.grid(row=2, column=0)

        if diff == 0:
            yoff = 720 - 270
        elif diff == 1:
            yoff = 720 - 432
        self.root.geometry('+{}+{}'.format(yoff, 0))

    def chord(self, event):
        loc = self.loc(event.x_root, event.y_root)
        i, j = loc[0], loc[1]
        print('chording at', i, j)
        n = int(self.field[i][j]['text'])
        m = 0
        for a in range(-1, 2):
            for b in range(-1, 2):
                y, x = i+a, j+b
                if (y >= 0) and (y < Y) and (x >= 0) and (x < X):
                    try:
                        if self.dirt[i+a][j+b]['highlightbackground'] == 'red':
                            m += 1
                    except IndexError:
                        continue

        if m == n:
            for a in range(-1, 2):
                for b in range(-1, 2):
                    y, x = i+a, j+b
                    if (y >= 0) and (y < Y) and (x >= 0) and (x < X):
                        try:
                            if (self.dirt[y][x]['highlightbackground'] != 'red') and (len(self.dirt[y][x].grid_info()) != 0):
                                self.click(y, x)
                        except IndexError:
                            continue

    def loc(self, x, y):
        # 5, 55
        print(x, y)
        if diff == 0:
            x = x - 450
            y = y - 55
        elif diff == 1:
            x = x - 292
            y = y - 58
        bx = self.dirt[0][0].winfo_width()
        by = self.dirt[0][0].winfo_height()
        i = y//by
        j = x//bx
        return [i, j]

    def setfield(self):
        mines = []
        n = random.randint(0, (Y*X)-1)
        for m in range(nmines):
            while n in mines:
                n = random.randint(0, (Y * X)-1)
            mines.append(n)
            i = n//X
            j = n % X
            self.field[i][j]['text'] = 'BOOM'
            for a in range(-1, 2):
                for b in range(-1, 2):
                    self.raiseno(i+a, j+b)

        for row in range(Y):
            for col in range(X):
                if self.field[row][col]['text'] == 'BOOM':
                    print('M', end=' ')
                else:
                    print(self.field[row][col]['text'], end=' ')
            print()

    def end(self):
        for i in range(Y):
            for j in range(X):
                self.dirt[i][j]['state'] = DISABLED
                if self.dirt[i][j]['highlightbackground'] != 'red' and self.field[i][j]['text'] == 'BOOM':
                    self.dirt[i][j]['highlightbackground'] = 'red'
        self.root.update()

    def raiseno(self, i, j):
        try:
            if (i >= 0) and (i < Y) and (j >= 0) and (j < X):
                if self.field[i][j]['text'] != 'BOOM':
                    self.field[i][j]['text'] += 1
        except IndexError:
            pass

    def click(self, i, j):
        if self.dirt[i][j]['highlightbackground'] != 'red':
            self.dirt[i][j].grid_forget()
            self.root.update()
            if self.field[i][j]['text'] == 0:
                self.massdig(i, j)
                self.root.update()
            else:
                self.field[i][j].grid(row=i, column=j)
                self.field[i][j].bind('<Button-1>', self.chord)
                self.root.update()
            if self.field[i][j]['text'] == 'BOOM':
                self.over = True
                print('ur dead')
                self.end()

            self.checkWin()

    def checkWin(self):
        for i in range(Y):
            for j in range(X):
                if self.field[i][j]['text'] != 'BOOM':
                    if len(self.dirt[i][j].grid_info()) != 0:
                        break
            else:
                continue
            break
        else:
            self.over = True
            print('u won')
            self.end()

    def massdig(self, i, j):
        for a in range(-1, 2):
            for b in range(-1, 2):
                y = i + a
                x = j + b
                if (y >= 0) and (y < Y) and (x >= 0) and (x < X):
                    try:
                        if self.field[y][x]['text'] == 0:
                            Label(self.game, height=LH, width=LW).grid(row=y, column=x)
                            if len(self.dirt[y][x].grid_info()) != 0:
                                self.dirt[y][x].grid_forget()
                                # self.root.update()
                                self.massdig(y, x)
                        elif self.field[y][x]['text'] != 'BOOM':
                            self.dirt[y][x].grid_forget()
                            self.field[y][x].grid(row=y, column=x)
                            self.field[y][x].bind('<Button-1>', self.chord)
                            # self.root.update()
                    except IndexError:
                        continue

    def flag(self, event):
        loc = self.loc(event.x_root, event.y_root)
        i = loc[0]
        j = loc[1]
        print(i, j)
        print()

        if self.dirt[i][j]['highlightbackground'] != 'red':
            self.dirt[i][j]['highlightbackground'] = 'red'
        else:
            self.dirt[i][j]['highlightbackground'] = 'systemWindowBackgroundColor'
        self.root.update()

        # img = Image.open('flag.png')
        # img = img.resize((50, 50))
        # flag = ImageTk.PhotoImage(img)
        # label = Label(self.game, image=flag)
        # label.grid(row=i, column=j)


def Main():
    obj = Minesweeper()

    from alg import solve
    sol = Button(obj.root, text='Watch AI Solve', height=2, width=7, command=lambda: solve(obj, diff))
    sol.grid(row=1, column=0)

    obj.root.mainloop()


if __name__ == '__main__':
    # global p1
    # p1 = multiprocessing.Process(target=Main)
    # p1.start()
    Main()
