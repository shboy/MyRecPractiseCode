'''
@Time    : 2020/4/14 10:21
@Author  : sh_lord
@FileName: GenerateProfile.py

'''
import pandas as pd
import numpy as np
import json
import os
from Constants.Constants import *

class GenerateProfile:
    def __init__(self):
        # self.mId_list = []  # 已去重
        # self.all_genres_list = []
        # self.item_geners_one_hot = self.prepare_item_profile()
        # self.item_geners_dict movieId->genres_list
        pass

    # 每个movieId->类型的one-hot向量
    # ['MovieID', 'Title', 'Genres']
    def prepare_item_profile(self):
        item_data = pd.read_csv(ITEM_DATA_CSV_PATH, sep=",")
        mId_set = set(item_data['MovieID'].values)
        self.mId_list = sorted(list(mId_set))
        mId_len = len(self.mId_list)
        all_genres_list = []
        item_geners_dict = dict()
        for mId in mId_set:
            genres = item_data[item_data['MovieID'] == mId]['Genres'].values[0].split('|')
            all_genres_list.extend(genres)
            # key 为 int，没法dump json
            item_geners_dict.setdefault(str(mId), []).extend(genres)
        self.item_geners_dict = item_geners_dict
        self.all_genres_list = all_genres_list = sorted(list(set(all_genres_list)))
        item_geners_one_hot = dict()
        for mId, geners_list in item_geners_dict.items():
            item_geners_one_hot.setdefault(mId, np.zeros(len(all_genres_list), dtype=np.int).tolist())
            for gener in geners_list:
                item_geners_one_hot[mId][all_genres_list.index(gener)] = 1
        self.item_geners_one_hot = item_geners_one_hot

        if os.path.exists(ITEM_PROFILE_JSON_PATH):
            print("item profile json exists")
            return item_geners_one_hot
        print("start to write item profile json")
        with open(ITEM_PROFILE_JSON_PATH, 'w') as f_w:
            json.dump(item_geners_one_hot, f_w)
        print("item profile json wrote down")

        return item_geners_one_hot

    # 输出用户对每一种类型的喜爱打分
    # ['UserID', 'MovieID', 'Rating', 'Timestamp']
    def prepare_user_rate_score_profile(self):
        if os.path.exists(USER_RATE_SCORE_PROFILE_JSON_PATH):
            print(USER_RATE_SCORE_PROFILE_JSON_PATH + " exists")
            return

        user_mId_score_dict = dict()
        if os.path.exists(USER_MOVIE_ID_SCORE_DICT_JSON_PATH):
            print(USER_MOVIE_ID_SCORE_DICT_JSON_PATH + " exists")
            with open(USER_MOVIE_ID_SCORE_DICT_JSON_PATH, 'r') as f_r:
                user_mId_score_dict = json.load(f_r)
        else:
            user_rate_score_data = pd.read_csv(RATE_DATA_CSV_PATH, sep=",")

            # 先生成 userid -> movieid -> rate 二级map
            for row_number in user_rate_score_data.index:
                print("row number: {}, all: {}".format(row_number, user_rate_score_data.shape[0]))

                row_data = user_rate_score_data.iloc[row_number]
                userId = str(row_data['UserID'])
                movieId = str(row_data['MovieID'])
                # int64类型 没法dump json， 转成普通int
                rating = int(row_data['Rating'])
                user_mId_score_dict.setdefault(userId, {})[movieId] = rating

            with open(USER_MOVIE_ID_SCORE_DICT_JSON_PATH, 'w') as f_w:
                json.dump(user_mId_score_dict, f_w)

        # userid -> 每种类型电影的平均打分（中心化了）
        user_rate_degree_profile = dict()
        for cnt, user_id in enumerate(user_mId_score_dict.keys()):
            user_id = str(user_id)
            print("cnt: {}, user_id: {}".format(cnt, user_id))
            # user_score_values = user_rate_score_data[user_rate_score_data['UserID'] == user_id]['Rating'].values
            user_score_values = user_mId_score_dict[user_id].values()
            user_avg_score = sum(user_score_values) / len(user_score_values)
            score = 0; score_len = 0
            for genre in self.all_genres_list:
                # for movie_id in user_rate_score_data[user_rate_score_data['UserID'] == user_id]['MovieID'].values:
                for movie_id in user_mId_score_dict[user_id].keys():
                    # 用户对movieId的打分
                    # 这种对df结构索引的方法太慢，每次都要遍历整个数据集
                    # user_score = user_rate_score_data[(user_rate_score_data['UserID'] == user_id) &
                    #                                   (user_rate_score_data['MovieID'] == movie_id)]['Rating'].values * 1.0
                    user_score = user_mId_score_dict[user_id][movie_id] * 1.0
                    user_score -= user_avg_score
                    cur_movie_genre_list = self.item_geners_dict[movie_id]
                    if genre in cur_movie_genre_list:
                        score += user_score
                        score_len += 1
                if score_len == 0:
                    genre_avg_score = 0.0
                else:
                    genre_avg_score = score / score_len
                user_rate_degree_profile.setdefault(user_id, []).append(genre_avg_score)

        print("start to write user rate score profile json")
        with open(USER_RATE_SCORE_PROFILE_JSON_PATH, 'w') as f_w:
            json.dump(user_rate_degree_profile, f_w)
        print("user rate score profile json wrote down")

if __name__ == '__main__':
    genProfile = GenerateProfile()
    genProfile.prepare_item_profile()
    genProfile.prepare_user_rate_score_profile()
