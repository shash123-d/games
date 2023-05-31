§from tkinter import *
from King import King
from Pawn import Pawn
from Knight import Knight
from Bishop import Bishop
from Rook import Rook
from Queen import Queen

root = Tk()
root.title('Chess')
dboard = Canvas(root, height=397, width=397)
dboard.grid(row=0, column=0)
board = []
for i in range(8):
    board.append([])
    for j in range(8):
        board[i].append(0)
    print(board[i])


def switchclr(c):
    if c == 'black':
        return 'white'
    else:
        return 'black'


clr = 'white'
for i in range(8):
    for j in range(8):
        dboard.create_rectangle(50*j, 50*i, (50*j)+50, (50*i)+50, fill=clr)
        clr = switchclr(clr)
    clr = switchclr(clr)

blackPieces = []

whitePieces = []

# Pieces
# kings
bk = King(dboard, board, 4, 0, 'black', whitePieces)
blackPieces.append(bk)
board[0][4] = bk
wk = King(dboard, board, 4, 7, 'white', blackPieces)
whitePieces.append(wk)
board[7][4] = wk

# pawns
for i in range(8):
    bp = Pawn(dboard, board, i, 1, 'black', whitePieces)
    blackPieces.append(bp)
    board[1][i] = bp
    wp = Pawn(dboard, board, i, 6, 'white', blackPieces)
    whitePieces.append(wp)
    board[6][i] = wp

# Knights
for i in range(1, 7, 5):
    bk = Knight(dboard, board, i, 0, 'black')
    blackPieces.append(bk)
    board[0][i] = bk
    wk = Knight(dboard, board, i, 7, 'white')
    whitePieces.append(wk)
    board[7][i] = wk

# Bishops
for i in range(2, 6, 3):
    bb = Bishop(dboard, board, i, 0, 'black')
    blackPieces.append(bb)
    board[0][i] = bb
    wb = Bishop(dboard, board, i, 7, 'white')
    whitePieces.append(wb)
    board[7][i] = wb

# Rook
br = Rook(dboard, board, 0, 0, 'black', 'queen')
blackPieces.append(br)
board[0][0] = br
wr = Rook(dboard, board, 0, 7, 'white', 'queen')
whitePieces.append(wr)
board[7][0] = wr
br = Rook(dboard, board, 7, 0, 'black', 'king')
blackPieces.append(br)
board[0][7] = br
wr = Rook(dboard, board, 7, 7, 'white', 'king')
whitePieces.append(wr)
board[7][7] = wr

# Queen
bq = Queen(dboard, board, 3, 0, 'black')
blackPieces.append(bq)
board[0][3] = bq
wq = Queen(dboard, board, 3, 7, 'white')
whitePieces.append(wq)
board[7][3] = wq

select = ''
sx, sy = 0, 0
turn = 'white'
check = False
cky, ckx = 10, 10
checkingPiece = 0
fiftydm = 0
mn = 0
pboards = []
moves = []
# keeping track of moves by
# moves = [#1st move[{moved piece}, old loc of piece, type of move, new loc of piece], #2nd move[],...]

# add checkmate
# add stalemate


def typePiece(p):
    if isinstance(p, King):
        return 'K'
    elif isinstance(p, Pawn):
        return 'P'
    elif isinstance(p, Knight):
        return 'Kn'
    elif isinstance(p, Bishop):
        return 'B'
    elif isinstance(p, Rook):
        return 'Rook'
    elif isinstance(p, Queen):
        return 'Q'


def replicateBoard():
    pboards.append([])
    m = len(pboards) - 1
    for i in range(8):
        pboards[m].append([])
        for j in range(8):
            if board[i][j] in whitePieces:
                pboards[m][i].append('W')
            elif board[i][j] in blackPieces:
                pboards[m][i].append('B')
            else:
                pboards[m][i].append('  ')
                continue

            pboards[m][i][j] += typePiece(board[i][j])


replicateBoard()


def isturn(m):
    if turn == 'white':
        if m in whitePieces:
            return True
    else:
        if m in blackPieces:
            return True

    return False


def movePiece(y, x, sy, sx):
    board[y][x] = board[sy][sx]
    board[sy][sx] = 0

    board[y][x].x = x
    board[y][x].y = y
    board[y][x].display()

    global turn
    turn = switchclr(turn)


def castle(ky, kx, rx, ckx, crx):
    board[ky][ckx] = board[ky][kx]
    board[ky][crx] = board[ky][rx]
    board[ky][kx] = 0
    board[ky][rx] = 0

    board[ky][ckx].x = ckx
    board[ky][crx].x = crx
    board[ky][ckx].display()
    board[ky][crx].display()

    global turn
    turn = switchclr(turn)
    

