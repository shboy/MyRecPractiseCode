'''
@Time    : 2020/4/29 9:48
@Author  : sh_lord
@FileName: TagBasedRec.py 基于标签的推荐

'''
class TagBasedRec:
    def __init__(self):
        # 1. 用户u对艺术家i的打分（听的次数）TFIDF/data/lastfm-2k/user_artists.dat
        self.userArtistRateDict = self.getUserArtistRateDict()
        # 2. 艺术家与标签t的相似度（如果艺术家有对应的标签则记录，相关度为1，否则不为1）
        self.artistTagRelationDict = self.getArtistTagRelationDict()
        # 3. 1、2得到用户u对标签t的打分, 可以加入平滑因子(k=1, 用户所有评分的平均值)
        # 4. TF计算：用户使用标签t的次数/用户使用所有标签标记的次数和
            # user->标签t Set
        # 5. IDF计算：lg(所有用户对所有标签的次数/(所有用户对标签t的次数+1))
            # 标签t->user Set
        self.userTagRateDict = self.getUserTagRateDict()

    def getUserArtistRateDict(self):
        pass

    def getArtistTagRelationDict(self):
        pass

    def getUserTagRateDict(self):
        pass

