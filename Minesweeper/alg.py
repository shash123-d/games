import pyautogui
import random
from tkinter import DISABLED
import time

# 1440x900
# formula for coords
# (x*bx)+(bx//2)+450, (y*by)+(by*2)

# rules for alg
# -if no of dirt around no is equal to no, then flag that dirt
# -if no of flags is equal to no and dirt is more than no, then dig all dirt except flags


def solve(game, diff):
    Y, X = len(game.field), len(game.field[0])
    by, bx = game.dirt[0][0].winfo_height(), game.dirt[0][0].winfo_width()

    def moveto(d, ret=False):
        l = d.grid_info()
        r, c = l['row'], l['column']
        if diff == 0:
            pyautogui.moveTo((c*bx)+(bx//2)+450, (r*by)+(by*2))
        elif diff == 1:
            pyautogui.moveTo((c*bx)+(bx//2)+292, (r*by)+(by*2))
        if ret:
            return [r, c]

    def mineandflag(y, x):
        change = False
        if game.field[y][x]['text'] != 'BOOM':
            ndirt = 0
            dirt = []
            # print('in dirt collection')
            for a in range(-1, 2):
                for b in range(-1, 2):
                    i, j = y+a, x+b
                    if (i >= 0) and (i < Y) and (j >= 0) and (j < X):
                        try:
                            game.root.update()
                            if (len(game.dirt[i][j].grid_info()) != 0) and (len(game.field[i][j].grid_info()) == 0):
                                # print(i, j)
                                # print(game.dirt[i][j].grid_info())
                                # print(game.field[i][j].grid_info())
                                dirt.append(game.dirt[i][j])
                                ndirt += 1
                        except IndexError:
                            continue
            # print()

            n = int(game.field[y][x]['text'])
            if ndirt == n:
                for d in dirt:
                    if d['highlightbackground'] != 'red':
                        change = True
                        moveto(d)
                        d['highlightbackground'] = 'red'
                        # time.sleep(0.2)
                        game.root.update()
            else:
                nf = 0
                for d1 in dirt:
                    if d1['highlightbackground'] == 'red':
                        nf += 1
                if nf == n:
                    # print('in mining part')
                    # print(y, x)
                    # print(ndirt)
                    # for test in dirt:
                    #     print(test)
                    #     print(test.grid_info())
                    # print()
                    for d2 in dirt:
                        if d2['highlightbackground'] != 'red':
                            change = True
                            if len(d2.grid_info()) != 0:
                                c = moveto(d2, True)
                                game.click(c[0], c[1])
                                # time.sleep(0.2)
                                game.root.update()

        return change

    while not game.over:
        change = False
        for i in range(Y):
            for j in range(X):
                if (len(game.dirt[i][j].grid_info()) == 0) and (game.field[i][j]['text'] != 0):
                    c = mineandflag(i, j)
                    if c and not change:
                        change = True

        if game.over:
            break

        if not change:
            i, j = random.randint(0, Y-1), random.randint(0, X-1)
            while (len(game.dirt[i][j].grid_info()) == 0) or (game.dirt[i][j]['highlightbackground'] == 'red'):
                i, j = random.randint(0, Y - 1), random.randint(0, X - 1)
            print(i, j)
            if diff == 0:
                pyautogui.moveTo((j*bx)+(bx//2)+450, (i*by)+(by*2))
            elif diff == 1:
                pyautogui.moveTo((j*bx)+(bx//2)+292, (i*by)+(by*2))
            game.click(i, j)
            game.root.update()
