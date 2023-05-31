from PIL import ImageTk, Image


class Queen:
    def __init__(self, dboard, board, x, y, color):
        self.dboard = dboard
        self.board = board
        self.x = x
        self.y = y
        self.color = color

        if self.color == 'white':
            self.img = Image.open('/Users/sdudeja/PycharmProjects/Chess/whiteQueen.png')
        else:
            self.img = Image.open('/Users/sdudeja/PycharmProjects/Chess/blackQueen.png')
        self.img = ImageTk.PhotoImage(self.img.resize((36, 36)))
        self.dimg = self.dboard.create_image((50 * self.x) + 25, (50 * self.y) + 25, image=self.img)

        self.posblMoves = []
        self.captures = []

    def display(self):
        self.dboard.delete(self.dimg)
        self.dimg = self.dboard.create_image((50*self.x)+25, (50*self.y)+25, image=self.img)

    def checkIfMove(self, m):
        self.checkMoves()
        print('Queen at:', self.y, self.x)
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

        # -1-1, -10, -1+1
        #  0-1,  00,  0+1
        # +1-1, +10, +1+1

        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i == 0) and (j == 0):
                    continue
                self.addMove(i, j)

    def addMove(self, i, j):
        m = self.y + i
        n = self.x + j
        if (m >= 0) and (n >= 0):
            try:
                while (self.board[m][n] == 0) and (m >= 0) and (n >= 0):
                    self.posblMoves.append([m, n])
                    m = m + i
                    n = n + j

                if (m >= 0) and (n >= 0):
                    if self.board[m][n].color != self.color:
                        self.captures.append([m, n])

            except IndexError:
                pass

