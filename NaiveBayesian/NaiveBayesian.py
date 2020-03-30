'''
@Time    : 2020/3/30 22:42
@Author  : sh_lord
@FileName: NaiveBayesian.py

'''
import numpy as np


class NaiveBayesian:
    def __init__(self):
        self.data, self.labels = self.load_data()

        pass

    def load_data(self):
        data = np.array(
            [
                [320, 204, 198, 265],
                [253, 53, 15, 2243],
                [53, 32, 5, 325],
                [63, 50, 42, 98],
                [1302, 523, 202, 5430],
                [32, 22, 5, 143],
                [105, 85, 70, 322],
                [872, 730, 840, 2762],
                [16, 15, 13, 52],
                [92, 70, 21, 693],
            ]
        )
        labels = np.array([1, 0, 0, 1, 0, 0, 1, 1, 1, 0])
        return data, labels

    def get_feat_charactors(self):
        data = self.data
        labels_0_idx = self.labels == 0
        labels_1_idx = self.labels == 1
        data_shape = np.shape(data)
        labels_0_num = np.sum(labels_0_idx)
        labels_1_num = np.sum(labels_1_idx)
        tmp = data[labels_1_idx]
        average_0 = np.sum(data[labels_0_idx], axis=0) / labels_0_num
        average_1 = np.sum(data[labels_1_idx], axis=0) / labels_1_num
        sigma_0 = np.sqrt(np.sum((data[labels_0_idx])**2)) / labels_0_num
        sigma_1 = np.sqrt(np.sum((data[labels_1_idx])**2)) / labels_1_num
        average = np.sum(data, axis=0) / data_shape[0]
        sigma = np.sqrt((data - average)**2) / (data_shape[0]-1)


        # self.sigma = np.

    def train(self):

        pass

    def predict(self):
        pass

if __name__ == '__main__':
    naiveBayesian = NaiveBayesian()
    naiveBayesian.get_feat_charactors()
