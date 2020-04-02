'''
@Time    : 2020/3/31 23:10
@Author  : sh_lord
@FileName: kMeans.py

'''
# 使用Python读写csv文件的三种方法
# https://www.cnblogs.com/cloud-ken/p/8432999.html
import csv
import pandas as pd
import numpy as np

class kMeans:
    def __init__(self, file_path):
        """
csv_data = pd.read_csv('birth_weight.csv')  # 读取训练数据
print(csv_data.shape)  # (189, 9)
N = 5
csv_batch_data = csv_data.tail(N)  # 取后5条数据
print(csv_batch_data.shape)  # (5, 9)
train_batch_data = csv_batch_data[list(range(3, 6))]  # 取这20条数据的3到5列值(索引从0开始)
print(train_batch_data)

        """
        self.skuid_price_data = skuid_price_data = pd.read_csv('data/sku-price/skuid_price.csv')
        print("data shape: ", skuid_price_data.shape)
        print("############# data example #############")
        example_data = skuid_price_data.head(5)
        print(example_data)

    def get_cluster_id(self, price, centres):
        centres_price = centres["price"]
        idx = np.argmin((centres_price-price)**2)
        return idx

    def update_centers(self, clusters: dict, centres: list):
        _centres = []
        for key, points in clusters.items():
            average = np.average(points["price"])
            _centres.append(average)
        centres = _centres


    def train(self, K=3, steps=10):
        skuid_price_data = self.skuid_price_data
        centres = skuid_price_data.sample(n=K)["price"]
        clusters = dict()
        while steps:
            for idx, row in skuid_price_data.iterrows():
                skuid = row["skuid"]
                price = row["price"]
                cluster_id = self.get_cluster_id(price, centres)
                clusters.setdefault(clusters, []).append(row)
            self.update_centers(clusters, centres)


            steps -= 1

        pass

    def predict(self):
        pass

if __name__ == '__main__':
    file_path = "data/sku-price/skuid_price.csv"
    kMeans = kMeans(file_path)
    kMeans.train(K=3, steps=10)