'''
@Time    : 2020/4/20 19:25
@Author  : sh_lord
@FileName: UserCFRec.py

'''
import random
import math
import json
import os
from CFConstants.CFConstants import *

class UserCFRec:
    def __init__(self, datafile):
        self.datafile = datafile
        self.data = self.loadData()
        self.trainData, self.testData = self.splitData(100)
        self.user_sim_dict = self.UserSimilarityBest()
        pass

    def loadData(self):
        print("loading data")
        data = []
        with open(self.datafile, 'r') as f_r:
            for line in f_r:
                userid, itemid, record, _timestamp = line.split("::")
                data.append((userid, itemid, int(record)))
        return data

    # 1: 9划分测试机、训练集
    def splitData(self, seed):
        print("划分训练集与测试集")
        train, test = dict(), dict()
        random.seed(seed)
        for user, item, record in self.data:
            if random.random() > 0.9:
                test.setdefault(user, dict())
                test[user][item] = record
            else:
                train.setdefault(user, dict())
                train[user][item] = record
        return train, test

    def UserSimilarityBest(self):
        if os.path.exists(USER_SIM_DICT_PATH):
            print("{} exists, skip".format(USER_SIM_DICT_PATH))
            with open(USER_SIM_DICT_PATH, 'r') as f_r:
                user_sim_dict = json.load(f_r)
            return user_sim_dict

        item_user_dict = dict()
        # 倒排索引
        for userid, itemid, _ in self.data:
            item_user_dict.setdefault(itemid, set())
            item_user_dict[itemid].add(userid)

        # user的共线矩阵
        user_common_cnt = dict()
        # 每个user评价过多少物品
        user_item_cnt_num = dict()
        for itemid in item_user_dict.keys():
            for userid_0 in item_user_dict[itemid]:
                user_common_cnt.setdefault(userid_0, dict())
                user_item_cnt_num[userid_0] = user_item_cnt_num.get(userid_0, 0) + 1
                for userid_1 in item_user_dict[itemid]:
                    if userid_0 == userid_1:
                        continue
                    user_common_cnt[userid_0][userid_1] = user_common_cnt[userid_0].get(userid_1, 0) + 1

        # userSimilar矩阵
        print("构造userSimilar矩阵")
        user_sim_dict = dict()
        for userid_0 in user_common_cnt.keys():
            user_sim_dict.setdefault(userid_0, dict())
            for userid_1, common_cnt in user_common_cnt[userid_0].items():
                user_sim_dict[userid_0].setdefault(userid_1, 0)
                user_sim_dict[userid_0][userid_1] = user_common_cnt[userid_0][userid_1] \
                                                    / math.sqrt(user_item_cnt_num[userid_0] * user_item_cnt_num[userid_1])

        print("save json file: {}".format(USER_SIM_DICT_PATH))
        with open(USER_SIM_DICT_PATH, 'w') as f_w:
            json.dump(user_sim_dict, f_w)

        return user_sim_dict


    """
    k: 选取k个最近邻（相似）用户
    nitems： 推荐nitems个物品
    """
    def recommend(self, userid, k=8, nitems=40):
        print("开始recommend")
        result = dict()
        scored_items = list(item[0] for item in self.trainData[userid].items())
        for u, sim_score in sorted(self.user_sim_dict[userid].items(), key=lambda x: x[1], reverse=True)[:k]:
            for item, score in self.trainData[userid].items():
                if item in scored_items:
                    continue
                result.setdefault(item, 0)
                result[item] = sim_score * score
        return dict(sorted(result.items(), key=lambda x: x[1], reverse=True)[:nitems])

if __name__ == '__main__':
    cf = UserCFRec("../data/ml-1m/ratings.dat")
    result = cf.recommend("1")
    print(result)





