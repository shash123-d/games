import pyautogui
from playsound import playsound
import time
import random


# 443, 298; 984 715
# 18x14

# bx = (984-443)//18
# by = (715-298)//14
bx, by = 30, 30

# 885, 586, 1080, 840

xoff, yoff = 465, 308
pxoff = 930


class minesweeperbot:
    def __init__(self):
        self.field = []
        for i in range(14):
            self.field.append([])
            for j in range(18):
                self.field[i].append('g')
        self.sc = ''

        # colors
        # dg; 161, 209, 84
        # lg; 169, 215, 91
        # ld; 230, 194, 160
        # dd; 216, 184, 154
        # 1; 14, 118, 207 (found in middle30, 30)
        # 2; 52, 142, 65  (30, 45)
        # 3; 213, 48, 48  (middle)(mor=1)
        # 4; 155, 79, 159 (middle)(mor = 8)
        # 5; 255, 143, 26 (middle)
        # 6; 0, 151, 167
        # 7; 66, 66, 66
        # flag; 244, 54, 11 (30, 15)
        self.colors = {(161, 209, 84, 255): 'g', (169, 215, 91, 255): 'g', (184, 221, 125, 255): 'g', (190, 225, 130, 255): 'g', (230, 194, 160, 255): 'd',
                  (216, 184, 154, 255): 'd', (14, 118, 207, 255): 1, (52, 142, 65, 255): 2,
                  (213, 48, 48, 255): 3, (155, 79, 159, 255): 4, (255, 143, 26, 255): 5, (0, 151, 167, 255): 6,
                  (66, 66, 66, 255): 7, (244, 54, 11, 255): 'f'}

        print('get to minesweeper')
        time.sleep(1.5)
        playsound('ding.mp3')

        self.scratch = False
        if not self.scratch:
            self.ss()
        # self.solve()

        # time.sleep(1)
        # playsound('ding.mp3')
        # time.sleep(0.5)
        # self.seechanges(0, 0)
        # for i in range(14):
        #     print(self.field[i])

    def ss(self):
        self.sc = pyautogui.screenshot('sc.png', region=(900, 586, 1080, 840))
        playsound('ding.mp3')
        print(self.sc.getpixel((0, 0)))
        print(self.sc.getpixel((1079, 0)))
        print(self.sc.getpixel((0, 839)))
        print()
        self.getfield()

    def getcolor(self, c, i, j, sc=False):
        clr = ''
        try:
            clr = self.colors[c]
        except KeyError:
            # check if 2 or flag or 4 or 3
            if sc:
                if self.sc.getpixel((j, i+15)) == (52, 142, 65, 255):
                    return 2
                if self.sc.getpixel((j, i-15)) == (244, 54, 11, 255):
                    return 'f'
            else:
                r, g, b = pyautogui.pixel(pxoff+(j*60), (yoff*2)+(i*60)+15)
                c2 = (r, g, b, 255)
                if c2 == (52, 142, 65, 255):
                    return 2
                # print()
                # print(pxoff+j-30, (yoff*2)+i-45)
                r, g, b = pyautogui.pixel(pxoff+(j*60), (yoff*2)+(i*60)-15)
                # print(r, g, b)
                cf = (r, g, b, 255)
                if cf == (244, 54, 11, 255):
                    return 'f'

            if (c[0] < 164) and (c[0] > 146) and (c[1] < 88) and (c[1] > 70) and (c[2] < 168) and (c[2] > 150):
                return 4
            elif (c[0] < 215) and (c[0] > 212) and (c[1] < 50) and (c[1] > 47) and (c[2] < 50) and (c[2] > 47):
                return 3
            else:
                print('problem')
                print(j, i)
                print((j + 30) // 60, (i + 30) // 60)
                print(c)
                for loop in range(100):
                    playsound('problem.wav')
        else:
            return clr

    def getfield(self):
        for i in range(30, 840, 60):
            for j in range(30, 1080, 60):
                c = self.sc.getpixel((j, i))
                self.field[i//60][j//60] = self.getcolor(c, i, j, True)

        for i in range(14):
            print(self.field[i])

        playsound('ding.mp3')

    def over(self):
        for i in range(14):
            for j in range(18):
                if self.field[i][j] == 'g':
                    return False

        return True
    
    def mineandflag(self, y, x):
        change = False
        
        ngrass = 0
        grass = []
        nf = -1
        # print('in dirt collection')
        for a in range(-1, 2):
            for b in range(-1, 2):
                i, j = y + a, x + b
                if (i >= 0) and (i < 14) and (j >= 0) and (j < 18):
                    if (self.field[i][j] == 'g') or (self.field[i][j] == 'f'):
                        grass.append([i, j])
                        ngrass += 1

        n = self.field[y][x]
        if ngrass == n:
            for [a, b] in grass:
                if self.field[a][b] != 'f':
                    change = True
                    print('rc', b, a)
                    print()
                    pyautogui.rightClick(xoff+(b*30), yoff+(a*30))
                    self.field[a][b] = 'f'
        else:
            nf = 0
            for [a, b] in grass:
                if self.field[a][b] == 'f':
                    nf += 1

            if nf == n:
                clicked = []
                for [a, b] in grass:
                    if self.field[a][b] != 'f':
                        change = True
                        clicked.append([b, a])
                        print('mining cus flags r full', b, a)
                        print()
                        # time.sleep(0.5)
                        # pyautogui.click(xoff + (b * 30), yoff + (a * 30), clicks=2)
                        p = pyautogui.pixel((xoff*2)+(b*60), (yoff*2)+(a*60))
                        ct = 0
                        while pyautogui.pixel((xoff*2)+(b*60), (yoff*2)+(a*60)) == p:
                            time.sleep(0.4)
                            pyautogui.click(xoff+(b*30), yoff+(a*30), clicks=2)
                            ct += 1
                            if ct >= 3:
                                break

        if change:
            if nf == n:
                time.sleep(0.6)
                for [cx, cy] in clicked:
                    self.seechanges(cy, cx)

        return change

    def seechanges(self, y, x):
        r, g, b = pyautogui.pixel((xoff*2)+(x*60), (yoff*2)+(y*60))
        c = self.getcolor((r, g, b, 255), y, x)
        # while c == self.field[y][x]:
        #     time.sleep(0.4)
        #     pyautogui.click(xoff+(x*30), yoff+(y*30), clicks=2)
        #     time.sleep(0.5)
        #     c = self.getcolor((r, g, b, 255), y, x)
        self.field[y][x] = c
        for i in range(14):
            print(self.field[i])
        # covered = []
        # for a in range(-1, 2):
        #     for b in range(-1, 2):
        #         i, j = y+a, x+b
        #         if ([i, j] not in skip) and (i >= 0) and (i < 14) and (j >= 0) and (j < 18):
        #             covered.append([i, j])
        #
        # for [ly, lx] in covered:
        #     r, g, bl = pyautogui.pixel((xoff*2)+(lx*60), (yoff*2)+(ly*60))
        #     c = (r, g, bl, 255)
        #     clr = self.getcolor(c, 30+(ly*60), 30+(lx*60))
        #     if clr != self.field[ly][lx]:
        #         self.field[ly][lx] = clr
        #         self.seechanges(ly, lx, covered)
        #     else:
        #         continue

    def randomclick(self):
        i, j = random.randint(0, 13), random.randint(0, 17)
        while self.field[i][j] != 'g':
            i, j = random.randint(0, 13), random.randint(0, 17)
        print('random click', j, i)
        print()
        pyautogui.click(xoff + (j * 30), yoff + (i * 30))
        time.sleep(0.7)

    def solve(self):
        if self.scratch:
            self.randomclick()
            self.ss()
            self.scratch = False

        while not self.over():
            change = False
            for i in range(14):
                for j in range(18):
                    if type(self.field[i][j]) == int:
                        pyautogui.moveTo(xoff+(j*30), yoff+(i*30))
                        # time.sleep(0.1)
                        c = self.mineandflag(i, j)
                        if c:
                            change = True

            if not change:
                # add complicated grouping logic here later
                self.randomclick()

            self.ss()


if __name__ == '__main__':
    obj = minesweeperbot()
