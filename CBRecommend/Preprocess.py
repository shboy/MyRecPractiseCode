'''
@Time    : 2020/4/11 21:35
@Author  : sh_lord
@FileName: Preprocess.py

'''
import pandas as pd
import json
import os
from Constants.Constants import *

class Preprocess:
    def __init__(self):
        print("start to process user data")
        self.process_user_data()
        print("start to process item data")
        self.process_item_data()
        print("start to process rate data")
        self.process_rate_data()
        print("preprocess finished")

    def process_user_data(self):
        if os.path.exists(USER_DATA_CSV_PATH):
            print("user_data.csv exists")
            return
        user_data = pd.read_table("../data/ml-1m/users.dat", sep="::", engine="python",
                                  names=['UserID', 'Gender', 'Age', 'Occupation', 'Zip-code'])
        user_data.to_csv(USER_DATA_CSV_PATH, index=False)

    def process_item_data(self):
        if os.path.exists(ITEM_DATA_CSV_PATH):
            print("item_data.csv exists")
            return
        item_data = pd.read_table("../data/ml-1m/movies.dat", sep="::", engine="python",
                                  names=['MovieID', 'Title', 'Genres'])
        item_data.to_csv(ITEM_DATA_CSV_PATH, index=False)

    def process_rate_data(self):
        if os.path.exists(RATE_DATA_CSV_PATH):
            print("rate_data.csv exists")
            return
        rate_data = pd.read_table("../data/ml-1m/ratings.dat", sep="::", engine="python",
                                  names=['UserID', 'MovieID', 'Rating', 'Timestamp'])
        rate_data.to_csv(RATE_DATA_CSV_PATH, index=False)

if __name__ == '__main__':
    preprocess = Preprocess()

