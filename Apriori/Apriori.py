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

    # 生成项集C1，不包含项集中每个元素出现的次数
    def createC1(self, data):
        C1 = list()
        for items in data:
            for item in items:
                if [item] not in C1:
                    C1.append([item])
        return list(map(frozenset, sorted(C1)))

    """
    data: [[1,5], [2,3,4], [2,3,4,5], [2,3]]
    C1: [frozenset({1}), frozenset({2}), frozenset({3}), frozenset({4}), frozenset({5})]
    """
    # 该函数用于从候选项集Ck生成Lk，Lk表示满足最低支持度的元素集合
    def scanD(self, Ck):
        Data = list(map(set, self.data))
        CkCount = {}
        for items in Data:
            for one in Ck:
                if one.issubset(items):
                    CkCount.setdefault(one, 0)
                    CkCount[one] += 1
        numItems = len(list(Data))
        Lk = []
        supportData = {}
        for key in CkCount:
            support = CkCount[key] * 1.0 / numItems
            if support >= self.min_support:
                Lk.insert(0, key)
            supportData[key] = support
        return Lk, supportData

    def generateNewCk(self, Lk, k):
        nextLk = []
        lenLk = len(Lk)
        for i in range(lenLk):
            for j in range(i+1, lenLk):
                L1 = list(Lk[i])[: k-2]
                L2 = list(Lk[j])[: k-2]
                if sorted(L1) == sorted(L2):
                    nextLk.append(Lk[i] | Lk[j])
        return nextLk

    def gengrateLK(self):
        C1 = self.createC1(self.data)
        L1, supportData = self.scanD(C1)
        L = [L1]
        k = 2
        while len(L[k-2]) > 0:
            Ck = self.generateNewCk(L[k-2], k)
            Lk, supK = self.scanD(Ck)
            supportData.update(supK)
            L.append(Lk)
            k += 1
        return L, supportData

    """
    L: [[frozenset({4}), frozenset({3}), frozenset({2}), frozenset({5})], [frozenset({2, 3}), frozenset({2, 4}), frozenset({3, 4})], [frozenset({2, 3, 4})], []]
    supportData: {frozenset({1}): 0.25, frozenset({5}): 0.5, frozenset({2}): 0.75, frozenset({3}): 0.75, frozenset({4}): 0.5, frozenset({3, 4}): 0.5, frozenset({2, 4}): 0.5, frozenset({2, 3}): 0.75, frozenset({4, 5}): 0.25, frozenset({3, 5}): 0.25, frozenset({2, 5}): 0.25, frozenset({2, 3, 4}): 0.5}
    """
    def generateRules(self, L, supportData):
        ruleResult = []
        for i in range(1, len(L)):
            for ck in L[i]:
                Cks = [frozenset([item]) for item in ck]
                self.rulesOfMore(ck, Cks, supportData, ruleResult)
        return ruleResult

    def rulesOfMore(self, ck, Cks, supportData, ruleResult):
        m = len(Cks[0])
        while len(ck) > m:
            Cks = self.rulesOfTwo(ck, Cks, supportData, ruleResult)
            if len(Cks) > 1:
                Cks = self.generateNewCk(Cks, m+1)
                m+=1
            else:
                break


    def rulesOfTwo(self, ck, Cks, supportData, ruleResult):
        prunedH = []
        for oneCk in Cks:
            conf = supportData[ck] / supportData[ck - oneCk]
            if conf >= self.min_confidence:
                print(ck - oneCk, "-->", oneCk, "Confidence is:", conf)
                ruleResult.append((ck - oneCk, oneCk, conf))
                prunedH.append(oneCk)
        return prunedH

if __name__ == '__main__':
    apriori = Apriori(min_support=0.5, min_confidence=0.6)
    L, supportData = apriori.generateNewCk()
    for one in L:
        print("项数为 %s 的频繁项集：" % (L.index(one) + 1), one)
    print("supportData:", supportData)
    print("minConf={}时：".format(0.6))





