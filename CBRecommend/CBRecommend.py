'''
@Time    : 2020/4/11 19:40
@Author  : sh_lord
@FileName: CBRecommend.py

'''
import pandas as pd
import numpy as np
import json
import os
from Constants.Constants import *

class CBRecommend:
    def __init__(self, K: int=None):
        with open(ITEM_PROFILE_JSON_PATH, 'r') as f_1, open(USER_RATE_SCORE_PROFILE_JSON_PATH, 'r') as f_2:
            self.item_profile = json.load(f_1)
            self.user_profile = json.load(f_2)
        self.K = K
        pass

    def find_no_score(self, user_id):
        # ['MovieID', 'Title', 'Genres']
        all_movie_id = set(pd.read_csv(ITEM_DATA_CSV_PATH, sep=",")['MovieID'].values)
        # ['UserID', 'MovieID', 'Rating', 'Timestamp']
        item_data = pd.read_csv(RATE_DATA_CSV_PATH, sep=",")
        scored_movie_id = set(item_data[item_data['UserID'] == user_id].values)
        unscored_movie_id = all_movie_id - scored_movie_id
        return unscored_movie_id

    def calcu_cosine_distance(self, user_id, movie_id):
        user_id = str(user_id)
        movie_id = str(movie_id)
        numerator = sum(np.array(self.user_profile[user_id]) * np.array(self.item_profile[movie_id]))
        denumerator = np.sqrt(sum(np.square(np.array(self.user_profile[user_id])))) + \
            np.sqrt(sum(np.square(np.array(self.item_profile[movie_id]))))
        return numerator/denumerator


    def recommend(self, user_id):
        unscored_movie_id: set = self.find_no_score(str(user_id))
        mid_score_pair = list(map(lambda mId: (mId, self.calcu_cosine_distance(user_id, mId)), unscored_movie_id))
        if self.K is None:
            mid_score_pair = sorted(mid_score_pair, key=lambda p: p[1], reverse=True)
        else:
            mid_score_pair = sorted(mid_score_pair, key=lambda p: p[1], reverse=True)[:self.K]
        return mid_score_pair

if __name__ == '__main__':
    cbRec = CBRecommend(K=10)
    score_pair = cbRec.recommend(1)
    print(score_pair)
    pass


