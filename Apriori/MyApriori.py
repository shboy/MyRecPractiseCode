'''
@Time    : 2020/4/9 17:22
@Author  : sh_lord
@FileName: MyApriori.py

'''
class MyApriori:
    def __init__(self, min_support=0.5, min_confidence=0.6):
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.data = self.load_data()
        pass

    def load_data(self):
        return [[1, 5], [2, 3, 4], [2, 3, 4, 5], [2, 3]]

    def gen_C1(self):
        # C1 若是为set，[item] 为列表不能hash，添加不了
        C1 = []
        data = self.data
        for items in data:
            for item in items:
                if [item] not in C1:
                    C1.append([item])
        return list(map(frozenset, C1))

    # 得到频繁项集
    def scanD(self, Ck):
        data = list(map(set, self.data))
        Lk = []
        support_data = {}
        for items in data:
            for one in Ck:
                if one.issubset(items):
                    support_data.setdefault(one, 0)
                    support_data[one] += 1

        num_data = len(self.data)
        for key, value in support_data.items():
            support = value/num_data
            if support >= self.min_support:
                Lk.insert(0, key)
            support_data[key] = support

        return  Lk, support_data

    def gen_new_Ck(self, Lk, k):
        next_Ck = []
        len_Ck = len(Lk)
        for i in range(len_Ck):
            for j in range(i+1, len_Ck):
                # FIXME: list能保证顺序？
                _C1 = list(Lk[i])[:k-2]
                _C2 = list(Lk[j])[:k-2]
                if sorted(_C1) == sorted(_C2):
                    next_Ck.insert(0, Lk[i]|Lk[j])
        return next_Ck

    def gen_new_Lk(self):
        C1 = self.gen_C1()
        L1, support_data = self.scanD(C1)
        L = [L1]
        k = 2
        while (len(L[k-2]) > 0):
            Ck = apriori.gen_new_Ck(L[k-2], k)
            Lk, support_k = self.scanD(Ck)
            support_data.update(support_k)
            L.append(Lk)
            k += 1
        return L, support_data

    #generateRules
    def gen_rules(self, L, support_data):
        pass








if __name__ == '__main__':
    apriori = MyApriori(min_support=0.5, min_confidence=0.6)
    L, support_data = apriori.gen_new_Lk()
    pass

