# JoinSample_ANN
## 简介

* 一种基于JoinSample 和ANN的推荐算法实现的关注列表推荐应用

## start

* python main.py

## 参考复现的文献

* Zhao Z , Christensen R , Li F , et al. Random Sampling over Joins Revisited[C]// 2018:1525-1539.
* Andoni A , Indyk P . Near-Optimal Hashing Algorithms for Approximate Nearest Neighbor in High Dimensions[C]// 47th
  Annual IEEE Symposium on Foundations of Computer Science (FOCS 2006), 21-24 October 2006, Berkeley, California, USA,
  Proceedings. IEEE, 2006.

## 文件结构

* ANNtest.py 测试ANN算法的可行性
* EW.py sample join的动态规划算法
* JoinSampleTest.py 测试sampleJoin的可行性
* log.txt输出日志
* main.py 优化算法运行demo
* naive.py 朴素算法的demo
* minhash 普通的minhash算法
* nearoptimal 优化后的lsh 解决ann算法
* RandomSample.py 抽样算法
* SnapGraph.py 数据集的预处理
* test_xxx.py 相关函数的测试脚本
* user_like.txt twitter_combined.txt 数据集
* lrw_friend.py lrw-friend算法的实现

## 数据库

* 使用sqllit3 
