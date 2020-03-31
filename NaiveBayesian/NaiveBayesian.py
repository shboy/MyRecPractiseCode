'''
@Time    : 2020/3/30 22:42
@Author  : sh_lord
@FileName: NaiveBayesian.py

'''
import numpy as np
import math


class NaiveBayesian:
    def __init__(self):
        self.data, self.labels = self.load_data()

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
        sigma_0 = np.sqrt(np.sum((data[labels_0_idx])**2 / labels_0_num, axis=0))
        sigma_1 = np.sqrt(np.sum((data[labels_1_idx])**2 / labels_1_num, axis=0))

        self.average = average = [average_0, average_1]
        self.sigma = sigma = [sigma_0, sigma_1]
        self.labels_0_num = labels_0_num
        self.labels_1_num = labels_1_num

        return average, sigma


    def train(self):
        average, sigma = self.get_feat_charactors()

    def predict(self, x):
        assert x.shape[0] == self.data.shape[1]

        p_label_0 = self.labels_0_num / self.data.shape[0]
        p_label_1 = 1 - p_label_0
        for i, xi in enumerate(x):
            #label0
            part1_label_0 = 1.0 / np.sqrt(2*math.pi*self.sigma[0][i]**2)
            part1_label_1 = 1.0 / np.sqrt(2*math.pi*self.sigma[1][i]**2)

            p_label_0 *= part1_label_0 * np.exp(-(xi-self.average[0][i])**2/(2*self.sigma[0][i]**2))
            p_label_1 *= part1_label_1 * np.exp(-(xi-self.average[1][i])**2/(2*self.sigma[1][i]**2))

        if (p_label_0 > p_label_1):
            return 0
        else:
            return 1

if __name__ == '__main__':
    naiveBayesian = NaiveBayesian()
    naiveBayesian.train()
    x = np.array([134, 84, 235, 349])
    print(naiveBayesian.predict(x))
    x = np.array([253, 53, 15, 2243])
    print(naiveBayesian.predict(x))
