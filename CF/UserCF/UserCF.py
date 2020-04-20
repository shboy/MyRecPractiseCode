'''
@Time    : 2020/4/18 17:34
@Author  : sh_lord
@FileName: UserCF.py

'''
import numpy as np


class UserCF:
    def __init__(self):
        self.user_score_dict = self.initUserScore()
        # self.users_sim = self.calcuUsersSim()
        # self.users_sim = self.calcuUsersSimWithIdx()
        self.users_sim = self.calcuUsersSimWithIdxAndHotPanish()

    # 初始化用户评分数据
    # 这个数据构造的不好，未评分的应该为-1
    def initUserScore(self):
        user_score_dict = {"A": {"a": 3.0, "b": 4.0, "c": 0.0, "d": 3.5, "e": 0.0},
                           "B": {"a": 4.0, "b": 0.0, "c": 4.5, "d": 0.0, "e": 3.5},
                           "C": {"a": 0.0, "b": 3.5, "c": 0.0, "d": 0., "e": 3.0},
                           "D": {"a": 0.0, "b": 4.0, "c": 0.0, "d": 3.50, "e": 3.0}}
        return user_score_dict

    def calcuUsersSim(self):
        users_sim = dict()
        for user_0 in self.user_score_dict.keys():
            user_0_items_set = set(key for key in self.user_score_dict[user_0].keys() if self.user_score_dict[user_0][key] > 0)
            for user_1 in self.user_score_dict.keys():
                if user_0 == user_1:
                    continue
                user_1_items_set = set(key for key in self.user_score_dict[user_1].keys() if self.user_score_dict[user_1][key] > 0)
                nominator = len(user_0_items_set & user_1_items_set)
                denominator = np.sqrt(len(user_0_items_set) * len(user_1_items_set))
                users_sim.setdefault(user_0, dict())[user_1] = nominator / denominator
        return users_sim


    # 带倒排索引的相似度计算
    def calcuUsersSimWithIdx(self):
        # 建立item->users的倒排矩阵
        item_users_dict = dict()
        for user, item in self.user_score_dict.items():
            for item_name, score in item.items():
                if score > 0:
                    item_users_dict.setdefault(item_name, set()).add(user)

        # 计算用户相似度
        user_scored_nums_dict = dict()
        user_common_items_dict = dict()
        for item_name, users in item_users_dict.items():
            for user_0 in users:
                user_scored_nums_dict.setdefault(user_0, 0)
                user_scored_nums_dict[user_0] += 1
                user_common_items_dict.setdefault(user_0, dict())
                for user_1 in users:
                    if user_0 == user_1:
                        continue
                    user_common_items_dict[user_0].setdefault(user_1, 0)
                    user_common_items_dict[user_0][user_1] += 1

        users_sim = dict()
        for user_0, user_item_dict in user_common_items_dict.items():
            users_sim[user_0] = dict()
            for user_1, common_items_num in user_item_dict.items():
                users_sim[user_0].setdefault(user_1, 0)
                users_sim[user_0][user_1] = user_common_items_dict[user_0][user_1] / \
                                            np.sqrt(user_scored_nums_dict[user_0] * user_scored_nums_dict[user_1])
        return users_sim


    def calcuUsersSimWithIdxAndHotPanish(self):
        # 建立item->users的倒排矩阵
        item_users_dict = dict()
        for user, item in self.user_score_dict.items():
            for item_name, score in item.items():
                if score > 0:
                    item_users_dict.setdefault(item_name, set()).add(user)

        # 计算用户相似度
        user_scored_nums_dict = dict()
        user_common_items_dict = dict()
        for item_name, users in item_users_dict.items():
            for user_0 in users:
                user_scored_nums_dict.setdefault(user_0, 0)
                user_scored_nums_dict[user_0] += 1
                user_common_items_dict.setdefault(user_0, dict())
                for user_1 in users:
                    if user_0 == user_1:
                        continue
                    user_common_items_dict[user_0].setdefault(user_1, 0)
                    user_common_items_dict[user_0][user_1] += 1 / np.log(1+len(item_users_dict[item_name]))

        users_sim = dict()
        for user_0, user_item_dict in user_common_items_dict.items():
            users_sim[user_0] = dict()
            for user_1, common_items_num in user_item_dict.items():
                users_sim[user_0].setdefault(user_1, 0)
                users_sim[user_0][user_1] = user_common_items_dict[user_0][user_1] / \
                                            np.sqrt(user_scored_nums_dict[user_0] * user_scored_nums_dict[user_1])
        return users_sim


    def recommend(self, user_name):
        items_not_scored = set(key for key in self.user_score_dict[user_name].keys() if self.user_score_dict[user_name][key] <=0)
        item_score_dict = dict()
        for item in items_not_scored:
            cur_item_score = 0
            for u, score in self.users_sim[user_name].items():
                cur_item_score += score * self.user_score_dict[u][item]
            item_score_dict[item] = cur_item_score
        print(sorted(item_score_dict.items(), key=lambda _: _[0]))

if __name__ == '__main__':
    ucf = UserCF()
    ucf.recommend("C")

