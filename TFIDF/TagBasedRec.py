'''
@Time    : 2020/4/29 9:48
@Author  : sh_lord
@FileName: TagBasedRec.py 基于标签的推荐

'''
import numpy as np
import pandas as pd
import math

USER_ARTISTS_DAT_PATH = "data/lastfm-2k/user_artists.dat"
USER_Artist_TAG_DAT_PATH = "data/lastfm-2k/user_taggedartists-timestamps.dat"
ARTISTS_DAT_PATH = "data/lastfm-2k/artists.dat"

class TagBasedRec:
    def __init__(self, K):
        self.K = K # 平滑因子
        self.allArtistIDsList = self.getAllArtistIDs()
        # 1. 用户u对艺术家i的打分（听的次数）TFIDF/data/lastfm-2k/user_artists.dat
        self.userArtistRateDict = self.getUserArtistRateDict()
        # 2. 艺术家与标签t的相似度（如果艺术家有对应的标签则记录，相关度为1，否则不为1）
        self.artistTagRelationDict, self.userTagCntDict, self.tagCntDict = self.getArtistTagRelationDict()
        # 3. 1、2得到用户u对标签t的打分, 可以加入平滑因子(k=1, 用户所有评分的平均值)
        # 4. TF计算：用户使用标签t的次数/用户使用所有标签标记的次数和
            # user->标签t cnt
        # 5. IDF计算：lg(所有用户对所有标签的次数/(所有用户对标签t的次数+1))
            # 标签t->cnt
        self.userTagRateDict = self.getUserTagRateDict()

    def getAllArtistIDs(self):
        allArtistIDSList = []
        with open(ARTISTS_DAT_PATH, 'r', encoding='utf8') as f_r:
            for line in f_r:
                if line.strip().startswith("id"):
                    continue
                artistID = line.strip().split("\t")[0]
                allArtistIDSList.append(artistID)
        return allArtistIDSList

    def getUserArtistRateDict(self):
        user_artist_rate_dict = dict()
        with open(USER_ARTISTS_DAT_PATH, 'r', encoding='utf8') as f_r:
            for row in f_r:
                if row.strip().startswith("userID"):
                    continue
                userID, artistID, score = row.strip().split("\t")
                score = int(score)
                user_artist_rate_dict.setdefault(userID, dict())
                user_artist_rate_dict[userID][artistID] = score
        return user_artist_rate_dict

    # 2. 艺术家与标签t的相似度（如果艺术家有对应的标签则记录，相关度为1，否则不为1）
    def getArtistTagRelationDict(self):
        artistTagRelationDict = dict()
        userTagCntDict = dict()
        tagCntDict = dict()
        with open(USER_Artist_TAG_DAT_PATH, 'r', encoding='utf8') as f_r:
            for line in f_r:
                if line.strip().startswith("userID"):
                    continue
                userID, artistID, tagID = line.strip().split("\t")[:3]
                artistID[tagID] = 1
                userTagCntDict.setdefault(userID, dict())
                userTagCntDict[userID][tagID] = userTagCntDict[userID].get(tagID, 0) + 1
                tagCntDict[tagID] = tagCntDict.get(tagID, 0) + 1
        return artistTagRelationDict, userTagCntDict, tagCntDict

    # 3. 1、2得到用户u对标签t的打分, 可以加入平滑因子(k=1, 用户所有评分的平均值)
    # 4. TF计算：用户使用标签t的次数/用户使用所有标签标记的次数和
    # user->标签t cnt
    # 5. IDF计算：lg(所有用户对所有标签的次数/(所有用户对标签t的次数+1))
    # 标签t->cnt
    def getUserTagRateDict(self):
        for userID in self.userTagCntDict.keys():
            for tagId in self.tagCntDict.keys():
                tf = self.userTagCntDict[tagId]/sum(self.userTagCntDict[userID].values())
                idf = math.log(sum(self.tagCntDict.values())/(self.tagCntDict[tagId] + 1))
                tfIdf = tf*idf
                nominator = 0
                denominator = 0
                for artistID in self.allArtistIDsList:
                    nominator += self.userArtistRateDict[userID].get(artistID, 0) \
                                 * self.artistTagRelationDict[artistID].get(tagId, 0)
                    denominator += self.artistTagRelationDict[artistID].get(tagId, 0)
                # 加入平滑因子
                nominator += self.K * sum(self.userArtistRateDict[userID].values()) \
                             / len(self.userArtistRateDict[userID].values())



        pass

