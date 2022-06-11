# -*- coding: utf-8 -*-
"""
@Time ： 2022/5/25 11:25
@Auth ： qianzekai
@stuId:1190202011
@File ：JoinSampleTest.py
@IDE ：PyCharm
"""
import time

from EW import ExactWeightJoinSample


def getMethodCompare(query):
    EW = ExactWeightJoinSample("small_data.db", False, 5)
    SampleSet = [1, 10, 100, 200]
    times = []  # 抽样运行时间

    for i, SampleNum in enumerate(SampleSet):
        print("begin ExactWeightSampling")
        begin = time.process_time()
        wt = EW.RandomSample(SampleNum, query)
        end = time.process_time()
        print("end ExactWeightSampling")
        if i == 0:
            wtime = wt  # 找权重准备的时间
            times.append(end - begin - wt)
        else:
            times.append(end - begin)
        print(times)


if __name__ == "__main__":
    getMethodCompare(["Twitter_user", "Twitter_user", "Twitter_user"])
    # getMethodCompare(["Popular_user", "Twitter_user", "Popular_user", "Twitter_user", "Popular_user"])
