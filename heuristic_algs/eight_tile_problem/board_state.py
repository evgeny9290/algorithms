import itertools
import math
import numpy as np
from copy import deepcopy


class BoardState:
    def __init__(self, mat, target=None, heuristic='mismatch'):
        self.mat = mat
        self.target = target
        self.g = math.inf
        self.parent = None
        self.heuristic = heuristic
        self.f = 0

    def __eq__(self, other):
        return np.all(self.mat == other.mat)

    def __lt__(self, other):
        return self.f < other.f

    @property
    def h(self):
        if self.heuristic == 'mismatch':
            return np.sum(~(self.mat == self.target))
        elif self.heuristic == 'manhattan':
            return self.__manhattan_dist()
        else:
            return 0

    def __manhattan_dist(self):
        h = 0
        for num in range(1, np.size(self.mat)):
            num_i = np.where(self.mat == num)[0][0]
            num_j = np.where(self.mat == num)[1][0]
            target_i = np.where(self.target == num)[0][0]
            target_j = np.where(self.target == num)[1][0]
            h += np.abs(num_i - num_j) + np.abs(target_i - target_j)
        return h

    def __str__(self):
        return f'{self.mat}'

    def neighbors(self):
        result = []
        max_row, max_col = self.mat.shape[0], self.mat.shape[1]
        zero_i = np.where(self.mat == 0)[0][0]
        zero_j = np.where(self.mat == 0)[1][0]
        valid_idxs = list(itertools.product(list(range(max_col)), list(range(max_row))))
        if (zero_i - 1, zero_j) in valid_idxs:  # up swap
            result.append(self.__create_move_board(zero_i, zero_j, zero_i - 1, zero_j))
        if (zero_i + 1, zero_j) in valid_idxs:  # down swap
            result.append(self.__create_move_board(zero_i, zero_j, zero_i + 1, zero_j))
        if (zero_i, zero_j - 1) in valid_idxs:  # left swap
            result.append(self.__create_move_board(zero_i, zero_j, zero_i, zero_j - 1))
        if (zero_i, zero_j + 1) in valid_idxs:  # right swap
            result.append(self.__create_move_board(zero_i, zero_j, zero_i, zero_j + 1))

        return result

    def __create_move_board(self, i_from, j_from, i_to, j_to):
        cpy = deepcopy(self)
        cpy.mat[i_from, j_from], cpy.mat[i_to, j_to] = cpy.mat[i_to, j_to], cpy.mat[i_from, j_from]
        cpy.g = math.inf
        # cpy.parent = self
        return cpy


if __name__ == '__main__':
    target = np.array([
        [1, 2, 3],
        [8, 0, 4],
        [7, 6, 5]
    ])
    mat1 = np.array([
        [2, 8, 3],
        [1, 6, 4],
        [7, 0, 5]
    ])

    b2 = BoardState(mat1, target)
