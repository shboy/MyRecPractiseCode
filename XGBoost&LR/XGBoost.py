'''
@Time    : 2020/5/7 9:44
@Author  : sh_lord
@FileName: XGBoost.py

'''
from sklearn.model_selection import  train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import metrics
from sklearn.metrics import mean_squared_error
import pandas as pd
import os

class ChurnPredWithGBDT:
    def __init__(self):
        self.file = "../data/telecom-churn/telecom-churn-prediction-data.csv"
        self.data = self.feature_transform()
        self.train, self.test = self.split_data()

    def isNone(self, value):
        if

    def feature_transform(self):
        pass

    def split_data(self0):
        pass