from PIL import ImageTk, Image


class Knight:
    def __init__(self, dboard, board, x, y, color):
        self.dboard = dboard
        self.board = board
        self.x = x
        self.y = y
        self.color = color

        if self.color == 'white':
            self.img = Image.open('/Users/sdudeja/PycharmProjects/Chess/whiteKnight.png')
        else:
            self.img = Image.open('/Users/sdudeja/PycharmProjects/Chess/blackKnight.png')
        self.img = ImageTk.PhotoImage(self.img.resize((36, 36)))
        self.dimg = self.dimg = self.dboard.create_image((50*self.x)+25, (50*self.y)+25, image=self.img)

        self.posblMoves = []
        self.captures = []

    def display(self):
        self.dboard.delete(self.dimg)
        self.dimg = self.dboard.create_image((50*self.x)+25, (50*self.y)+25, image=self.img)

    def checkIfMove(self, m):
        self.checkMoves()
        print('Knight at:', self.y, self.x)
        print('posblmoves:', self.posblMoves)
        print('captures', self.captures)

        if m in self.posblMoves:
            return 'move'

        if m in self.captures:
            return 'capture'

        return 'illegal'

    def checkMoves(self):
        self.posblMoves = []
        self.captures = []

        #      -2-1, -2+1
        # -1-2,          -1+2
        #           k
        # +1-2,          +1+2
        #      +2-1, +2+1

        for i in range(-2, 3):
            if i == 0:
                continue

            if abs(i) == 2:
                n = 1
            else:
                n = 2

            self.addMove(self.y + i, self.x + n)
            self.addMove(self.y + i, self.x - n)

    def addMove(self, m, n):
        try:
            if (m >= 0) and (n >= 0):
                if self.board[m][n] == 0:
                    self.posblMoves.append([m, n])
                else:
                    if self.board[m][n].color != self.color:
                        self.captures.append([m, n])
        except IndexError:
            pass
