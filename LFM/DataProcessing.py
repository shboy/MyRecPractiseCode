'''
@Time    : 2020/4/24 12:18
@Author  : sh_lord
@FileName: DataProcessing.py

'''
import pandas as pd
import pickle
from Constants import *


class DataProcessing:
    def __init__(self):
        # 'userID', 'Gender', 'Age', 'Occupation', 'Zip-code'
        self.user_data = pd.read_csv(USER_DATA_CSV_PATH)
        # 'MovieID', 'Title', 'Genres'
        self.item_data = pd.read_csv(ITEM_DATA_CSV_PATH)
        # 'UserID', 'MovieID', 'Rating', 'Timestamp'
        self.rate_data = pd.read_csv(RATE_DATA_CSV_PATH)

    def genLFMData(self):
        user_item_label = dict()
        items = set(self.item_data['MovieID'].values)
        for userid in set(self.user_data["UserID"].values):
            user_item_label.setdefault(userid, dict())
            scored_items = set(self.rate_data[self.rate_data['UserID'] == userid]['MovieID'].values)
            unscored_items = list(items.difference(scored_items))[:len(scored_items)]
            for itemid in scored_items: user_item_label[userid][itemid] = 1
            for itemid in unscored_items: user_item_label[userid][itemid] = 0
        with open(USER_ITEM_LABEL_PATH, 'wb') as f_w:
            pickle.dump(user_item_label, f_w)


if __name__ == '__main__':
    dp = DataProcessing()
    dp.genLFMData()
