from tkinter import DISABLED, NORMAL


class SolAlg:

    def __init__(self, cube, cubeObj):
        self.cube = cube
        self.cubeObj = cubeObj

        self.edgeSwap = "R U R' U' R' F R2 U' R' U' R U R' F'"
        self.cornerSwap = "R U' R' U' R U R' F' R U R' U' R' F R"
        self.paritySolve = "R U' R' U' R U R D R' U' R D' R' U2 R' U'"
        self.parity = False

        self.edgeSetups = []
        self.edgeSetups = ["R2 U' R2", '', "R2 U R2", '', "L' U B' U'", "U' F U", "L' U' F U", "U B' U'", "R F' L' R'", "U2 R U2",
                           "U' F U L'"]
        self.edgeSetups += ["L'", '', "U B U'", "U2 R U F' U", "U' F' U", "R' B L R", "L", "R' B' L R", "U2 R' U2", "D' L2", "D2 L2"]
        self.edgeSetups += ["D L2", "L2"]

        self.cornerSetups = []
        self.cornerSetups = ['', "R2", "F2 D", "F2", '', "F' D", "F'", "D' R", "F R'", "R'", "D' F'", "F2 R'", "F", "R' F"]
        self.cornerSetups += ["R2 F", "D R", "R D'", '', "D F'", "R", "D", '', "D'", "D2"]

        self.faces = ['U', 'L', 'F', 'R', 'B', 'D']
        self.colors = ['white', 'orange', 'green', 'red', 'blue', 'yellow']
        self.corners = [0, 0, 0, 2, 2, 2, 2, 0]
        self.edges = [0, 1, 1, 2, 2, 1, 1, 0]
        self.faceSurr = [[4, 3, 2, 1], [0, 2, 5, 4], [0, 3, 5, 1], [0, 4, 5, 2], [0, 1, 5, 3], [2, 3, 4, 1]]

        self.solution = ''

    def solve(self, but):
        # pseudo code
        #
        # solve edges
        # buffer = 0, 1, 2
        # find where it belongs
        # perform setup moves
        # do swap
        # undo setup
        #
        # if there is parity, then solve it
        #
        # solve corners
        # buffer = 1, 0, 0
        # find where it belongs
        # perform setup moves
        # do swap
        # undo setup
        #

        but['state'] = DISABLED

        # edges
        nel = 0
        while not self.checkIfSolved(True):
            c1 = self.cube[0][1][2]['bg']
            c2 = self.cube[3][0][1]['bg']
            print('buffer colors:', c1, c2)
            while ((c1 != 'white') or (c2 != 'red')) and ((c1 != 'red') or (c2 != 'white')):
                print('buffer colors:', c1, c2)
                loc = self.findEdgeLoc(c1, c2)
                print('letter no.:', nel)
                print('loc:', loc)
                print()
                self.doEdgeCycle(loc)
                nel += 1
                self.parity = not self.parity
                c1 = self.cube[0][1][2]['bg']
                c2 = self.cube[3][0][1]['bg']
                print('completed letter')
                print()

            a = self.checkIfSolved(True, True)
            if a != True:
                print('starting new cycle')
                print('loc:', a)
                print()
                self.doEdgeCycle(a)
                nel += 1
                self.parity = not self.parity

        print('no. of edge letters:', nel)

        print('edges are solved')
        print()
        # parity
        if self.parity:
            print('solving parity')
            print()
            self.cubeObj.turns(self.paritySolve)
            self.solution += self.paritySolve

        # corners
        ncl = 0
        while not self.checkIfSolved(False):
            c1 = self.cube[0][0][0]['bg']
            c2 = self.cube[1][0][0]['bg']
            c3 = self.cube[4][0][2]['bg']
            a = (c1 != 'white') or (c2 != 'orange') or (c3 != 'blue')
            b = (c1 != 'orange') or (c2 != 'blue') or (c3 != 'white')
            c = (c1 != 'blue') or (c2 != 'white') or (c3 != 'orange')
            print('buffer colors:', c2, c1, c3)
            while a and b and c:
                print('in inner loop')
                print('buffer colors:', c2, c1, c3)
                loc = self.findCornerLoc(c2, c1, c3)
                print('loc:', loc)
                self.doCornerCycle(loc)
                ncl += 1
                print('letter number:', ncl)
                c1 = self.cube[0][0][0]['bg']
                c2 = self.cube[1][0][0]['bg']
                c3 = self.cube[4][0][2]['bg']
                a = (c1 != 'white') or (c2 != 'orange') or (c3 != 'blue')
                b = (c1 != 'orange') or (c2 != 'blue') or (c3 != 'white')
                c = (c1 != 'blue') or (c2 != 'white') or (c3 != 'orange')
                print('completed letter')
                print()
            x = self.checkIfSolved(False, True)
            if x != True:
                print('starting new cycle')
                print('loc:', x)
                self.doCornerCycle(x)
                ncl += 1
                print('started new cycle')
                print()

        print('no. of corner letters:', ncl)
        print('corners are solved')
        print()
        print('Cube is solved!!')

        print(self.solution)
        print(len(self.solution))
        for i in range(len(self.solution)):
            if (i != 0) and (i % 100) == 0:
                print(self.solution[i])
            else:
                print(self.solution[i], end='')
        print()

        but['state'] = NORMAL

    def doEdgeCycle(self, loc):
        # find edge setup
        f = int(loc[0])
        p = 0
        for i in range(0, len(self.edges), 2):
            if (int(loc[1]) == self.edges[i]) and (int(loc[2]) == self.edges[i + 1]):
                p = i // 2
        ind = (f * 4) + p
        # do edge setup
        print(self.edgeSetups[ind])
        self.cubeObj.turns(self.edgeSetups[ind])
        self.solution += self.edgeSetups[ind] + ' '
        # do edge swap
        self.cubeObj.turns(self.edgeSwap)
        self.solution += self.edgeSwap + ' '
        # reverse setup
        rev = self.cubeObj.revMoves(self.edgeSetups[ind], True)
        self.cubeObj.turns(rev)
        self.solution += rev + ' '

    def doCornerCycle(self, loc):
        # find corner setup
        f = int(loc[0])
        p = 0
        for i in range(0, len(self.corners), 2):
            if (int(loc[1]) == self.corners[i]) and (int(loc[2]) == self.corners[i + 1]):
                p = i // 2
        ind = (f * 4) + p
        # do corner setup
        self.cubeObj.turns(self.cornerSetups[ind])
        print('setup:', self.cornerSetups[ind])
        self.solution += self.cornerSetups[ind] + ' '
        # do corner swap
        print('doing corner swap:', self.cornerSwap)
        self.cubeObj.turns(self.cornerSwap)
        self.solution += self.cornerSwap + ' '
        # reverse setup
        print('undoing setup')
        print()
        rev = self.cubeObj.revMoves(self.cornerSetups[ind], True)
        self.cubeObj.turns(rev)
        self.solution += rev + ' '

    def findEdgeLoc(self, c1, c2):
        f1 = self.colors.index(c1)
        f2 = self.colors.index(c2)

        x = self.edges[self.faceSurr[f1].index(f2) * 2]
        y = self.edges[(self.faceSurr[f1].index(f2) * 2) + 1]
        return str(f1) + str(x) + str(y)

    def findCornerLoc(self, c1, c2, c3):
        f1 = self.colors.index(c1)
        f2 = self.colors.index(c2)
        f3 = self.colors.index(c3)

        l2 = self.faceSurr[f1].index(f2)
        l3 = self.faceSurr[f1].index(f3)

        if abs(l3 - l2) == 1:
            a = max(l3, l2)
        else:
            a = 0

        x = self.corners[a * 2]
        y = self.corners[(a * 2) + 1]

        return str(f1) + str(x) + str(y)

    def checkIfSolved(self, edges, unsolvedLoc=False):
        if edges:
            for i in range(6):
                for j in range(4):
                    con1 = (i == 0) and (self.edges[j*2] == 1) and (self.edges[(j*2)+1] == 2)
                    con2 = (i == 3) and (self.edges[j*2] == 0) and (self.edges[(j*2)+1] == 1)
                    if con1 or con2:
                        continue

                    if self.cube[i][self.edges[j * 2]][self.edges[(j * 2) + 1]]['bg'] != self.colors[i]:
                        if unsolvedLoc:
                            return str(i) + str(self.edges[j * 2]) + str(self.edges[(j * 2) + 1])
                        else:
                            return False
        else:
            for i in range(6):
                for j in range(4):
                    con1 = (i == 0) and (self.corners[j*2] == 0) and (self.corners[(j*2)+1] == 0)
                    con2 = (i == 1) and (self.corners[j*2] == 0) and (self.corners[(j*2)+1] == 0)
                    con3 = (i == 4) and (self.corners[j*2] == 0) and (self.corners[(j*2)+1] == 2)
                    if con1 or con2 or con3:
                        continue

                    if self.cube[i][self.corners[j * 2]][self.corners[(j * 2) + 1]]['bg'] != self.colors[i]:
                        if unsolvedLoc:
                            return str(i) + str(self.corners[j * 2]) + str(self.corners[(j * 2) + 1])
                        else:
                            return False

        return True
