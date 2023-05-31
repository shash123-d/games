import random
import time


class Piece:
    def __init__(self, p, grid, c, scl):
        self.x = random.randint(1, 6)
        self.y = 0
        self.grid = grid
        self.canvas = c
        self.p = p
        self.scl = scl
        self.body = []
        self.color = ''
        self.dropped = False
        if p == 0:
            # line piece
            self.color = 'blue'
            for i in range(4):
                self.body.append([self.x+i, self.y])

        elif p == 1:
            # square piece
            self.color = 'yellow'
            self.body.append([self.x, self.y])
            self.body.append([self.x, self.y+1])
            self.body.append([self.x+1, self.y])
            self.body.append([self.x+1, self.y+1])

        elif p == 2:
            # cross piece
            self.color = 'purple'
            self.body.append([self.x, self.y-1])
            for i in range(-1, 2):
                self.body.append([self.x+i, self.y])

        elif p == 3:
            # l piece
            self.color = 'orange'
            self.body.append([self.x, self.y])
            self.body.append([self.x-1, self.y-1])
            self.body.append([self.x, self.y - 1])
            self.body.append([self.x, self.y + 1])

        elif p == 4:
            # j piece
            self.color = '#00008b'
            self.body.append([self.x, self.y])
            self.body.append([self.x, self.y-1])
            self.body.append([self.x, self.y + 1])
            self.body.append([self.x-1, self.y + 1])

        elif p == 5:
            # s piece
            self.color = 'green'
            self.body.append([self.x, self.y])
            self.body.append([self.x-1, self.y-1])
            self.body.append([self.x-1, self.y])
            self.body.append([self.x, self.y+1])

        elif p == 6:
            # z piece
            self.color = 'red'
            self.body.append([self.x, self.y])
            self.body.append([self.x+1, self.y-1])
            self.body.append([self.x+1, self.y])
            self.body.append([self.x, self.y+1])

        self.shape = []

        print('body:', self.body)
        
    def show(self):
        # self.y = 0
        for i in range(4):
            self.shape.append(self.canvas.create_rectangle(self.body[i][0]*self.scl, self.body[i][1]*self.scl, (self.body[i][0]*self.scl)+self.scl, (self.body[i][1]*self.scl)+self.scl, fill=self.color))

    def updateGrid(self):
        if not self.dropped:
            for c in range(len(self.body)):
                self.grid[self.body[c][1]][self.body[c][0]] = self.shape[c]

            # line clearance logic
            # check lines of which the block is a part of
            chkdlines = []
            for block in self.body:
                if block[1] not in chkdlines:
                    chkdlines.append(block[1])
                    for i in self.grid[block[1]]:
                        if i == 0:
                            break
                    else:
                        print('row passed', block[1])
                        self.clearline(block[1])

            self.dropped = True

            print('chkdlines:', chkdlines)

        return 0

    def clearline(self, row):
        print('in clearline trying to clear line')
        print('row', row)
        for i in range(10):
            self.canvas.delete(self.grid[row][i])
            self.grid[row][i] = 0

        for i in range(row-1, 0, -1):
            empty = 0
            for j in range(10):
                self.grid[i+1][j] = self.grid[i][j]
                if self.grid[i][j] != 0:
                    empty = 0
                    self.canvas.move(self.grid[i+1][j], 0, self.scl)
                else:
                    empty += 1
                    if empty == 10:
                        break
                    continue
            else:
                continue
            break

    def update(self):
        # update position
        for p in self.body:
            if p[1] == 19:
                time.sleep(0.2)
                return self.updateGrid()
            elif self.grid[p[1]+1][p[0]] != 0:
                if p[1] == 0:
                    return -1
                else:
                    time.sleep(0.2)
                    return self.updateGrid()
        else:
            self.y += 1
            for i in range(4):
                self.body[i][1] += 1

            # move shape

            # 'smooth' animation
            # pps = 5
            # for m in range(self.scl//pps):
            #     for i in range(4):
            #       self.canvas.move(self.shape[i], 0, pps)
            #     self.canvas.update()

            # 'blocky' animation
            for i in range(4):
                self.canvas.move(self.shape[i], 0, self.scl)

            return 1

    def move_left(self, event):
        print('left arrow key')
        for p in self.body:
            if p[0] == 0:
                break
            elif self.grid[p[1]][p[0]-1] != 0:
                break
        else:
            self.x -= 1
            for a in range(len(self.body)):
                self.body[a][0] -= 1
                self.canvas.move(self.shape[a], -self.scl, 0)
            self.canvas.update()

    def move_right(self, event):
        print('right arrow key')
        for p in self.body:
            if p[0] == 9:
                break
            elif self.grid[p[1]][p[0]+1] != 0:
                break
        else:
            self.x += 1
            for a in range(len(self.body)):
                self.body[a][0] += 1
                self.canvas.move(self.shape[a], self.scl, 0)
            self.canvas.update()

    def rotate_left(self, event):
        print('z')
        # self.rotate_right(0)
        # self.rotate_right(0)
        # self.rotate_right(0)
        if (self.p == 0) or (self.p >= 5):
            self.rotate_right(0)
        else:
            self.rotate_right(0)
            self.rotate_right(0)
            self.rotate_right(0)

    def rotate_right(self, event):
        if event != 0:
            print('up')
        if self.p != 1:
            # 0: line piece
            if self.p == 0:
                # if lying horizontally (making vertical)
                if self.body[1][0] == self.body[0][0] + 1:
                    if self.y <= 17:
                        # top block
                        self.x += 2
                        self.y -= 1

                        self.body[0][0] += 2
                        self.body[0][1] -= 1
                        self.canvas.move(self.shape[0], 2*self.scl, -self.scl)

                        self.body[1][0] += 1
                        self.canvas.move(self.shape[1], self.scl, 0)

                        self.body[2][1] += 1
                        self.canvas.move(self.shape[2], 0, self.scl)

                        self.body[3][0] -= 1
                        self.body[3][1] += 2
                        self.canvas.move(self.shape[3], -self.scl, 2*self.scl)

                    else:
                        # top block
                        self.x += 2
                        self.y = 16

                        self.body[0][0] += 2
                        self.body[0][1] = 16
                        self.canvas.moveto(self.shape[0], self.body[0][0]*self.scl, self.body[0][1]*self.scl)

                        self.body[1][0] += 1
                        self.body[1][1] -= self.body[1][1] - 17
                        self.canvas.moveto(self.shape[1], self.body[1][0]*self.scl, self.body[1][1]*self.scl)

                        self.body[2][1] -= self.body[2][1] - 18
                        self.canvas.moveto(self.shape[2], self.body[2][0]*self.scl, self.body[2][1]*self.scl)

                        self.body[3][0] -= 1
                        self.body[3][1] += 19 - self.body[3][1]
                        self.canvas.moveto(self.shape[3], self.body[3][0]*self.scl, self.body[3][1]*self.scl)

                else:
                    # if vertical (make horizontal)
                    self.x -= 2
                    self.y += 1

                    self.body[0][0] -= 2
                    self.body[0][1] += 1
                    self.canvas.move(self.shape[0], -2 * self.scl, self.scl)

                    self.body[1][0] -= 1
                    self.canvas.move(self.shape[1], -self.scl, 0)

                    self.body[2][1] -= 1
                    self.canvas.move(self.shape[2], 0, -self.scl)

                    self.body[3][0] += 1
                    self.body[3][1] -= 2
                    self.canvas.move(self.shape[3], self.scl, -2 * self.scl)

            # 2: cross piece
            # 0 1 0
            # 1 1 1
            # 0 0 0
            if self.p == 2:
                # -1,0;0,-1;+1,0;0+1
                # +1-1,+1+1,-1+1,-1-1
                coords = [[-1, 0], [0, -1], [1, 0], [0, 1], [-1, 0]]
                if (self.x > 0) and (self.x < 9) and (self.y < 19):
                    for c in range(len(coords)):
                        if [self.x + coords[c][0], self.y + coords[c][1]] not in self.body:
                            ind = self.body.index([self.x + coords[c+1][0], self.y + coords[c+1][1]])
                            self.body[ind][0] = self.x + coords[c][0]
                            self.body[ind][1] = self.y + coords[c][1]
                            xoff = coords[c][0] - coords[c+1][0]
                            yoff = coords[c][1] - coords[c+1][1]
                            self.canvas.move(self.shape[ind], xoff*self.scl, yoff*self.scl)
                            break

            # 3: l piece
            # 1 1 0
            # 0 1 0
            # 0 1 0
            # &
            # 4: j piece
            # 0 1 0
            # 0 1 0
            # 1 1 0
            if (self.p == 3) or (self.p == 4):
                self.rotate_corner_n_edges()

            # 5: s piece
            # 1 0 0
            # 1 1 0
            # 0 1 0
            if self.p == 5:
                if [self.x-1, self.y-1] in self.body:
                    self.rotate_corner_n_edges()
                else:
                    self.rotate_corner_n_edges()
                    self.rotate_corner_n_edges()
                    self.rotate_corner_n_edges()

            # 6: z piece
            # 0 0 1
            # 0 1 1
            # 0 1 0
            if self.p == 6:
                # self.rotate_corner_n_edges()
                if [self.x, self.y - 1] in self.body:
                    self.rotate_corner_n_edges()
                    self.rotate_corner_n_edges()
                    self.rotate_corner_n_edges()
                else:
                    self.rotate_corner_n_edges()

    def rotate_corner_n_edges(self):
        ccoords = [[-1, -1], [1, -1], [1, 1], [-1, 1]]
        cmoves = [[2, 0], [0, 2], [-2, 0], [0, -2]]
        ecoords = [[0, -1], [1, 0], [0, 1], [-1, 0]]
        emoves = [[1, 1], [-1, 1], [-1, -1], [1, -1]]

        if (self.x > 0) and (self.x < 9) and (self.y < 19):
            # corner
            for c in range(len(ccoords)):
                cnr = [self.x + ccoords[c][0], self.y + ccoords[c][1]]
                if cnr in self.body:
                    ind = self.body.index(cnr)
                    self.body[ind][0] += cmoves[c][0]
                    self.body[ind][1] += cmoves[c][1]
                    self.canvas.move(self.shape[ind], cmoves[c][0] * self.scl, cmoves[c][1] * self.scl)
                    break

            # edges
            e = 0
            ne = 0
            while e < 4:
                edg = [self.x + ecoords[e][0], self.y + ecoords[e][1]]
                if edg in self.body:
                    if (self.p == 6) and (ne == 1):
                        ind = self.body.index(edg)
                        try:
                            ind = self.body.index(edg, ind+1)
                        except ValueError:
                            ind = self.body.index(edg)
                    else:
                        ind = self.body.index(edg)
                    self.body[ind][0] += emoves[e][0]
                    self.body[ind][1] += emoves[e][1]
                    self.canvas.move(self.shape[ind], emoves[e][0] * self.scl, emoves[e][1] * self.scl)
                    if (self.p == 3) or (self.p == 4):
                        e += 2
                        continue
                    ne += 1
                    if ne == 2:
                        break
                e += 1

    def drop(self, event):
        print('space')
        colstocheck = []
        for b in self.body:
            if [b[0], b[1]+1] not in self.body:
                colstocheck.append([b[0], b[1]])

        drop = 21
        for r in colstocheck:
            for c in range(r[1]+1, 20):
                if self.grid[c][r[0]] != 0:
                    if c - r[1] - 1 < drop:
                        drop = c - r[1] - 1
                    break
            else:
                if 19 - r[1] < drop:
                    drop = 19 - r[1]

        self.y += drop
        for b in self.body:
            b[1] += drop
        for i in self.shape:
            self.canvas.move(i, 0, drop*self.scl)
        self.updateGrid()
