#coding=utf-8

#coding=utf-8

# 测试正确率

from __future__ import division
import os
import time
from base import *
from utils import proc_line
from itemcf_model_v2 import predict_1
from db_utils_v2 import connect_db

test_file = 'testIdx2.txt'
# test_file = './testSet/test50.txt'
# test_file = './testSet/test4000.txt'

def test_prec(sim_table, db_conn):
    test_file_in = os.path.join(source_dir, test_file)
    # test_file_in = test_file
    fi_test = open(test_file_in, 'r')
    total_num_of_testCases = 0
    right_num_of_testCases = 0
    userId = 0
    num_of_testCases = 0 # 测试实例总数目
    cur_testCase = 0     # 当前测试实例的序号
    testCases = {}       # 测试实例值,key means itemId, value means score
    predCases = []       # 预测值,predCases[0] means itemId, predCases[1] means score
    line_is_score = False
    for line in fi_test:
        line = line.rstrip('\n')
        if not line_is_score:
            seg_list = proc_line(line, '|')
            userId = int(seg_list[0])
            num_of_testCases = int(seg_list[1])
            total_num_of_testCases += num_of_testCases
            cur_testCase = 0
            predCases = [[] for x in range(num_of_testCases)]
            line_is_score = True
        else:
            seg_list = proc_line(line, '\t')
            itemId = int(seg_list[0])
            score = int(seg_list[1])
            testCases[itemId] = score
            pred_score = predict_1(userId, itemId, sim_table, db_conn)
            predCases[cur_testCase] = [itemId, pred_score]
            cur_testCase += 1
            if cur_testCase >= num_of_testCases:
                # 对预测分数进行排序
                predCases = sorted(predCases, key=lambda x:x[1], reverse=True)
                for i in range(3):
                    itemId = predCases[i][0]
                    if testCases[itemId] != -1:
                        right_num_of_testCases += 2
                predCases = []
                line_is_score = False
                # if not userId % 2000:
                #     print 'done with userId: %d' % userId
                print 'done with user ', userId
                if userId >= 1000:
                    break
    fi_test.close()
    return right_num_of_testCases / total_num_of_testCases


def test_main(sim_table, db_conn):
    start_time = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
    prec = test_prec(sim_table, db_conn)
    print "precision: %f" %(prec)
    end_time = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
    print 'start test at ', start_time, ',end test at ', end_time, '.'
    return prec

if __name__ == '__main__':
    db_sim = "./data/kddcup2011_sim.test.db"
    conn_sim, cursor_sim = connect_db(db_sim)
    for sim_table in sim_tables:
        print sim_table
        test_main(sim_table, conn_sim)
    conn_sim.close()
    cursor_sim.close()