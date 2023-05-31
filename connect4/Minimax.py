import random
# make base minimax algorithm
# then maybe add basic strategic principles
# rules/strategy added
# if score of all moves is same then dont drop coin on top of opponents coin


def minimax(pos, depth, alpha, beta, maximizingPlayer, top=False):
    if checkWin(pos, maximizingPlayer):
        # print()
        # print('win seen at depth', depth)
        # print(pos)
        # print(depth)
        # print()
        if maximizingPlayer:
            return [-1, pos]
        else:
            return [1, pos]
    if depth == 0:
        return [0, pos]

    if maximizingPlayer:
        children = makeChildren(pos, 'blue')
        #
        # print()
        # print(children)
        # print()
        maxsc = -10
        maxPos = children[random.randint(0, len(children)-1)]
        for child in children:
            score = minimax(child, depth-1, alpha, beta, False)
            if score[0] > maxsc:
                maxsc = score[0]
                maxPos = child
            alpha = max(alpha, score[0])
            if beta <= alpha:
                break
        return [maxsc, maxPos]

    else:
        children = makeChildren(pos, 'yellow')
        minsc = 10
        minPos = children[random.randint(0, len(children)-1)]
        for child in children:
            score = minimax(child, depth-1, alpha, beta, True)
            if top:
                for r in child:
                    print(r)
                print(score[0])
                print()

            if score[0] < minsc:
                minsc = score[0]
                minPos = child
            beta = min(beta, score[0])
            if beta <= alpha:
                break
        return [minsc, minPos]


def makeChildren(pos, side):
    children = []

    for c in range(7):
        for r in range(6):
            if pos[r][c] != 0:
                if r != 0:
                    children.append(copy(pos))
                    children[len(children)-1][r-1][c] = side
                break

            if (r == 5) and (pos[r][c] == 0):
                children.append(copy(pos))
                children[len(children)-1][5][c] = side
                break

    return children


def copy(a1):
    a2 = []
    for r in range(6):
        a2.append([])
        for c in range(7):
            a2[r].append(a1[r][c])

    return a2


def checkWin(pos, mplayer):
    if mplayer:
        side = 'yellow'
    else:
        side = 'blue'

    for r in range(len(pos)):
        for c in range(len(pos[r])):
            if pos[r][c] == side:
                # check if connected to 4 on
                # down
                # right                    
                # downright and downleft
                if c <= 3:
                    for rs in range(c+1, c+4):
                        if pos[r][rs] != side:
                            break
                    else:
                        return True

                if r <= 2:
                    for ds in range(r+1, r+4):
                        if pos[ds][c] != side:
                            break
                    else:
                        return True

                    if c <= 3:
                        for dr in range(1, 4):
                            if pos[r+dr][c+dr] != side:
                                break
                        else:
                            return True

                    if c >= 3:
                        for dl in range(-1, -4, -1):
                            if pos[r-dl][c+dl] != side:
                                break
                        else:
                            return True

    return False
