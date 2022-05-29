# -*- coding: utf-8 -*-
"""
@Time ： 2022/5/25 11:25
@Auth ： qianzekai
@stuId:1190202011
@File ：RandomSample.py
@IDE ：PyCharm
"""
import os
import sqlite3

import numpy as np

import SnapGraph

ALLJOIN = -1
threshold = 0.5


class JoinSample:
    def __init__(self, db_file, needCreatData, k):
        self.r0 = (ALLJOIN, ALLJOIN)
        if os.path.exists(db_file) and needCreatData == False:
            self.conn = sqlite3.connect(db_file)
            self.cursor = self.conn.cursor()
        elif not (os.path.exists(db_file)) and needCreatData == False:
            self.conn = sqlite3.connect(db_file)
            self.cursor = self.conn.cursor()
            SnapGraph.LoadTwitter("twitter_combined.txt", db_file)
            SnapGraph.getGraph("twitter_combined.txt", "popular_user.txt")
            SnapGraph.LoadUserLike("user_like.txt", db_file, k);
        else:
            self.conn = sqlite3.connect(db_file)
            self.cursor = self.conn.cursor()
            SnapGraph.LoadTwitter("twitter_combined.txt", db_file)
            SnapGraph.getGraph("twitter_combined.txt", "popular_user.txt")
            SnapGraph.CreateUserLike("user_like.txt", db_file, k);
            SnapGraph.creatLikeData("twitter_combined.txt", db_file, k);

    # def CreateDatabase(self, user_like_file, twitter_user_file):
    #     self.conn.execute("CREATE TABLE Twitter_user (source, destination, count)")
    #     self.conn.commit()
    #     self.conn.execute('PRAGMA synchronous = OFF')
    #     print("开始插入twitter数据...")
    #     with open(twitter_user_file, "r", encoding="utf8") as f:
    #         datas = []
    #         for num, line in enumerate(f):
    #             if num % 1000000 == 0:
    #                 print("Twitter数据已插入{}条".format(num))
    #                 s, d = line.strip().split()
    #                 datas.append((int(s), int(d), 1))
    #                 self.conn.executemany("INSERT INTO Twitter_user"
    #                                       "(source, destination, count) VALUES(?,?,?)", datas)
    #                 datas.clear()
    #             else:
    #                 s, d = line.strip().split()
    #                 datas.append((int(s), int(d), 1))
    #     if len(datas) > 0:
    #         self.conn.executemany("INSERT INTO Twitter_user"
    #                               "(source, destination, count) VALUES(?,?,?)", datas)
    #     self.conn.commit()

    def ChainRandomJoinSampling(self, join_order, W):
        # print(W)
        t = self.r0
        # print(t);
        # S = []
        for i in range(len(join_order)):
            # print(i,t);
            wt = W[i][t]

            if i == 0:
                # 从第一个表中先随便选一个
                p = "select " + join_order[i] + ".source, " + join_order[i] + ".destination" + " from " + join_order[i]
                tRi = self.conn.execute(p)
                tRI = self.conn.execute(p)
                WtRi = 0
                for result in tRi:  # 后续表中选中的元组之和就是这个元组的权重
                    WtRi += W[i + 1][result]
            else:
                p = "select " + join_order[i] + ".source, " + join_order[i] + ".destination" + " from " + join_order[
                    i] + \
                    " where " + str(t[1]) + "=" + join_order[i] + ".source"
                tRi = self.conn.execute(p)
                tRI = self.conn.execute(p)
                WtRi = 0
                for result in tRi:
                    # print(result)
                    # print(W[i+1][result])
                    WtRi += W[i + 1][result]

            W[i][t] = WtRi  # 权重的准确值
            if (wt != 0):
                reject_prob = 1 - WtRi / wt  # 准确值除以上界是接受率，1-接受率是拒绝率
            else:
                reject_prob = 0;
                # print(wt)
            if np.random.rand() <= min(reject_prob, threshold):  # 被拒绝了
                return None

            num = np.random.rand()
            p = 0.
            sample = None
            for result in tRI:
                # if(WtRi!=0):
                p += W[i + 1][result] / WtRi  # 一直加到大于num为止，就选择它
                # else:
                #     p=0;

                if num < p:
                    sample = result
                    t = result
                    break
                # if p==0:
                #     sample = result
                #     t = result
                #     break;
            if sample is not None and i == len(join_order) - 1:
                p = "select * from userLike where " + str(sample[1]) + "=""userLike.source"
                tRi = self.conn.execute(p)
                for result in tRi:
                    print(result);
                    return result


if __name__ == "__main__":
    s = JoinSample("twitter_data.db", "user_like.txt", "twitter_combined.txt")
    # s.ChainRandomJoinSampling(["Popular_user", "Twitter_user"], 1)
