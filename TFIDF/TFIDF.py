'''
@Time    : 2020/4/28 22:37
@Author  : sh_lord
@FileName: TFIDF.py

'''
import numpy as np
import pandas as pd
from Constants import *
import jieba
import math

class TFTDF:
    def __init__(self):
        self.id_title = pd.read_csv(ID_TITILE_PATH, header=None, names=["id","title"], sep="\t", encoding="utf-8")
        self.stop_words = self.loadStopWords(STOP_WORDS_PATH)
        self.wordsNums = 0 # 总词数
        self.docNums = self.id_title.size() # 总文档数
        self.termFreqDict = dict() # word -> 词频
        self.wordDocSetDict = dict() # word -> 文档set

    def loadStopWords(self, filePath):
        stop_words = set()
        with open(filePath, 'r', encoding="utf-8") as f_r:
            for word in f_r:
                word = word.strip()
                stop_words.add(word)
        print("load stop words finished, size: {}".format(len(stop_words)))
        return stop_words

    def dataProcess(self):
        for _tup in self.id_title.itertuples():
            docid = _tup['id']
            title = _tup['title']
            words = jieba.cut(title.strip())
            for word in words:
                if word in self.stop_words:
                    continue
                self.wordsNums += 1
                self.termFreqDict[word] = self.termFreqDict.get(word, 0) + 1
                self.wordDocSetDict.setdefault(word, set())
                self.wordDocSetDict[word].add(docid)


    def calculateTFIDF(self, word):
        tf = self.termFreqDict.get(word, 0) / self.wordsNums
        wordDocNums = len(self.wordDocSetDict.get(word)) if word in self.wordDocSetDict else 0
        idf = math.log10(self.docNums/(1 + wordDocNums))
        return tf * idf

if __name__ == '__main__':
    tfidf = TFTDF()
    tfidf.dataProcess()
