#coding=utf-8

from __future__ import division
from base import logger
from dataset import get_itemset, get_itemset_topk, get_userset, get_simVal

# topK  = 50
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
def predict_1(co_rated_dir, userId, itemId):
    itemset = get_itemset(userId)
    pred_score = 0
    for item in itemset:
        itemId2 = item[0]
        score = item[1]
        simVal = get_simVal(co_rated_dir, itemId, itemId2)
        pred_score += simVal * (1+score)**gamma
    return pred_score

def predict_2(co_rated_dir, userId, itemId, topN):
    itemset = get_itemset(userId)
    simset = []
    for item in itemset:
        itemId2 = item[0]
        score = item[1]
        simVal = get_simVal(co_rated_dir, itemId, itemId2)
        simset.append((simVal, score))
    sim_list = sorted(simset, key=lambda x:x[0], reverse=True)
    pred_score = 0
    for sim in sim_list[0:topN]:
        pred_score += sim[0] * (1+sim[1])**gamma
    return pred_score


def test_model(co_rated_dir, topN):
    # simVal = sim(1, 2)
    userId = 1
    testCases = [188135, 250273, 60428, 187953, 108088, 52615]
    for case in testCases:
        pred_score = predict_1(co_rated_dir, userId, case)
        s = '[predict_1]%d => %d: %f' %(userId, case, pred_score)
        print s
        logger.info(s)
        pred_score = predict_2(co_rated_dir, userId, case, topN)
        s = '[predict_2]%d => %d: %f' %(userId, case, pred_score)
        print s
        logger.info(s)

if __name__ == '__main__':
    test_model('./data/co_rated_dir.tk100_1', 50)