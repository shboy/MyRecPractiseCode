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
        skuid_price_data = pd.read_csv('data/sku-price/skuid_price.csv')
        print("data shape: ", skuid_price_data.shape)
        print("############# data example #############")
        example_data = skuid_price_data.head(5)
        print(example_data)
        print("############# filter 异常值  #############")
        upper_limit = np.mean(skuid_price_data['price']) + 3*np.std(skuid_price_data['price'])
        lower_limit = np.mean(skuid_price_data['price']) - 3*np.std(skuid_price_data['price'])
        # max_idx = upper_limit >= skuid_price_data['price']
        # min_idx = skuid_price_data['price'] >= lower_limit
        upper_limit = upper_limit if upper_limit > 5000 else 5000
        lower_limit = lower_limit if upper_limit > 1 else 1
        print("upper_limit: {}, lower_limit: {}".format(upper_limit, lower_limit))
        skuid_price_data = skuid_price_data[(upper_limit >= skuid_price_data['price']) &
                                            (skuid_price_data['price'] >= lower_limit)]
        self.skuid_price_data = skuid_price_data

    def get_cluster_id(self, price, centres):
        centres_price = centres
        idx = np.argmin((centres_price-price)**2)
        return idx

    def update_centers(self, clusters: dict, centres: list):
        _centres = []
        for key, points in clusters.items():
            average = np.average(points)
            _centres.append(average)
        centres = _centres


    def train(self, K=3, steps=10):
        skuid_price_data = self.skuid_price_data
        centres = list(skuid_price_data.sample(n=K)["price"].values)
        clusters = dict()
        while steps:
            for idx, row in skuid_price_data.iterrows():
                skuid = row["skuid"]
                price = row["price"]
                cluster_id = self.get_cluster_id(price, centres)
                clusters.setdefault(cluster_id, []).append(price)
            self.update_centers(clusters, centres)


            steps -= 1

        return clusters

    def predict(self, clusters: dict):
        pass

if __name__ == '__main__':
    file_path = "data/sku-price/skuid_price.csv"
    kMeans = kMeans(file_path)
    clusters: dict = kMeans.train(K=3, steps=10)
    print(clusters)
