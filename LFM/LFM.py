'''
@Time    : 2020/4/24 13:01
@Author  : sh_lord
@FileName: LFM.py

'''
import numpy as np
import pandas as pd
import pickle
import math
import random

from Constants import *


class LFM:
    def __init__(self, K=4, lr=0.01, l2_panish=0.02, epochs=100):
        self.user_data = pd.read_csv(USER_DATA_CSV_PATH)
        # 'MovieID', 'Title', 'Genres'
        self.item_data = pd.read_csv(ITEM_DATA_CSV_PATH)
        # 'UserID', 'MovieID', 'Rating', 'Timestamp'
        self.user_item_rate_data = pd.read_csv(RATE_DATA_CSV_PATH)

        with open(USER_ITEM_LABEL_PATH, 'rb') as f_r:
            self.user_item_label = pickle.load(f_r)

        self.lr = lr
        self.lam = l2_panish
        self.epochs = epochs

        self._init_model(K)


    def _init_model(self, K):
        # 以0为均值、以1为标准差的正态分布，记为N（0，1）
        self.userids = set(self.user_item_rate_data['UserID'].values)
        self.itemids = set(self.user_item_rate_data['MovieID'].values)
        array_p = np.random.randn(len(self.userids), K)
        array_q = np.random.randn(len(self.itemids), K)
        self.p = pd.DataFrame(data=array_p, index=list(self.userids), columns=range(0, K))
        self.q = pd.DataFrame(data=array_q, index=list(self.itemids), columns=range(0, K))


    # 用户i对用户j的喜爱程度
    def _predict(self, userid, itemid):
        ui = np.mat(self.p.loc[userid])
        itemj = np.mat(self.q.loc[itemid])
        mul_val = np.sum(ui.dot(itemj.T))
        logit = 1 / (1 + math.exp(mul_val))
        return logit


    def _loss(self, userid, itemid, y, step):
        e = y - self._predict(userid, itemid)
        return e


    # 梯度回归 这里是随机下降， 每次只有一个样本
    def _optimize(self, userid, itemid, e):
        gradient_p = -e * self.q[itemid].values
        l2_p = self.lam * self.p[userid].values
        gradient_q = -e * self.p[userid].values
        l2_q = self.lam * self.q[itemid].values

        dp = gradient_p + l2_p
        dq = gradient_q + l2_q

        self.p[userid] -= self.lr * dp
        self.q[itemid] -= self.lr * dq


    def save(self):
        with open(MODEL_PATH, "wb") as f_w:
            pickle.dump((self.p, self.q), f_w)


    def load(self):
        with open(MODEL_PATH, "rb") as f_r:
            self.p, self.q = pickle.load(f_r)


    def train(self):
        for epoch in range(self.epochs):
            for userid, itemid_label_dict in self.user_item_label.items():
                itemid_list = random.shuffle(itemid_label_dict.keys())
                for itemid in itemid_list:
                    label = itemid_label_dict[itemid]
                    e = self._loss(userid, itemid, label, epoch)
                    self._optimize(userid, itemid, e)
            self.lr *= 0.9
        self.save()


    def evaluate(self):
        self.load()
        users = random.sample(self.userids, 10)
        user_dict=dict()
        for user in users:
            user_item_ids = set(self.user_item_rate_data[self.user_item_rate_data['UserID'] == user]['MovieID'])
            _sum=0.0
            for itemid in user_item_ids:
                p = np.mat(self.p.loc[user].values)
                q = np.mat(self.q.loc[itemid].values).T
                _r = sum(p.dot(q))
                r = self.user_item_rate_data[(self.user_item_rate_data['UserID'] == user)
                                             & (self.user_item_rate_data['MovieID'] == itemid)]['Rating'].values

                _sum += abs(r-_r)
            user_dict[user] = _sum/len(user_item_ids)
            print("userID：{},AE：{}".format(user,user_dict[user]))
        return sum(user_dict.values())/len(user_dict.keys())


    def predict(self, userid, top_n=10):
        self.load()
        user_item_ids = set(self.user_item_rate_data[self.user_item_rate_data['UserID'] == userid]['MovieID'])
        other_item_ids = list(self.itemids.difference(user_item_ids))
        interest_list = [self._predict(userid, itemid) for itemid in other_item_ids]
        candidates = sorted(zip(other_item_ids, interest_list), key=lambda x: x[1], reverse=True)
        return candidates[:top_n]


if __name__ == '__main__':
    lfm = LFM()
    lfm._predict(1, 1)
