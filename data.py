import matplotlib.pyplot as plt
import random

if __name__ == '__main__':
    n = 5000  # 人数
    m = 4 * n  # 总关注数
    left = int(m * 0.005)
    right = int(m * 0.02)
    k = int(n / 200)
    lst = []
    B = []
    cur = 0
    for i in range(k):
        u = 0
        while (True):
            u = random.randint(1, n)
            if (u not in B):
                B.append(u)
                break
        deg = random.randint(left, right)
        while (deg > 0):
            v = random.randint(1, n)
            if (u == v or [v, u] in lst):
                continue
            deg -= 1
            cur += 1
            lst.append([v, u])
    for i in range(cur, m):
        while (True):
            u = random.randint(1, n)
            v = random.randint(1, n)
            if (u == v or [v, u] in lst):
                continue
            else:
                lst.append([v, u])
                break
    output = 'smalldata.txt'
    with open(output, 'w', encoding='utf-8') as file1:
        for i in range(m):
            print(lst[i][0], ' ', lst[i][1], file=file1)
    deg = [0 for i in range(n + 1)]
    zx = 0
    for i in range(m):
        deg[lst[i][1]] += 1
    tot = [0 for i in range(n + 1)]
    for i in range(1, n + 1):
        tot[deg[i]] += 1
    X = []
    Y = []
    for i in range(n + 1):
        if (tot[i] != 0):
            print(i, tot[i])
            plt.scatter(i, tot[i])
            X.append(i)
            Y.append(tot[i])
    plt.plot(X, Y)
    plt.show()
