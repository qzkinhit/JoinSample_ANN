# -*- coding: utf-8 -*-
"""
@Time ： 2022/5/25 11:25
@Auth ： qianzekai
@stuId:1190202011
@File ：EW.py
@IDE ：PyCharm
"""
import copy
import random
import time

import numpy as np

import nearoptimal
from RandomSample import JoinSample


##ExactWeightSampling
class ExactWeightJoinSample(JoinSample):
    def __init__(self, db_file, needCreatData, k):
        super(ExactWeightJoinSample, self).__init__(db_file, needCreatData, k)
        self.W = None
        self.k = k

    def ExactWeight(self, join_order):
        print("开始计算W值...")
        W = []  # 初始化
        for i in range(len(join_order) - 1, -1, -1):  # 从后向前遍历
            # print(str(join_order)+"\n")
            W_set = {}
            if i == len(join_order) - 1:
                ts = self.conn.execute("SELECT source, destination FROM " + join_order[i])
                for result in ts:
                    # print(result)
                    W_set[result] = random.uniform(0, 100)  # 初始化权重,通过随机数模拟这个用户的活跃程度，活跃程度越大，价值越高
                W.append(W_set)
            else:
                next_set = W[0]
                ts = self.conn.execute("SELECT source, destination FROM " + join_order[i])
                ds = self.conn.execute("SELECT DISTINCT destination FROM " + join_order[i])
                s_set = {}
                for result in ds:
                    p = "select " + join_order[i + 1] + ".source, " + join_order[i + 1] + ".destination" + " from " + \
                        join_order[i + 1] + \
                        " where " + str(result[0]) + "=" + join_order[i + 1] + ".source"
                    path_tuples = self.conn.execute(p)
                    m = 0
                    for t in path_tuples:
                        m += next_set[t]
                    s_set[result[0]] = m
                for result in ts:
                    W_set[result] = s_set[result[1]]
                W = [W_set] + W
        m = sum(W[0].values())
        W = [{self.r0: m}] + W
        self.W = W
        return W

    def RandomSample(self, sample_num, join_order):
        dim1 = self.k  # To make some nice sidelengths, we cheat on omega
        # omega = 5 / sqrt(sqrt(dim))
        m = nearoptimal.MultiDimHash(dim=dim1)
        Sample = []
        begin = 0
        end = 0
        if self.W is None:
            begin = time.process_time()
            W = self.ExactWeight(join_order)
            end = time.process_time()  ##模拟数据量大的情况
        else:
            W = copy.deepcopy(self.W)
        print("开始进行sample的计算...")
        i = 0
        while i < sample_num:
            S = self.ChainRandomJoinSampling(join_order, W)
            if S is not None:
                i += 1
                a = np.array(S[1:self.k + 1]).astype(np.float)
                m.insert(a, str(S[0]))
        return end - begin, S, m


if __name__ == "__main__":
    a = ExactWeightJoinSample("twitter_data.db")
    s = a.RandomSample(10, ["Popular_user", "Twitter_user", "Twitter_user"])
    print(s)
