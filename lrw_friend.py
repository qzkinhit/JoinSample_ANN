import numpy as np


def lrw(A, s, l, n, belta=0.1):
    """
    :param A: 关注图的邻接矩阵
    :param s: 要推荐好友的人对应的点编号
    :param belta: 流行度指数
    :param l:随机游走步数
    :param n:推荐人数
    :return:推荐的人的列表
    """
    # 由邻接矩阵得到随机游走转移矩阵M
    a = np.array(A)
    f = [1]  # 预处理阶乘
    E = 0  # 总边数
    for i in range(1, a.shape[0] + 1):
        f.append(f[i - 1] * i)
    M = np.zeros(a.shape)
    for i in range(a.shape[0]):
        du = a[i].sum()
        E += du
        for j in range(a.shape[1]):
            if a[i][j] == 1:
                M[i][j] = 1 / du
            else:
                M[i][j] = 0
    p = np.zeros(a.shape[0])
    p[s - 1] = 1
    lp = [p]
    # 随机游走
    for i in range(l):
        p = np.dot(M.T, p)
        lp.append(p)
    ans = []
    # 按公式计算每个与s不同且不与s直接相邻的点和s的相似度
    for j in range(a.shape[0]):
        if j == s - 1 or a[s - 1][j] == 1:
            continue
        p_sum = 0
        for t in range(2, l + 1):
            p_sum += lp[t][j]
        ans.append(((f[j] / E) ** belta * p_sum, j + 1))
    ans = sorted(ans)[::-1]
    return ans[:n]

"""
adj = [[0, 1, 0, 1, 0, 0], [1, 0, 0, 0, 0, 0], [0, 1, 0, 1, 1, 0], [1, 1, 1, 0, 1, 0], [0, 0, 0, 1, 0, 0],
       [0, 1, 0, 0, 0, 0]]
print(lrw(adj, 6, 3, 2))
"""