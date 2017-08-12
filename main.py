import numpy as np
import time

class HyperSudokuSolver:
    """
    This class implements a solver for hypersudoku-puzzles.

    Design principles:
        uses backtracking algorithm brute force search
        zero is a special character for 'empty cell'
    """

    def __init__(self):
        self.puzzle = np.array([
            [0,0,0,0,0,0,0,1,0],
            [0,0,2,0,0,0,0,3,4],
            [0,0,0,0,5,1,0,0,0],
            [0,0,0,0,0,6,5,0,0],
            [0,7,0,3,0,0,0,8,0],
            [0,0,3,0,0,0,0,0,0],
            [0,0,0,0,8,0,0,0,0],
            [5,8,0,0,0,0,9,0,0],
            [6,9,0,0,0,0,0,0,0]
        ])
        self.given = (self.puzzle != 0)
        self.done = False

    @staticmethod
    def validate_segment(segment):
        """
        Takes an array (or matrix) object and checks if any non-zero number appears twice.
        """
        values = segment.flatten()
        if len(values) != 9:
            print('WARNING: can only validate segments with 9 elements.')
        unique, counts = np.unique(values, return_counts=True)
        for i in range(len(unique)):
            if unique[i] == 0:
                continue
            if counts[i] > 1:
                return False
        return True

    def full_validation(self):
        """
        Orchestrator to call validate_segment on all the necessary segments.
        """
        # rows
        for r in range(9):
            if not self.validate_segment(self.puzzle[r]):
                return False
        # columns
        for c in range(9):
            if not self.validate_segment(self.puzzle[:, c]):
                return False
        # sectors
        for r in range(0, 9, 3):
            for c in range(0, 9, 3):
                if not self.validate_segment(self.puzzle[r:r+3, c:c+3]):
                    return False
        # hyper-sectors
        for r in [1, 5]:
            for c in [1, 5]:
                if not self.validate_segment(self.puzzle[r:r+3, c:c+3]):
                    return False
        return True

    def validate(self, r, c):
        # row
        if not self.validate_segment(self.puzzle[r]):
            return False
        # column
        if not self.validate_segment(self.puzzle[:, c]):
            return False
        # sector
        r_sector = (r // 3) * 3
        c_sector = (c // 3) * 3
        if not self.validate_segment(self.puzzle[r_sector:r_sector + 3, c_sector:c_sector + 3]):
            return False
        # hyper-sector
        if r in [1, 2, 3, 5, 6, 7] and c in [1, 2, 3, 5, 6, 7]:
            # in a hyper-sector
            r_hyper_sector = (r > 4) * 4 + 1
            c_hyper_sector = (c > 4) * 4 + 1
            if not self.validate_segment(self.puzzle[r_hyper_sector:r_hyper_sector + 3,
                                         c_hyper_sector:c_hyper_sector + 3]):
                return False
        return True

    def increment(self, r, c):
        c += 1
        if c >= 9:
            c = 0
            r += 1
        if r < 9 and c  < 9 and self.given[r, c]:
            r, c = self.increment(r, c)
        return r, c

    def check_done(self, r, c):
        if r > 8:
            self.done = True

    def fill(self, r, c):
        self.check_done(r, c)
        if self.done:
            return
        for value in range(1, 10):
            self.puzzle[r, c] = value
            # print(self.puzzle)
            if self.validate(r, c):
                r_next, c_next = self.increment(r, c)
                self.fill(r_next, c_next)
                if self.done:
                    return
        self.puzzle[r, c] = 0

    def solve(self):
        start_time = time.time()
        r, c = self.increment(0, -1)
        self.fill(r, c)
        if self.done:
            print('Found solution:')
            print(self.puzzle)
        else:
            print('No solution found.')
        print(f'\nTime: {np.round(time.time() - start_time, 3)}s')

if __name__ == '__main__':
    hss = HyperSudokuSolver()
    hss.solve()