#coding=utf-8

from __future__ import division
from dataset_v2 import get_itemset_topk, get_simVal
from db_utils_v2 import connect_db

trainSize = 5000 # 训练集大小
topK  = 50
gamma = 0.65

db_sim = "./data/kddcup2011_sim.db"
conn_sim, cursor_sim = connect_db(db_sim)

# 预测评分
def predict(userId, itemId):
    itemset = get_itemset_topk(userId, topK)
    pred_score = 0
    for item in itemset:
        itemId2 = item[0]
        score = item[1]
        simVal = get_simVal(itemId, itemId2, conn_sim)
        pred_score += simVal * (1+score)**gamma
    return pred_score

if __name__ == '__main__':
    # simVal = sim(1, 2)
    testCases = [188135, 250273, 60428, 187953, 108088, 52615]
    for case in testCases:
        pred_score = predict(1, case)
        print pred_score