'''
@Time    : 2020/4/6 20:04
@Author  : sh_lord
@FileName: Apriori.py

'''
class Apriori:
    def __init__(self, min_support, min_confidence):
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.data = self.load_data()

    def load_data(self):
        return [[1,5], [2,3,4], [2,3,4,5], [2,3]]

