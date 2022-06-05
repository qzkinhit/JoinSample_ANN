"""
select s2.destination as id,count(*) as cnt  from
twitter_user as s0 join twitter_user as s1 on s0.destination=s1.source
join twitter_user as s2 on s1.destination=s2.source
group by s2.destination
order by cnt desc
"""
import sqlite3
import numpy as np


def get_sample(db_file, k):
    # k是连接操作次数
    conn = sqlite3.connect(db_file)
    qry = 'select s' + str(k - 1) + '.destination as id,count(*) as cnt from twitter_user as s0 '
    for i in range(1, k):
        qry += 'join twitter_user as s' + str(i) + ' on s' + str(i - 1) + '.destination=s' + str(i) + '.source '
    qry += 'group by s' + str(k - 1) + '.destination order by cnt desc'
    cur = conn.cursor()
    cur.execute(qry)
    result = cur.fetchall()
    conn.commit()
    conn.close()
    return result


def naive_friend(db_file, k, n, likes):
    # n是推荐个数
    tot = get_sample(db_file, k)
    conn = sqlite3.connect(db_file)
    l = []
    cur = conn.cursor()
    for ele in tot:
        qry = 'select * from userLike where source=' + str(ele[0])
        cur.execute(qry)
        result = cur.fetchall()[0]
        a = np.array(result[1:]).astype(float)
        b = np.array(likes)
        l.append((((a - b) * (a - b)).sum(), result[1:], ele[0]))
    conn.commit()
    conn.close()
    l = sorted(l)
    ans = []
    for i in range(min(n, len(l))):
        ans.append((l[i][2], l[i][1]))
    return ans

# print(naive_friend('twitter_data.db', 3, 3, (0.5, 0.5, 0.5, 0.5, 0.5)))
