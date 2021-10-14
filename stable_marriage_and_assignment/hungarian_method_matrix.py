import numpy as np
import math


def step_1_and_2(matrix):
    dim = matrix.shape[0]
    cur_mat = matrix.copy()

    for row_num in range(dim):
        cur_mat[row_num] -= np.min(cur_mat[row_num])

    for col_num in range(dim):
        cur_mat[:, col_num] -= np.min(cur_mat[:, col_num])

    return cur_mat,dim


def step_3_helper_1(zeroes_mat, marked_zeroes):
    #get row/col with minimum number of zeroes [number of zeroes, index of row/col]
    min_row = [math.inf, -1]

    for row_idx in range(zeroes_mat.shape[0]):
        if 0 < np.sum(zeroes_mat[row_idx]) < min_row[0]:
            min_row = [np.sum(zeroes_mat[row_idx]), row_idx]
    # print(zeroes_mat)

    #get marked_zero location and mark corresponding row/col as False
    zero_idx = np.where(zeroes_mat[min_row[1]])[0][0]
    marked_zeroes.append((min_row[1], zero_idx))
    zeroes_mat[min_row[1], :] = False
    zeroes_mat[:, zero_idx] = False


def step_3_helper_2(zeroes_mat, marked_zeroes):
    #mark every single row/col with False and get zeroes locations
    while True in zeroes_mat:
        step_3_helper_1(zeroes_mat, marked_zeroes)


def step_3(matrix):
    cur_mat = matrix
    zero_bool_mat = (cur_mat == 0)
    zeroes_mat_cpy = zero_bool_mat.copy()
    marked_zeroes = []
    step_3_helper_2(zeroes_mat_cpy, marked_zeroes)

    #get indexes of rows and cols with marked zeroes
    marked_zeroes_rows = []
    marked_zeroes_cols = []
    for i in range(len(marked_zeroes)):
        marked_zeroes_rows.append(marked_zeroes[i][0])
        marked_zeroes_cols.append(marked_zeroes[i][1])

    #
    non_marked_row = list(set(range(cur_mat.shape[0])) - set(marked_zeroes_rows))
    marked_cols = []

    flag = True
    while flag:
        flag = False
        for i in range(len(non_marked_row)):
            row_arr = zero_bool_mat[non_marked_row[i], :]
            for j in range(len(row_arr)):
                if row_arr[j] == True and j not in marked_cols:
                    marked_cols.append(j)
                    flag = True

        for row_num, col_num in marked_zeroes:
            if row_num not in non_marked_row and col_num in marked_cols:
                non_marked_row.append(row_num)
                flag = True

    marked_rows = list(set(range(cur_mat.shape[0])) - set(non_marked_row))
    return marked_zeroes, marked_rows, marked_cols
            # for j in range(row_arr.shape[0])


def step_4(matrix,cover_rows, cover_cols):
    cur_mat = matrix
    non_zero_elems = []

    for row in range(len(cur_mat)):
        if row not in cover_rows:
            for i in range(len(cur_mat[row])):
                if i not in cover_cols:
                    non_zero_elems.append(cur_mat[row][i])
    min_num = min(non_zero_elems)

    for row in range(len(cur_mat)):
        if row not in cover_rows:
            for i in range(len(cur_mat[row])):
                if i not in cover_cols:
                    cur_mat[row, i] -= min_num

    for i in range(len(cover_rows)):
        for j in range(len(cover_cols)):
            cur_mat[cover_rows[i], cover_cols[j]] += min_num

    return cur_mat


def hungarian_matrix_method(matrix):
    mat, dim = step_1_and_2(matrix)
    zero_count = 0

    while zero_count < dim:
        res_pos, marked_rows, marked_cols = step_3(mat)
        zero_count = len(marked_cols) + len(marked_rows)

        if zero_count < dim:
            mat = step_4(mat, marked_rows, marked_cols)

    return res_pos


def calc_minimum_cost(matrix, positions):
    res = 0
    ans_mat = np.zeros((matrix.shape[0], matrix.shape[1]), dtype=int)
    for i in range(len(positions)):
        res += matrix[positions[i][0],positions[i][1]]
        ans_mat[positions[i][0], positions[i][1]] = matrix[positions[i][0], positions[i][1]]
    return res, ans_mat


if __name__ == '__main__':
    mat = np.array([[5,5,20,2,6],
                    [7,4,2,3,4],
                    [9,3,5,15,3],
                    [7,2,6,7,2],
                    [6,5,7,9,1]])
    print(mat)
    match = hungarian_matrix_method(mat.copy())
    print(match)
    # print(match)
    # print('##########################')
    ans,ans_mat = calc_minimum_cost(mat, match)
    print(ans)
    print(ans_mat)


