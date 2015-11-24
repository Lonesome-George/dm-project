#coding=utf-8

# 测试正确率

from __future__ import division
import os
import time
from base import *
from utils import proc_line
from itemcf_model import predict_1, predict_2

test_file = 'testIdx2.txt'

def test_prec(co_rated_dir, topN):
    test_file_in = os.path.join(source_dir, test_file)
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
            # pred_score = predict_1(co_rated_dir, userId, itemId)
            pred_score = predict_2(co_rated_dir, userId, itemId, topN)
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
                print 'done with user: %d' % userId
                if userId >= 50:
                    break
    fi_test.close()
    logger.info("similarity file:%s" % co_rated_dir)
    logger.info("test data size: %d|topN:%d" % (userId, topN))
    prec = right_num_of_testCases / total_num_of_testCases
    logger.info("precision: %f" % (prec))
    return prec


ISOTIMEFORMAT = '%Y-%m-%d %X'

if __name__ == '__main__':
    start_time = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
    prec = test_prec('./data/co_rated_dir.tk100_1', 30)
    print "precision: %f" %(prec)
    end_time = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
    print 'start at ', start_time, ',end at ', end_time, '.'