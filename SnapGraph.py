# -*- coding: utf-8 -*-
"""
@Time ： 2022/5/25 11:25
@Auth ： qianzekai
@stuId:1190202011
@File ：SnapGraph.py
@IDE ：PyCharm
"""
import random
import sqlite3

import snap


def getAttribute(origin_file):
    min_num = float("inf")
    max_num = float("-inf")
    records_num = 0
    with open(origin_file, "r", encoding="utf8") as f:
        for line in f:
            if records_num % 1000 == 0:
                print("handel{}num".format(records_num))
            records_num += 1
            source, des = line.strip().split()
            source = int(source)
            des = int(des)
            max_n = max(source, des)
            min_n = min(source, des)
            if max_n > max_num:
                max_num = max_n
            if min_n < min_num:
                min_num = min_n
    print("record{}，max{}，min{}".format(records_num, max_num, min_num))


def LoadTwitter(twitter_user_file, db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        conn.execute("CREATE TABLE Twitter_user (source, destination)")
        conn.execute("create index Twitter_user_destination_index on Twitter_user(destination)")
        conn.execute("create index Twitter_user_source_index on Twitter_user(source)")
        conn.commit()
    except:
        conn.execute("DROP TABLE Twitter_user;")
        conn.execute("CREATE TABLE Twitter_user (source, destination)")
        conn.execute("create index Twitter_user_destination_index on Twitter_user(destination)")
        conn.execute("create index Twitter_user_source_index on Twitter_user(source)")
        conn.commit()

    conn.execute('PRAGMA synchronous = OFF')
    print("开始插入twitter数据...")
    with open(twitter_user_file, "r", encoding="utf8") as f:
        datas = []
        for num, line in enumerate(f):
            if num % 1000000 == 0:
                print("Twitter数据已插入{}条".format(num))
                s, d = line.strip().split()
                datas.append((int(s), int(d)))
                conn.executemany("INSERT INTO Twitter_user"
                                 "(source, destination) VALUES(?,?)", datas)
                datas.clear()
            else:
                s, d = line.strip().split()
                datas.append((int(s), int(d)))
    if len(datas) > 0:
        conn.executemany("INSERT INTO Twitter_user"
                         "(source, destination) VALUES(?,?)", datas)
        conn.commit()
    f.close()


def LoadUserLike(user_like_file, db_file, k):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    sqlcreate = "CREATE TABLE userLike (source constraint userLike_pk primary key,"
    for i in range(k - 1):
        sqlcreate += "like" + str(i + 1) + ","
    sqlcreate += "like" + str(k) + ")"
    try:
        conn.execute(sqlcreate)
        conn.commit()
    except:
        conn.execute("DROP TABLE userLike;")
        conn.execute(sqlcreate)
        conn.commit()
    conn.execute('PRAGMA synchronous = OFF')
    print("开始插入Like数据...")
    with open(user_like_file, "r", encoding="utf8") as f:
        datas = []
        for num, line in enumerate(f):
            if num % 10000 == 0:
                print("Like数据已插入{}条".format(num))
                a = line.strip().split()
                s = a[0];
                # print(s);
                data = []
                data.append(int(s))
                for i in range(k):
                    data.append(a[i + 1])
                datas.append(data)
                sqlinsert = "INSERT INTO userLike (source,"
                for i in range(k - 1):
                    sqlinsert += "like" + str(i + 1) + ","
                sqlinsert += "like" + str(k) + ")VALUES("
                for i in range(k - 1):
                    sqlinsert += "?,"
                sqlinsert += "?,?)"
                conn.executemany(sqlinsert, datas)
                datas.clear()
            else:
                data = []
                a = line.strip().split()
                s = a[0];
                data.append(int(s))
                for i in range(k):
                    data.append(a[i + 1])
                datas.append(data)

    if len(datas) > 0:
        sqlinsert = "INSERT INTO userLike (source,"
        for i in range(k - 1):
            sqlinsert += "like" + str(i + 1) + ","
        sqlinsert += "like" + str(k) + ")VALUES("
        for i in range(k - 1):
            sqlinsert += "?,"
        sqlinsert += "?,?)"
        conn.executemany(sqlinsert, datas)
    conn.commit()

    f.close()


def CreateUserLike(user_like_file, db_file, k):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    sqlcreate = "CREATE TABLE userLike (source constraint userLike_pk primary key,"
    for i in range(k - 1):
        sqlcreate += "like" + str(i + 1) + ","
    sqlcreate += "like" + str(k) + ")"
    try:
        conn.execute(sqlcreate)
        conn.commit()
    except:
        conn.execute("DROP TABLE userLike;")
        conn.execute(sqlcreate)
        conn.commit()
    conn.execute('PRAGMA synchronous = OFF')
    print("开始插入Like数据...")
    with open(user_like_file, "r", encoding="utf8") as f:
        datas = []
        for num, line in enumerate(f):
            if num % 10000 == 0:
                print("Like数据已插入{}条".format(num))
                s = line.strip().split()
                # print(s);
                data = []
                data.append(int(s[0]))
                for i in range(k):
                    data.append(random.uniform(.5, .6))
                datas.append(data)
                sqlinsert = "INSERT INTO userLike (source,"
                for i in range(k - 1):
                    sqlinsert += "like" + str(i + 1) + ","
                sqlinsert += "like" + str(k) + ")VALUES("
                for i in range(k - 1):
                    sqlinsert += "?,"
                sqlinsert += "?,?)"
                conn.executemany(sqlinsert, datas)
                datas.clear()
            else:
                data = []
                s = line.strip().split()
                data.append(int(s[0]))
                for i in range(k):
                    data.append(random.uniform(.5, .6))
                datas.append(data)

    if len(datas) > 0:
        sqlinsert = "INSERT INTO userLike (source,"
        for i in range(k - 1):
            sqlinsert += "like" + str(i + 1) + ","
        sqlinsert += "like" + str(k) + ")VALUES("
        for i in range(k - 1):
            sqlinsert += "?,"
        sqlinsert += "?,?)"
        conn.executemany(sqlinsert, datas)
    conn.commit()

    f.close()


def getGraph(origin_file, save_file):
    print("begin get graph...")
    f = open(save_file, "w+", encoding="utf8")
    graph = snap.LoadEdgeList(snap.PNGraph, origin_file, 0, 1)  # 构建图
    print("end get graph,get users......")
    for node in graph.Nodes():
        if node.GetInDeg() > 1000:
            # for item in node.GetOutEdges():
            #     f.write(str(node.GetId()) + " " + str(item)+" "+str(node.GetInDeg()) + "\n")
            for item in node.GetInEdges():
                # print(str(node.GetId()))
                f.write(str(item) + " " + str(node.GetId()) + " " + str(node.GetInDeg()) + "\n")
    f.close()
    print("end getGraph")


def creatLikeData(origin_file, db_file, k):
    mu = 0
    sigma = 0.05
    like = [0] * 10
    count = 0;
    conn = sqlite3.connect(db_file)
    print("begin get graph...")
    graph = snap.LoadEdgeList(snap.PNGraph, origin_file, 0, 1)  # 构建图
    print("end get graph,get allusers'like......")
    for node in graph.Nodes():
        count += 1
        print("Total user 77097,has update" + str(count) + ", NowupdateId=" + str(node.GetId()) + ",need update " + str(
            node.GetInDeg()))
        for item in node.GetInEdges():
            p = "select * from userLike where " + str(node.GetId()) + "=""userLike.source"
            # print(p)
            pr = conn.execute(p)
            q = "select * from userLike where " + str(item) + "=""userLike.source"
            qr = conn.execute(q)
            for result1 in pr:
                for result2 in qr:
                    for i in range(k):
                        like[i] = ((result2[i + 1] + result1[i + 1] + random.gauss(mu, sigma)) / 2)
            sqlupdate = "UPDATE userLike set "
            for i in range(k - 1):
                sqlupdate += "like" + str(i + 1) + "=" + str(like[i]) + ","
            sqlupdate += "like" + str(k) + "=" + str(like[k - 1]) + " where source=" + str(item)
            # print(sqlupdate)
            conn.execute(sqlupdate)
            conn.commit()
            # f.write(str(item) + " " + str(node.GetId())+" "+str(node.GetInDeg())  + "\n")

    print("end getGraph")


if __name__ == "__main__":
    LoadTwitter("twitter_combined.txt", "twitter_data.db")
    getGraph("twitter_combined.txt", "popular_user.txt")
    LoadUserLike("user_like.txt", "twitter_data.db", 10);
    # CreateUserLike("user_like.txt", "twitter_data.db",10);
    # creatLikeData("twitter_combined.txt", "twitter_data.db",10)
