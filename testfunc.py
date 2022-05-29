# -*- coding: utf-8 -*-
"""
@Time ： 2022/5/28 17:48
@Auth ： qianzekai
@stuId:1190202011
@File ：testfunc.py
@IDE ：PyCharm
"""
import numpy as np


def epsilonCheck(x, epsilon=1e-6):
    """Checks that x is in (-epsilon, epsilon)."""
    epsilon = abs(epsilon)
    return -epsilon < x < epsilon


def checkARandomSort(m, n):
    # print(m)
    # print(n)
    a = np.sort(list(m))
    b = np.sort(list(n))

    if (a == b).all():
        return True
    else:
        return False
