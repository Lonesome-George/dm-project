#encoding=utf-8

# 测试正确率

import os
from __future__ import division
from preprocess import source_dir
from utils import proc_line
from itemcf_model import predict

test_file = './testIdx2.txt'

if __name__ == '__main__':
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
            line_is_score = True
        else:
            seg_list = proc_line(line, '\t')
            itemId = int(seg_list[0])
            score = int(seg_list[1])
            testCases[itemId] = score
            pred_score = predict(userId, itemId)
            predCases[cur_testCase] = [itemId, pred_score]
            cur_testCase += 1
            if cur_testCase >= num_of_testCases:
                # 对预测分数进行排序
                predCases = sorted(predCases, key=lambda x:x[1], reverse=True)
                for i in range(3):
                    itemId = predCases[i][0]
                    if testCases[itemId] != -1:
                        right_num_of_testCases += 2
                line_is_score = False
    fi_test.close()
    print 'precision: ' + str(right_num_of_testCases / total_num_of_testCases)