from board import Direction, Rotation
from random import Random
import time

class Player:
    def choose_action(self, board):
        raise NotImplementedError

class RandomPlayer(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)

    def choose_action(self, board):
        return self.random.choice([
                Direction.Left,
                Direction.Right,
                Direction.Down,
                Rotation.Anticlockwise,
                Rotation.Clockwise,
        ])

class ChrisPlayer(Player):

    def choose_action(self, board):
        global score_before
        score_before = board.score
        bestscore = -10000
        bestmove = None
        for rotation in range(4):
            for xtarget in range(10):
                score, move = self.try_move(board, xtarget, rotation)
                if score > bestscore:
                    bestscore = score
                    bestmove = move
        return bestmove


    def try_move(self, board, xtarget, rotation):
        global score_before
        clone = board.clone()
        tryrotate = None

        if rotation == 1:
            tryrotate = [Rotation.Clockwise]
            res1 = clone.rotate(tryrotate)
            if res1:
                score = self.calScore(clone)
                return score, tryrotate
            else:
                clone.rotate(Rotation.Clockwise)

        if rotation == 2:
            tryrotate = [Rotation.Clockwise, Rotation.Clockwise]
            res1 = clone.rotate(tryrotate)
            if res1:
                score = self.calScore(clone)
                return score, tryrotate
            else:
                clone.rotate(Rotation.Clockwise)
                clone.rotate(Rotation.Clockwise)

        if rotation == 3:
            tryrotate = [Rotation.Anticlockwise]
            res1 = clone.rotate(tryrotate)
            if res1:
                score = self.calScore(clone)
                return score, tryrotate
            else:
                clone.rotate(Rotation.Anticlockwise)

        firstmove = None
        while True:
            try:
                a = clone.falling.left
            except AttributeError:
                return 0, [Direction.Drop]
            else:
                if clone.falling.left < xtarget:
                    trymove = Direction.Right
                elif clone.falling.left > xtarget:
                    trymove = Direction.Left
                else:
                    trymove = Direction.Drop
                if firstmove is None:
                    firstmove = trymove
                res = clone.move(trymove)
                if res:
                    score = self.calScore(clone)
                    if rotation == 0:
                        return score, [firstmove]
                    if rotation == 1:
                        return score, [Rotation.Clockwise, firstmove]
                    if rotation == 2:
                        return score, [Rotation.Clockwise, Rotation.Clockwise, firstmove]
                    if rotation == 3:
                        return score, [Rotation.Anticlockwise, firstmove]

    def calScore(self, clone):
        global score_before
        lines_removed = 0
        row_trans = 0
        col_trans = 0
        holes = 0
        wells = 0
        total = 0
        height = 23

        score_difference = clone.score - score_before

        if 0 <= score_difference < 100:
            lines_removed = 0
        elif 100 <= score_difference < 400:
            lines_removed = 1
        elif 400 <= score_difference < 800:
            lines_removed = 2
        elif 800 <= score_difference < 1600:
            lines_removed = 3
        else:
            lines_removed = 4



        for y in range(23, 0, -1):
            for x in range(10):
                condition1 = ((x, y) in clone.cells) and ((x + 1, y) not in clone.cells)
                condition2 = ((x, y) not in clone.cells) and ((x + 1, y) in clone.cells)
                if condition1 or condition2:
                    row_trans += 1

        for x in range(10):
            for y in range(23, 1, -1):
                condition3 = ((x, y) in clone.cells) and ((x, y - 1) not in clone.cells)
                condition4 = ((x, y) not in clone.cells) and ((x, y - 1) in clone.cells)
                if condition3 or condition4:
                    col_trans += 1

        for x in range(10):
            holes_in_col = None
            for y in range(24):
                condition5 = (holes_in_col == None) and ((x, y) in clone.cells)
                condition6 = (holes_in_col != None) and ((x, y) not in clone.cells)
                if condition5:
                    holes_in_col = 0
                if condition6:
                    holes_in_col += 1
                if (x, y) not in clone.cells:
                    condition7 = ((x - 1) < 0) or ((x - 1, y) in clone.cells)
                    condition8 = ((x + 1) > 9) or ((x + 1, y) in clone.cells)
                    if condition7 and condition8:
                        wells += 1
                    else:
                        i = 0
                        while i<=wells:
                            total += i
                            i += 1
                        wells = 0
            if holes_in_col is not None:
                holes += holes_in_col

        for x, y in clone.cells:
            if y < height:
                height = y
        height = 23 - height

        score = 34 * lines_removed - 16 * row_trans - 46.5 * col_trans - 39.5 * holes - 17 * total - 22.5 * height

        return score



SelectedPlayer = ChrisPlayer
#SelectedPlayer = RandomPlayer
