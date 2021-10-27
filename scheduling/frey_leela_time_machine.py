import math
import numpy as np
from graph.graph_package.graph import Graph
import pandas as pd
from collections import defaultdict
from copy import deepcopy


class PrecSchedule:
    def __init__(self, file_name=None, graph=None):
        if file_name is not None and graph is not None:
            self.file_name = file_name
            self.fi_list, self.pi_list, self.adj_mat = self.__init_csv()
            self.graph = self.__graph_init(graph)

    def __init_csv(self):
        data_frame = pd.read_csv(self.file_name)
        data_frame_fi = list(map(lambda x: float(x), data_frame.columns.values))
        data_frame_pi = list(map(lambda x: int(x), data_frame.iloc[0]))
        data_frame_adj_matrix = data_frame.to_numpy()[1:]
        return data_frame_fi, data_frame_pi, data_frame_adj_matrix

    def __str__(self):
        return f'{self.file_name}:\n fi_list: {self.fi_list}\n pi_list: {self.pi_list}\n adj_matrix:\n{self.adj_mat}\n'

    def __graph_init(self, graph):
        mat_graph = defaultdict(dict)
        for i in range(len(self.adj_mat)):
            for j in range(len(self.adj_mat[0])):
                if self.adj_mat[i][j] != 0:
                    mat_graph[i][j] = self.adj_mat[i][j]

        for src, neighbors in mat_graph.items():
            for dst in neighbors.keys():
                graph.add_edge(src, dst)

        return graph

    def display_graph(self):
        print(self.graph)

    def compute_schedule(self):
        return self.__lawler()

    # @staticmethod
    # def combine_schedules(first, second, connection_mat_file_name):
    #     df = pd.read_csv(connection_mat_file_name, header=None)
    #     conn_mat = df.to_numpy()
    #     combined_mat = PrecSchedule.__concatenate_mats(left=first.adj_mat,
    #                                                    diagonal=second.adj_mat,
    #                                                    right=conn_mat)
    #     print(combined_mat)
    #     combined_fi = first.fi_list + second.fi_list
    #     combined_pi = first.pi_list + second.pi_list
    #
    #     combined = PrecSchedule()
    #     g = Graph(kind='list', directed=True)
    #     combined.fi_list, combined.pi_list, combined.adj_mat = combined_fi, combined_pi, combined_mat
    #     combined.graph = combined.__graph_init(g)
    #     res = combined.__lawler()
    #
    #     return res

    # @staticmethod
    # def __concatenate_mats(left, diagonal, right):
    #     zeros_pad = np.zeros(shape=(diagonal.shape[0], diagonal.shape[0]), dtype=int)
    #     upper_mat_combine = np.concatenate((left, right), axis=1)
    #     lower_mat_combine = np.concatenate((zeros_pad, diagonal), axis=1)
    #     return np.concatenate((upper_mat_combine, lower_mat_combine))

    @staticmethod
    def combine_schedules(first, second, prec_mat):
        prec_df = pd.read_csv(prec_mat, header=None)
        prec_mat_adj = prec_df.to_numpy()

        combined_adj_mat = PrecSchedule.__concat_matrices(left_mat=first.adj_mat,
                                                          right_mat=prec_mat_adj,
                                                          diag_mat=second.adj_mat)
        combined_fi = first.fi_list + second.fi_list
        combined_pi = first.pi_list + second.pi_list

        combined = PrecSchedule()
        g = Graph(kind='list', directed=True)

        combined.fi_list, combined.pi_list, combined.adj_mat = combined_fi, combined_pi, combined_adj_mat
        combined.graph = combined.__graph_init(g)
        result = combined.__lawler()

        return result

    @staticmethod
    def __concat_matrices(left_mat, diag_mat, right_mat):
        zero_pad = np.zeros(shape=(diag_mat.shape[0], diag_mat.shape[0]), dtype=int)
        upper_mat = np.concatenate((left_mat, right_mat), axis=1)
        lower_mat = np.concatenate((zero_pad, diag_mat), axis=1)
        final_mat = np.concatenate((upper_mat, lower_mat))
        return final_mat

    def __lawler(self):
        graph = deepcopy(self.graph)
        prc_times = self.pi_list.copy()
        p = sum(self.fi_list)
        s = set(self.graph.get_vertices_list())
        sched_res = []
        n = len(s)

        for k in range(n, 0, -1):
            f_k = math.inf
            taken_job = -1
            taken_idx = 0
            # find job j in s such that out deg is 0 and fj(p) is minimal
            for idx, job in enumerate(s):
                # check if out degree is 0
                if graph.vertex_deg(job.key)[1] == 0:
                    if f_k > (self.fi_list[job.key] * p):
                        f_k = self.fi_list[job.key] * p
                        taken_job = job
                        taken_idx = idx

            # update given data
            if taken_job != -1:
                s.remove(taken_job)
                sched_res.append(taken_job)
                p = p - prc_times[taken_idx]
                prc_times.pop(taken_idx)
                graph.remove_vertex(taken_job.key)

        # return the schedule
        return sched_res[::-1]

