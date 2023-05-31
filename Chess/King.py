from PIL import ImageTk, Image
from Pawn import Pawn
from Rook import Rook
# add check
# add checkmate


class King:
    def __init__(self, dboard, board, x, y, color, oppPieces):
        self.dboard = dboard
        self.board = board
        self.oppPieces = oppPieces
        self.x = x
        self.y = y
        self.color = color
        self.moved = False

        if self.color == 'white':
            self.img = Image.open('/Users/sdudeja/PycharmProjects/Chess/whiteKing.png')
        else:
            self.img = Image.open('/Users/sdudeja/PycharmProjects/Chess/blackKing.png')
        self.img = ImageTk.PhotoImage(self.img.resize((36, 36)))
        self.dimg = self.dboard.create_image((50*self.x)+25, (50*self.y)+25, image=self.img)

        self.posblMoves = []
        self.captures = []

        # check rules
        # if after move moved piece has king in self.captures move is check
        # no move except move which moves king out of checkingpiece.captures or captures checking piece is posbl
        # could be block, king move or capture of checkingpiece
        # if no posblMoves accomplishes this, checkmate = True and side who checked wins and game ends
        #
        #
        #
        # P.S.
        # careful bout discovered checks
        # figure out pins

    def display(self):
        self.moved = True
        self.dboard.delete(self.dimg)
        self.dimg = self.dboard.create_image((50 * self.x) + 25, (50 * self.y) + 25, image=self.img)

    def checkIfMove(self, m):
        self.checkMoves()
        print('King at:', self.y, self.x)
        print('posblmoves:', self.posblMoves)
        print('captures', self.captures)

        if m in self.posblMoves:
            if self.color == 'black':
                start = 0
            else:
                start = 7

            if m == [start, 6]:
                return 'kcastle'
            elif m == [start, 2]:
                return 'qcastle'

            return 'move'

        if m in self.captures:
            return 'capture'

        return 'illegal'

    def checkMoves(self):
        self.posblMoves = []
        self.captures = []

        # -1-1, -10, -1+1
        # 0-1, 00, 0+1
        # +1-1, +10, +1+1

        # castling
        if not self.moved:
            # check king rook castling rights
            # check pieces between king and king rook
            # check queen rook castling rights
            # check pieces between king and queen rook
            # no opponent piece can have vision of castling squares
            if isinstance(self.board[self.y][7], Rook):
                if self.board[self.y][7].side == 'king':
                    if not self.board[self.y][7].moved:
                        # check if anything in between king and rook
                        obst = False
                        for a in range(5, 7):
                            if self.board[self.y][a] != 0:
                                obst = True

                        if not obst:
                            # check whether enemPieces look at castling squares (k:765, q:32)
                            opvis = False
                            for a in self.oppPieces:
                                if isinstance(a, Pawn):
                                    if abs(a.y-self.y) == 1:
                                        if a.x in [7, 6, 5, 4]:
                                            opvis = True
                                elif isinstance(a, King):
                                    if abs(a.y-self.y) == 1:
                                        if a.x == 6:
                                            opvis = True
                                else:
                                    csq = [[self.y, 7], [self.y, 6], [self.y, 5]]
                                    a.checkMoves()
                                    for b in csq:
                                        if b in a.posblMoves:
                                            opvis = True

                            if not opvis:
                                self.posblMoves.append([self.y, 6])

            if isinstance(self.board[self.y][0], Rook):
                if self.board[self.y][0].side == 'queen':
                    if not self.board[self.y][0].moved:
                        obst = False
                        for a in range(1, 4):
                            if self.board[self.y][a] != 0:
                                obst = True

                        if not obst:
                            opvis = False
                            for a in self.oppPieces:
                                if isinstance(a, Pawn):
                                    if abs(a.y - self.y) == 1:
                                        if a.x in [4, 3, 2, 1]:
                                            opvis = True
                                elif isinstance(a, King):
                                    if abs(a.y - self.y) == 1:
                                        if a.x == 2:
                                            opvis = True
                                else:
                                    csq = [[self.y, 3], [self.y, 2]]
                                    a.checkMoves()
                                    for b in csq:
                                        if b in a.posblMoves:
                                            opvis = True

                            if not opvis:
                                self.posblMoves.append([self.y, 2])

        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i == 0) and (j == 0):
                    continue

                try:
                    if (self.y+i >= 0) and (self.x+j >= 0):
                        if self.board[self.y+i][self.x+j] == 0:
                            safe = True
                            for m in self.oppPieces:
                                if isinstance(m, King):
                                    if (abs(m.y - (self.y+i)) <= 1) and (abs(m.x - (self.x+j)) <= 1):
                                        safe = False
                                elif isinstance(m, Pawn):
                                    if m.y + m.dir == self.y + i:
                                        if (m.x + 1 == self.x + j) or (m.x - 1 == self.x + j):
                                            safe = False
                                else:
                                    # uncomment when done with everything else
                                    m.checkMoves()
                                    if [self.y+i, self.x+j] in m.posblMoves:
                                        safe = False
                            if safe:
                                self.posblMoves.append([self.y+i, self.x+j])
                        else:
                            if self.board[self.y+i][self.x+j].color != self.color:
                                # see if king can capture opponent piece
                                # check if oppking is protecting
                                opking = 0
                                for m in self.oppPieces:
                                    if isinstance(m, King):
                                        opking = m

                                if (abs(opking.y - (self.y + i)) <= 1) and (abs(opking.x - (self.x + j)) <= 1):
                                    continue
                                else:
                                    # if opking is not protecting then capture on board and check oppieces.captures
                                    piece = self.board[self.y+i][self.x+j]
                                    self.board[self.y+i][self.x+j] = self.board[self.y][self.x]
                                    unprotected = True
                                    for p in self.oppPieces:
                                        if isinstance(p, King):
                                            continue
                                        elif isinstance(p, Pawn):
                                            if p.y + p.dir == self.y + i:
                                                if (p.x + 1 == self.x + j) or (p.x - 1 == self.x + j):
                                                    unprotected = False
                                        else:
                                            # uncomment when done with everything else
                                            p.checkMoves()
                                            if [self.y+i, self.x+j] in p.captures:
                                                unprotected = False
                                    if unprotected:
                                        self.captures.append([self.y+i, self.x+j])

                                    self.board[self.y+i][self.x+j] = piece
                except IndexError:
                    continue
