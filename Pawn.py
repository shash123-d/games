from PIL import ImageTk, Image


class Pawn:
    def __init__(self, dboard, board, x, y, color, oppPieces):
        self.dboard = dboard
        self.board = board
        self.oppPieces = oppPieces
        self.x = x
        self.y = y
        self.color = color
        self.epp = False
        self.epc = []

        if self.color == 'white':
            self.img = Image.open('/Users/sdudeja/PycharmProjects/Chess/whitePawn.png')
            self.dir = -1
        else:
            self.img = Image.open('/Users/sdudeja/PycharmProjects/Chess/blackPawn.png')
            self.dir = 1
        self.img = ImageTk.PhotoImage(self.img.resize((36, 36)))
        self.dimg = self.dboard.create_image((50*self.x)+25, (50*self.y)+25, image=self.img)

        self.posblMoves = []
        self.captures = []

    def display(self):
        self.dboard.delete(self.dimg)
        self.dimg = self.dboard.create_image((50 * self.x) + 25, (50 * self.y) + 25, image=self.img)

        for i in self.oppPieces:
            if isinstance(i, Pawn):
                i.epp = False

    def checkIfMove(self, m):
        self.checkMoves()
        print('pawn at:', self.y, self.x)
        print('posblmoves:', self.posblMoves)
        print('captures', self.captures)

        if self.epp:
            self.epp = False

        if m in self.posblMoves:
            if (m[0] == 0) or (m[0] == 7):
                return 'promote'

            # signify that pawn just moved up two squares
            if abs(m[0] - self.y) == 2:
                self.epp = True

            if m in self.epc:
                return 'enpsnt'
            
            return 'move'

        if m in self.captures:
            if (m[0] == 0) or (m[0] == 7):
                return 'cpromote'

            return 'capture'

        return 'illegal'

    def checkMoves(self):
        self.posblMoves = []
        self.captures = []

        # en passant logic

        if ((self.color == 'white') and (self.y == 3)) or ((self.color == 'black') and (self.y == 4)):
            if self.x > 0:
                if isinstance(self.board[self.y][self.x - 1], Pawn):
                    if self.board[self.y][self.x-1].epp:
                        self.posblMoves.append([self.y+self.dir, self.x-1])
                        self.epc.append([self.y+self.dir, self.x-1])
            
            if self.x < 7:
                if isinstance(self.board[self.y][self.x + 1], Pawn):
                    if self.board[self.y][self.x+1].epp:
                        self.posblMoves.append([self.y+self.dir, self.x+1])
                        self.epc.append([self.y + self.dir, self.x + 1])

        if self.board[self.y+self.dir][self.x] == 0:
            if ((self.y == 1) and (self.color == 'black')) or ((self.y == 6) and (self.color == 'white')):
                if self.board[self.y + (self.dir * 2)][self.x] == 0:
                    self.posblMoves.append([self.y + (self.dir * 2), self.x])

            self.posblMoves.append([self.y + self.dir, self.x])

        # check capture
        for i in range(-1, 2, 2):
            try:
                if self.board[self.y + self.dir][self.x+i] != 0:
                    if self.board[self.y + self.dir][self.x + i].color != self.color:
                        self.captures.append([self.y+self.dir, self.x+i])
            except IndexError:
                continue
