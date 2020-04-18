'''
@Time    : 2020/4/14 12:31
@Author  : sh_lord
@FileName: test.py

'''
from Constants.Constants import *
import numpy as np
import pandas as pd

class Test:
    def test01(self):
        user_rate_score_data = pd.read_csv(RATE_DATA_CSV_PATH, sep=",")
        var = user_rate_score_data[user_rate_score_data['UserID'] == 2]
        pass

    def test02(self):
        user_rate_score_data = pd.read_csv(RATE_DATA_CSV_PATH, sep=",")
        var = user_rate_score_data['UserID']
        pass

    def test03(self):
        user_rate_score_data = pd.read_csv(RATE_DATA_CSV_PATH, sep=",")
        user_score_list = user_rate_score_data[user_rate_score_data['UserID'] == 1]['Rating'].values
        user_avg_score = sum(user_score_list) / len(user_score_list)
        user_score = user_rate_score_data[user_rate_score_data['UserID'] == 1][
            user_rate_score_data['MovieID'] == 661]['Rating'].values
        pass

if __name__ == '__main__':
    test = Test()
    test.test02()


