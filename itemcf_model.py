#encoding=utf-8

from __future__ import division
from dataset import get_itemset_topk, get_userset

topK  = 50
gamma = 0.65

# 计算相似度
def sim(itemId1, itemId2):
    userset1 = get_userset(itemId1)
    userset2 = get_userset(itemId2)
    # 分别求出userset1和userset2的交集和并集
    intersect = [val for val in userset1 if val in userset2]
    union = list(set(userset1).union(set(userset2)))
    return len(intersect) / len(union)

# 预测评分
def predict(userId, itemId):
    itemset = get_itemset_topk(userId, topK)
    pred_score = 0
    for item in itemset:
        itemId2 = item[0]
        score = item[1]
        pred_score += sim(itemId, itemId2) * (1+score)**gamma
    return pred_score

if __name__ == '__main__':
    # sim = sim(1, 2)
    testCases = [188135, 250273, 60428, 187953, 108088, 52615]
    for case in testCases:
        pred_score = predict(1, case)
        print pred_score