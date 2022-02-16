from board import Direction, Rotation, Shape, Block
from random import Random
import time
import math


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

class SimplePlayer(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)

    def choose_action(self, board):
        bestscore = 0
        bestmove = None
        for xtarget in range(10):
            score, move = self.try_move(board, xtarget)
            time.sleep(10)
            if score > bestscore:
                bestscore = score
                bestmove = move
        return bestmove

    def try_move(self, board, xtarget):
        clone = board.clone()
        firstmove = None
        while True:
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
                score = self.score_board(clone)
                return score, firstmove

    def score_board(self, clone):
        miny = 23
        for x, y in clone.cells:
            if y < miny:
                miny = y
        print(miny)
        return miny


class ChrisPlayer(Player):

    def choose_action(self, board):
        bestscore = -10000
        bestmove = None
        for rotation in range(4):
            for xtarget in range(10):
                score, move = self.try_move(board, xtarget, rotation)
                print(score)
                if score > bestscore:
                    bestscore = score
                    bestmove = move
        return bestmove


    def try_move(self, board, xtarget, rotation):
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


    def calScore(self,clone):

        lines_removed = 0
        hole_line = [0]*10
        hole_total = [0]*10
        top = [0]*10

        num_of_holes = 0
        for y in range(23, -1, -1):
            exist_hole = False
            exist_block = False
            for x in range(10):
                if (x, y) in clone.cells:
                    exist_block = True
                    top[x] = 24 - y
                    if hole_line[x] > 0:
                        hole_total[x] += hole_line[x]
                        hole_line[x] = 0
                else:
                    exist_hole = True
                    hole_line[x] += 1
            if not exist_block:
                break
            condition = not exist_hole and exist_block
            if condition:
                lines_removed += 1

        for i in hole_total:
            num_of_holes += i ** 0.7

        max_top = max(top) - lines_removed

        score = lines_removed * 2 - num_of_holes * 1.5 - max_top * 2

        return score



   def calScore(self, clone):
        height = self.calHeight(clone)
        lines_removed = self.calLinesRemoved(clone)
        row_trans = self.calRowTrans(clone)
        col_trans = self.calColTrans(clone)
        holes = self.calHoles(clone)
        wells = self.calWells(clone)

        score = -45 * height + 102 * lines_removed - 32 * row_trans - 93 * col_trans - 79 * holes - 34 * wells
        print(height, lines_removed, row_trans, col_trans, holes, wells)

        return score

    def calHeight(self, clone):
        height = 23
        for x, y in clone.cells:
            if y < height:
                height = y
        print(height)
        height = 23 - height
        return height


    def calLinesRemoved(self,clone):
        lines_removed = 0
        for y in range(23, -1, -1):
            exist_hole = False
            exist_block = False
            for x in range(10):
                if (x, y) in clone.cells:
                    exist_block = True
                else:
                    exist_hole = True
            condition = not exist_hole and exist_block
            if condition:
                lines_removed += 1
        return lines_removed

    def calRowTrans(self, clone):
        count = 0
        for y in range(23, 0, -1):
            for x in range(10):
                condition1 = ((x, y) in clone.cells) and ((x+1, y) not in clone.cells)
                condition2 = ((x, y) not in clone.cells) and ((x+1, y)  in clone.cells)
                if condition1 or condition2:
                    count += 1
        return count

    def calColTrans(self, clone):
        count = 0
        for x in range(10):
            for y in range(23, 1, -1):
                condition1 = ((x, y) in clone.cells) and ((x, y-1) not in clone.cells)
                condition2 = ((x, y) not in clone.cells) and ((x, y-1)  in clone.cells)
                if condition1 or condition2:
                    count += 1
        return count

    def calHoles(self, clone):
        count = 0
        for x in range(10):
            holes_in_col = None
            for y in range(24):
                condition1 = (holes_in_col == None) and ((x, y) in clone.cells)
                condition2 = (holes_in_col != None) and ((x, y) not in clone.cells)
                if condition1:
                    holes_in_col = 0
                if condition2:
                    holes_in_col += 1
            if holes_in_col is not None:
                count += holes_in_col
        return count

    def calWells(self, clone):
        sums = [0, 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78, 91, 105, 120, 136, 153, 171, 190, 210, 231, 253, 276]
        total = 0
        count = 0
        for x in range(10):
            for y in range(24):
                if (x, y) not in clone.cells:
                    condition1 = ((x-1) < 0) or ((x-1, y) in clone.cells)
                    condition2 = ((x+1) > 9) or ((x+1, y) in clone.cells)
                    if condition1 and condition2:
                        count += 1
                    else:
                        total += sums[count]
                        count = 0
        return total





#SelectedPlayer = ChrisPlayer
SelectedPlayer = SimplePlayer
#SelectedPlayer = RandomPlayer
