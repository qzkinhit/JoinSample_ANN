# -*- coding: utf-8 -*-
"""
@Time ： 2022/5/29 16:19
@Auth ： qianzekai
@stuId:1190202011
@File ：main.py
@IDE ：PyCharm
"""

# -*- coding: utf-8 -*-

import random

from EW import ExactWeightJoinSample


def getMethodCompare(query):
    b = []
    EW = ExactWeightJoinSample("twitter_data.db", False, 5)
    SampleNum = 20#111
    print("begin ExactWeightSampling")
    _, S, m = EW.RandomSample(SampleNum, query)
    for i in range(5):
        b.append(random.uniform(0.5, 0.7))
    a = m.knn(b, 3)
    print("find 3 kind of object which is similar to {0}:{1}".format(b, a))
    print("end ExactWeightSampling")


if __name__ == "__main__":
    # getMethodCompare(["Popular_user", "Twitter_user"])
    getMethodCompare(["Twitter_user", "Twitter_user", "Twitter_user", "Twitter_user"])
    # getMethodCompare(["Popular_user", "Twitter_user", "Popular_user", "Twitter_user", "Popular_user"])