# def init_csv(data_frame):
#     data_frame_fi = list(map(lambda x: float(x), data_frame.columns.values))
#     data_frame_pi = list(map(lambda x: int(x), data_frame.iloc[0]))
#     data_frame_adj_matrix = data_frame.to_numpy()[1:]
#
#     return data_frame_fi, data_frame_pi, data_frame_adj_matrix
#
#
# def graph_init(graph, mat):
#     mat_graph = defaultdict(dict)
#     for i in range(len(mat)):
#         for j in range(len(mat[0])):
#             if mat[i][j] != 0:
#                 mat_graph[i][j] = mat[i][j]
#
#     for src, neighbors in mat_graph.items():
#         for dst in neighbors.keys():
#             graph.add_edge(src, dst)
#
#     return graph


# def lawler(graph, tasks_funcs, process_time):
#     prc_times = process_time.copy()
#     p = sum(process_time)
#     s = set(graph.get_vertices_list())
#     sched_res = []
#     n = len(s)
#
#     for k in range(n, 0, -1):
#         f_k = math.inf
#         taken_job = -1
#         taken_idx = 0
#         #find job j in s such taht out deg is 0 and fj(p) is minimal
#         for idx, job in enumerate(s):
#             # check if out degree is 0
#             if graph.vertex_deg(job.key)[1] == 0:
#                 if f_k > (tasks_funcs[job.key] * p):
#                     f_k = tasks_funcs[job.key] * p
#                     taken_job = job
#                     taken_idx = idx
#
#         #update given data
#         if taken_job != -1:
#             s.remove(taken_job)
#             sched_res.append(taken_job)
#             p = p - prc_times[taken_idx]
#             prc_times.pop(taken_idx)
#             graph.remove_vertex(taken_job.key)
#
#     #return the schedule
#     return sched_res[::-1]


if __name__ == '__main__':
    g_fry = Graph(kind='list', directed=True)
    fry = PrecSchedule('Data/Fry.csv', g_fry)
    sched_fry = fry.compute_schedule()
    # for x in sched_fry:
    #     print(x.key, end=' ')
    # print()
    # fry.display_graph()

    g_leela = Graph(kind='list', directed=True)
    leela = PrecSchedule('Data/Leela.csv', g_leela)
    sched_leela = leela.compute_schedule()
    # for x in sched_leela:
    #     print(x.key, end=' ')
    # print()
    # leela.display_graph()

    comb = PrecSchedule.combine_schedules(fry, leela, 'Data/Fry_Leela.csv')
    for x in comb:
        print(x.key, end=' ')

    # g_fry = Graph(kind='list', directed=True)
    # fry = PrecSchedule('Fry.csv', g_fry)
    # sched = fry.compute_schedule()
    # for x in sched:
    #     print(x.key, end=' ')
    # print()
    #
    # g_leela = Graph(kind='list', directed=True)
    # leela = PrecSchedule('Fry.csv', g_leela)
    # sched1 = leela.compute_schedule()
    # for x in sched1:
    #     print(x.key, end=' ')
    # print()
    #
    # comb = PrecSchedule.combine_schedules(fry, leela, 'Data/Fry_Leela.csv')
    # for x in comb:
    #     print(x.key, end=' ')
    # print()

    # fry.display_graph()

    # fry = pd.read_csv('Data/Fry.csv')
    # leela = pd.read_csv('Data/Leela.csv')
    # # fry_leela = pd.read_csv('Data/Fry_Leela.csv')
    # fry_fi, fry_pi, fry_adj_matrix = init_csv(fry)
    # fry_fi[-1] = 4
    # leela_fi, leela_pi, leela_adj_matrix = init_csv(leela)
    # fry_leela_fi, fry_leela_pi, fry_leela_adj_matrix = init_csv(fry_leela)

    # g_fry = Graph(kind='list', directed=True)
    # g_leela = Graph(kind='list', directed=True)
    # g_fry = graph_init(g_fry, fry_adj_matrix)
    # g_leela = graph_init(g_leela, leela_adj_matrix)
    #
    # fry_sched = lawler(g_fry, fry_fi, fry_pi)
    # print('result fry')
    # for task in fry_sched:
    #     print(task.key, end=' ')
    # print()
    # leela_sched = lawler(g_leela, leela_fi, leela_pi)
    # print('result leela')
    # for task in leela_sched:
    #     print(task.key, end=' ')