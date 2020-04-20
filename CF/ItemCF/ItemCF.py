'''
@Time    : 2020/4/18 20:06
@Author  : sh_lord
@FileName: ItemCF.py

'''
import math

class ItemCF:
    def __init__(self):
        self.user_score_dict = self.initUserScore()
        # self.item_sim_dict = self.itemSimilarity()
        self.item_sim_dict = self.itemSimilarityWithHotPanish()


    # 初始化用户评分数据
    def initUserScore(self):
        user_score_dict = {
            "A": {"a": 3.0, "b": 4.0, "c": 0.0, "d": 3.5, "e": 0.0},
            "B": {"a": 4.0, "b": 0.0, "c": 4.5, "d": 0.0, "e": 3.5},
            "C": {"a": 0.0, "b": 3.5, "c": 0.0, "d": 0.0, "e": 3.0},
            "D": {"a": 0.0, "b": 4.0, "c": 0.0, "d": 3.5, "e": 3.0},
        }
        return user_score_dict

    def itemSimilarity(self):
        # 建立user->item 倒排索引
        user_items_dict = dict()
        for user, item_score_dict in self.user_score_dict.items():
            for item, score in item_score_dict.items():
                if score > 0:
                    user_items_dict.setdefault(user, set()).add(item)

        # 构建共现矩阵
        count = dict()
        item_users_count_dict = dict()
        for user, items in user_items_dict.items():
            for item_0 in items:
                count.setdefault(item_0, dict())
                if self.user_score_dict[user][item_0] > 0:
                    item_users_count_dict.setdefault(item_0, 0)
                    item_users_count_dict[item_0] += 1
                for item_1 in items:
                    if (item_0 == item_1
                            and self.user_score_dict[user][item_0] > 0
                            and self.user_score_dict[user][item_1] > 0):
                        continue
                    count[item_0].setdefault(item_1, 0)
                    count[item_0][item_1] += 1

        # 计算item之间的相似度矩阵
        item_sim_dict = dict()
        for item_0, item_common_cnt in count.items():
            for item_1, common_cnt in item_common_cnt.items():
                if item_0 == item_1:
                    continue
                nominator = count[item_0][item_1]
                denominator = item_users_count_dict[item_0]
                item_sim_dict.setdefault(item_0, dict())
                item_sim_dict[item_0][item_1] = nominator/denominator
        return item_sim_dict

    def itemSimilarityWithHotPanish(self):
        # 建立user->item 倒排索引
        user_items_dict = dict()
        for user, item_score_dict in self.user_score_dict.items():
            for item, score in item_score_dict.items():
                if score > 0:
                    user_items_dict.setdefault(user, set()).add(item)

        # 构建共现矩阵
        count = dict()
        item_users_count_dict = dict()
        for user, items in user_items_dict.items():
            for item_0 in items:
                count.setdefault(item_0, dict())
                if self.user_score_dict[user][item_0] > 0:
                    item_users_count_dict.setdefault(item_0, 0)
                    item_users_count_dict[item_0] += 1
                for item_1 in items:
                    if (item_0 == item_1
                            and self.user_score_dict[user][item_0] > 0
                            and self.user_score_dict[user][item_1] > 0):
                        continue
                    count[item_0].setdefault(item_1, 0)
                    count[item_0][item_1] += 1

        # 计算item之间的相似度矩阵
        item_sim_dict = dict()
        for item_0, item_common_cnt in count.items():
            for item_1, common_cnt in item_common_cnt.items():
                if item_0 == item_1:
                    continue
                nominator = count[item_0][item_1]
                denominator = math.sqrt(item_users_count_dict[item_0] * item_users_count_dict[item_1])
                item_sim_dict.setdefault(item_0, dict())
                item_sim_dict[item_0][item_1] = nominator/denominator
        return item_sim_dict


    def predictUserItemScore(self, user_name, item_name):
        user_predict_score = 0
        for item, sim_score in self.item_sim_dict[item_name].items():
            if item != item_name:
                user_item_score = self.user_score_dict[user_name][item]
                item_similarity = sim_score
                user_predict_score += user_item_score * item_similarity
        return user_predict_score


    def recommend(self, user_name):
        user_item_predict_score_dict = dict()
        for item_name, score in self.user_score_dict[user_name].items():
            if score <= 0:
                user_item_predict_score_dict[item_name] = self.predictUserItemScore(user_name, item_name)
        print(sorted(user_item_predict_score_dict.items(), key=lambda x: x[1], reverse=True))

if __name__ == '__main__':
    itemCf = ItemCF()
    itemCf.recommend("C")