def prommenu(y, x, sy, sx):
    global py, px, psy, psx, prmenuid
    py, px, psy, psx = y, x, sy, sx
    stp = StringVar(root)
    stp.set('Choose piece')
    opt = ['Queen', 'Rook', 'Bishop', 'Knight']
    prmenu = OptionMenu(root, stp, *opt, command=promote)
    prmenuid = dboard.create_window((x*50)+25, (y*50)+25, window=prmenu)
    
    global turn 
    turn = turn[0]
    print(turn)
    

def promote(p):
    global py, px, psy, psx, prmenuid
    dboard.delete(prmenuid)

    if p == 'Queen':
        board[py][px] = Queen(dboard, board, px, py, board[psy][psx].color)
    elif p == 'Rook':
        board[py][px] = Rook(dboard, board, px, py, board[psy][psx].color)
    elif p == 'Bishop':
        board[py][px] = Bishop(dboard, board, px, py, board[psy][psx].color)
    elif p == 'Knight':
        board[py][px] = Knight(dboard, board, px, py, board[psy][psx].color)

    if board[py][px].color == 'white':
        whitePieces.append(board[py][px])
    else:
        blackPieces.append(board[py][px])

    dboard.delete(board[psy][psx].dimg)
    board[psy][psx] = 0
    
    global turn
    if turn == 'b':
        turn = 'white'
    else:
        turn = 'black'
    
    
def delPiece(y, x):
    if board[y][x] in whitePieces:
        whitePieces.remove(board[y][x])
    else:
        blackPieces.remove(board[y][x])

    dboard.delete(board[y][x].dimg)


def checkIfPieceCheck(cp, ky, kx):
    global check, checkingPiece, cky, ckx
    cp.checkMoves()
    if [ky, kx] in cp.captures:
        # check
        check = True
        cky, ckx = ky, kx
        checkingPiece = cp


def checkIfCheck(s1, s2):
    kx, ky = 0, 0
    global check, checkingPiece, cky, ckx
    for i in s1:
        if isinstance(i, King):
            kx, ky = i.x, i.y
            break
    # see moves of moved piece
    print(moves[len(moves)-1][3][0], moves[len(moves)-1][3][1])
    mp = board[moves[len(moves)-1][3][0]][moves[len(moves)-1][3][1]]
    print('mp:', mp)
    checkIfPieceCheck(mp, ky, kx)
    # see moves of pieces of s2 if not check
    if not check:
        for j in s2:
            if j != mp:
                if isinstance(j, Bishop) or isinstance(j, Rook) or isinstance(j, Queen):
                    checkIfPieceCheck(j, ky, kx)


def turnOffCheck():
    global check, checkingPiece, cky, ckx
    check = False
    cky, ckx = 10, 10
    checkingPiece = 0


def checkIfStillCheck():
    global checkingPiece, ckx, cky
    checkingPiece.checkMoves()
    if [cky, ckx] in checkingPiece.captures:
        return True

    return False


def checkIfOppChecking(s, ky, kx):
    for p in s:
        if isinstance(p, Bishop) or isinstance(p, Rook) or isinstance(p, Queen):
            if board[p.y][p.x] == p:
                p.checkMoves()
                if [ky, kx] in p.captures:
                    return True
        else:
            continue

    return False


def draw():
    print('Draw')
    root.destroy()


def isPinned(y, x, sy, sx):
    if turn == 'white':
        s1 = whitePieces
        s2 = blackPieces
    else:
        s1 = blackPieces
        s2 = whitePieces

    # finding kings coordinates
    for k in s1:
        if isinstance(k, King):
            ky, kx = k.y, k.x
            break
        else:
            continue

    # temporarily moving piece there
    p = board[y][x]
    board[y][x] = board[sy][sx]
    board[sy][sx] = 0
    # checking if moved piece is pinned or not
    if not checkIfOppChecking(s2, ky, kx):
        # if not pinned then undo temporary move and proceed
        board[sy][sx] = board[y][x]
        board[y][x] = p
        return False
    else:
        # if moved piece is pinned just undo temporary move
        board[sy][sx] = board[y][x]
        board[y][x] = p
        return True


