import random
from main import Tetris
from multiprocessing import Process
import threading
import pyautogui
import time

# population initialization
# fitness calculation
# selection
# crossover
# mutation

# figure out ui and drawing each game
# figure out fitness equation
# figure out genes


class Population:
    def __init__(self, n=0):
        self.game = Tetris(True)
        # if n == 0:
        #     yoff = int(self.game.root.winfo_screenwidth() / 4 - self.game.root.winfo_reqwidth())
        # else:
        #     yoff = int(self.game.root.winfo_screenwidth()*3 / 4 - self.game.root.winfo_reqwidth())
        # self.game.root.geometry('+{}+{}'.format(2*n*(self.game.root.winfo_reqwidth()), 0))

        self.gameStart()

    def gameStart(self):
        while 1:
            u = self.game.current.update()
            if u == 0:
                self.game.newPiece()
                for row in self.game.grid:
                    for b in row:
                        if b != 0:
                            print(1, end=' ')
                        else:
                            print(0, end=' ')
                    print()
                print()
            elif u == -1:
                self.game.root.destroy()
                print('game over')

            self.move()

            self.game.game.update()
            time.sleep(self.game.wait)

    # def allMoves(self):
        # moves = ['left', 'right', 'down   ', 'space', 'z', 'c']

        # r = random.randint(0, len(moves)-1)
        # print(moves[r])
        # pyautogui.press(moves[r])


population = []
processes = []


def child(n):
    population.append(Population(n))


if __name__ == '__main__':
    size = 1
    for i in range(size):
        processes.append(Process(target=child, args=(i, )))

    for i in range(size):
        processes[i].start()
        print('process:', i)
        time.sleep(1)
        pyautogui.hotkey('command', 'tab')
