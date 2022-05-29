import random
from math import sqrt

import numpy as np

import nearoptimal


def knnfunc():
    dim = 2  # To make some nice sidelengths, we cheat on omega
    omega = 5 / sqrt(sqrt(dim))
    m = nearoptimal.MultiDimHash(dim=2)
    m.insert(np.array([0.9585762, 1.15822724]), 'test1')
    m.insert(np.array([1.02331605, 0.95385982]), 'test2')
    m.insert(np.array([0.80838576, 1.07507294]), 'test3')
    print("begin insert")
    for i in range(10000):
        if i % 1000 == 1:
            print("finish {} insert".format(i))
        m.insert(np.array([random.uniform(0, 2), random.uniform(0, 2)]), i)
    print("end insert")
    for i in range(100):
        b = np.array([random.uniform(0, 2), random.uniform(0, 2)])
        a = m.knn(b, 5)
        print("find 5 kind of object which is similar to {0}:{1}".format(a, b))


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    knnfunc()