def click(event):
    print('clicked at:', event.x, event.y)
    if (event.x > 400) or (event.y > 400) or (event.x < 0) or (event.y < 0):
        print('out of bounds')
    else:
        x = event.x//50
        y = event.y//50
        print('squares:', x, y)
        global select
        global sx, sy
        global turn
        if (select == '') and (board[y][x] != 0):
            if board[y][x].color == turn:
                select = dboard.create_rectangle((50*x)+2, (50*y)+2, (50*x)+48, (50*y)+48, outline='red')
                sx, sy = x, y
        else:
            dboard.delete(select)
            select = ''
            global check, mn
            if (sy != '') and (sx != ''):
                move = board[sy][sx].checkIfMove([y, x])
                if move != 'illegal':
                    # checking if moved piece is pinned or not
                    if not isPinned(y, x, sy, sx):
                        if not check:
                            if move == 'move':
                                movePiece(y, x, sy, sx)

                            elif move == 'capture':
                                delPiece(y, x)
                                movePiece(y, x, sy, sx)

                            elif 'castle' in move:
                                if move[0] == 'k':
                                    castle(sy, sx, 7, 6, 5)

                                elif move[0] == 'q':
                                    castle(sy, sx, 0, 2, 3)

                            elif move == 'enpsnt':
                                delPiece(y-board[sy][sx].dir, x)
                                movePiece(y, x, sy, sx)

                            elif move == 'promote':
                                prommenu(y, x, sy, sx)

                            elif move == 'cpromote':
                                delPiece(y, x)
                                prommenu(y, x, sy, sx)

                        else:
                            # if check

                            global checkingPiece, cky, ckx
                            if move == 'capture':
                                # if capture is of checking piece then do it else dont
                                if [checkingPiece.y, checkingPiece.x] == [y, x]:
                                    delPiece(y, x)
                                    movePiece(y, x, sy, sx)
                                    turnOffCheck()

                            if move == 'move':
                                # temporariliy move piece
                                board[y][x] = board[sy][sx]
                                board[sy][sx] = 0
                                # check if moving piece has blocked check
                                if checkIfStillCheck():
                                    # if it hasnt undo temporary move
                                    board[sy][sx] = board[y][x]
                                    board[y][x] = 0
                                else:
                                    # if it has complete move and turn off check
                                    turnOffCheck()

                                    board[y][x].x = x
                                    board[y][x].y = y
                                    board[y][x].display()

                                    turn = switchclr(turn)

                            if move == 'promote':
                                board[y][x] = board[sy][sx]
                                board[sy][sx] = 0
                                if checkIfStillCheck():
                                    board[sy][sx] = board[y][x]
                                    board[y][x] = 0
                                else:
                                    board[sy][sx] = board[y][x]
                                    board[y][x] = 0
                                    turnOffCheck()
                                    prommenu(y, x, sy, sx)

                            if move == 'cpromote':
                                cp = board[y][x]
                                board[y][x] = board[sy][sx]
                                board[sy][sx] = 0
                                if checkIfStillCheck():
                                    board[sy][sx] = board[y][x]
                                    board[y][x] = cp
                                else:
                                    board[sy][sx] = board[y][x]
                                    board[y][x] = cp
                                    turnOffCheck()
                                    delPiece(y, x)
                                    prommenu(y, x, sy, sx)

                            if move == 'enpsnt':
                                cp = board[y][x]
                                board[y][x] = board[sy][sx]
                                board[sy][sx] = 0
                                if checkIfStillCheck():
                                    board[sy][sx] = board[y][x]
                                    board[y][x] = cp
                                else:
                                    turnOffCheck()

                                    delPiece(y - board[sy][sx].dir, x)
                                    board[y][x].x = x
                                    board[y][x].y = y
                                    board[y][x].display()

                                    turn = switchclr(turn)

                    # checking if move occured
                    if board[sy][sx] == 0:
                        # updating move
                        moves.append([typePiece(board[y][x]), [sy, sx], move, [y, x]])

                        # updating pboard
                        replicateBoard()

                        # checking if check
                        if turn == 'white':
                            checkIfCheck(whitePieces, blackPieces)
                        elif turn == 'black':
                            checkIfCheck(blackPieces, whitePieces)

                        if check:
                            moves[mn][2] += '#'
                            # check for checkmate
                            pass
                        mn += 1

                        for i in pboards[len(pboards)-1]:
                            print(i)
                        print('moves(divide by two for move no.): ', mn)

                        # checking threefold repetition
                        tr = 0
                        if len(pboards) >= 3:
                            for bn in range(len(pboards)-3, -1, -2):
                                if pboards[len(pboards)-1] == pboards[bn]:
                                    tr += 1
                                    if tr == 3:
                                        draw()

                        # checking 50 move rule
                        if mn >= 99:
                            global fiftydm
                            if ('capture' not in moves[mn-1][2]) and (moves[mn-1][0] != 'P'):
                                fiftydm += 1
                            else:
                                fiftydm = 0

                            if fiftydm == 50:
                                draw()

                        # check for stalemate
                        pass

                for i in moves:
                    print(i)

            sx, sy = '', ''

# castling, en passant and promotion are special moves

#
# stalemate
# if no posblMoves of one side, stalemate and game ends in draw
#

#
# check rules
# if after move any piece in same side has opponent king in self.captures, move is check
# no move except move which moves king out of checkingpiece.captures or captures checking piece is posbl
# this move could be block, king move or capture of checkingpiece
# if no posblMoves accomplishes this, checkmate = True and side who checked wins and game ends
#

#
# 50 move rule
# if no capture or pawn move has occured in past 50 moves then draw = True
#


root.bind("<Button-1>", click)

e = Button(root, text='Exit', height=3, width=9, command=root.quit)
e.grid(row=1, column=0)

root.mainloop()
