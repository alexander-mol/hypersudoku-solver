import numpy as np
import time
import copy


class HyperSudokuSolver:
    """
    This class implements a solver for hypersudoku-puzzles.

    Design principles:
        uses backtracking algorithm brute force search
        zero is a special character for 'empty cell'
    """

    def __init__(self, puzzle):
        self.puzzle = copy.copy(puzzle)
        self.given = (self.puzzle != 0)
        self.done = False
        self.iteration_count = 0

    # not used
    def count_options(self, r, c):
        """
        Count the number of remaining possible values for cell (r, c) given what is already set on the board.
        """
        if self.puzzle[r, c] != 0:
            return 1
        values_taken = set()
        values_taken = values_taken.union(set(self.puzzle[r].flatten()))  # row
        values_taken = values_taken.union(set(self.puzzle[:, c].flatten()))  # column
        # sector
        r_sector = (r // 3) * 3
        c_sector = (c // 3) * 3
        values_taken = values_taken.union(set(self.puzzle[r_sector:r_sector + 3, c_sector:c_sector + 3].flatten()))
        # hyper-sector
        if r in [1, 2, 3, 5, 6, 7] and c in [1, 2, 3, 5, 6, 7]:
            # in a hyper-sector
            r_hyper_sector = (r > 4) * 4 + 1
            c_hyper_sector = (c > 4) * 4 + 1
            values_taken = values_taken.union(set(self.puzzle[r_hyper_sector:r_hyper_sector + 3,
                                                  c_hyper_sector:c_hyper_sector + 3].flatten()))
        return 10 - len(values_taken)

    # not used
    def score_orientation(self):
        # return self.count_options(0, 0)
        score = 1
        r, c = 0, -1
        while r < 1:
            r, c = self.increment(r, c)
            score *= self.count_options(r, c)
        return np.log(score)
    
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

    # not used
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
        """
        Go to the next empty cell after r, c (in left-to-right order, going to the next row at the end of a line).
        """
        c += 1
        if c >= 9:
            c = 0
            r += 1
        if r < 9 and c < 9 and self.given[r, c]:
            r, c = self.increment(r, c)
        return r, c

    def check_done(self, r, c):
        """
        Check if the puzzle has been solved.
        """
        if r > 8:
            self.done = True

    def fill(self, r, c):
        """
        Recursive method that performs the backtracking algorithm.
        """
        self.iteration_count += 1
        self.check_done(r, c)
        if self.done:
            return
        for value in range(1, 10):
            self.puzzle[r, c] = value
            # print(self.puzzle)  # for debugging
            if self.validate(r, c):
                r_next, c_next = self.increment(r, c)
                self.fill(r_next, c_next)
                if self.done:
                    return
        self.puzzle[r, c] = 0

    def solve(self):
        """
        Main method - starts solving process and reports performance metrics.
        """
        print('Started searching...')
        start_time = time.time()
        r, c = self.increment(0, -1)
        self.fill(r, c)
        if self.done:
            print('Found solution:')
            print(self.puzzle)
        else:
            print('No solution found.')
        print(f'\nTime: {np.round(time.time() - start_time, 3)} s')
        print(f'Iterations: {self.iteration_count}')
        print(f'Avg time/iter: {np.round((time.time() - start_time) / self.iteration_count * 1e6, 0)} ns\n')

if __name__ == '__main__':
    puzzle = np.array([
        # [0,0,0,0,0,0,0,1,0],
        # [0,0,2,0,0,0,0,3,4],
        # [0,0,0,0,5,1,0,0,0],
        # [0,0,0,0,0,6,5,0,0],
        # [0,7,0,3,0,0,0,8,0],
        # [0,0,3,0,0,0,0,0,0],
        # [0,0,0,0,8,0,0,0,0],
        # [5,8,0,0,0,0,9,0,0],
        # [6,9,0,0,0,0,0,0,0]
        [0, 0, 0, 0, 0, 0, 0, 7, 0],
        [0, 0, 4, 0, 0, 0, 0, 0, 0],
        [0, 0, 7, 0, 0, 8, 5, 0, 0],
        [0, 0, 6, 0, 0, 0, 0, 2, 5],
        [0, 0, 0, 0, 0, 0, 0, 0, 3],
        [0, 0, 0, 8, 0, 0, 0, 1, 4],
        [0, 0, 5, 0, 3, 0, 0, 9, 1],
        [2, 1, 0, 9, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 5, 0]
    ])
    # puzzle = np.flip(np.rot90(np.rot90(np.rot90(np.rot90(puzzle)))), 1)
    # hss = HyperSudokuSolver(puzzle)
    # print(f'Options (0,0): {hss.score_orientation()}')
    # hss.solve()
    # puzzle = np.rot90(np.rot90(np.rot90(puzzle)))
    # hss = HyperSudokuSolver(puzzle)
    # print(f'Options (0,0): {hss.score_orientation()}')
    # hss.solve()
    # puzzle = np.rot90(np.rot90(puzzle))
    # hss = HyperSudokuSolver(puzzle)
    # print(f'Options (0,0): {hss.score_orientation()}')
    # hss.solve()
    # puzzle = np.rot90(puzzle)
    # hss = HyperSudokuSolver(puzzle)
    # print(f'Options (0,0): {hss.score_orientation()}')
    # hss.solve()

    orientations = [puzzle, np.rot90(puzzle), np.rot90(np.rot90(puzzle)), np.rot90(np.rot90(np.rot90(puzzle)))]
    from multiprocessing import Pool
    pool = Pool(4)
    for orientation in orientations:
        solver = HyperSudokuSolver(orientation)
        pool.apply_async(solver.solve)
    pool.close()
    pool.join()
