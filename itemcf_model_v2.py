#coding=utf-8

from __future__ import division
from base import *
from dataset_v2 import get_itemset, get_itemset_topk, get_simVal
from db_utils_v2 import connect_db

topKItems  = 50
gamma_1 = 0.65
gamma_2 = 0.15

# 预测评分
def predict_1(userId, itemId, sim_table, db_conn):
    itemset = get_itemset_topk(userId, topKItems)
    # itemset = get_itemset(userId)
    pred_score = 0
    for item in itemset:
        itemId2 = item[0]
        score = item[1]
        simVal = get_simVal(itemId, itemId2, sim_table, db_conn)
        pred_score += simVal * (1+score)**gamma_1
    return pred_score

def predict_2(userId, itemId, sim_table, db_conn):
    pass

# 测试模型
def model_test(db_conn):
    # simVal = sim(1, 2)
    userId = 1
    testCases = [188135, 250273, 60428, 187953, 108088, 52615]
    # 测试每一种相似度的结果
    for sim_table in sim_tables:
        print sim_table
        for case in testCases:
            pred_score = predict_1(userId, case, sim_table, db_conn)
            print '%d %d ==> %f' %(userId, case, pred_score)

if __name__ == '__main__':
    db_sim = "./data/kddcup2011_sim.db"
    conn_sim, cursor_sim = connect_db(db_sim)
    model_test(conn_sim)
    conn_sim.close()
    cursor_sim.close()