#coding=utf-8

# 集成模型测试

from __future__ import division
import os
import io
from base import source_dir, result_dir, logger
from utils import proc_line
from itemcf_model import predict_2

test_file = 'testIdx2.txt'
result_data_prefix = 'result'

def fetch_user_score(file_in, max_userId, testset=False):
    user_score_dict = {}
    cur_userId = None
    fi = open(file_in, 'r')
    for line in fi:
        line = line.rstrip('\n')
        if line.find('\t') == -1:  # line is not score
            seg_list = proc_line(line, '|')
            cur_userId = int(seg_list[0])
            if cur_userId > max_userId: break
        else:
            seg_list = proc_line(line, '\t')
            itemId = int(seg_list[0])
            if testset:
                score = int(seg_list[1])
            else:
                score = float(seg_list[1])
            if not user_score_dict.has_key(cur_userId):
                user_score_dict[cur_userId] = {}
            user_score_dict[cur_userId][itemId] = score
    return user_score_dict

def ensemble_main():
    max_userId = 10000
    test_file_in = os.path.join(source_dir, test_file)
    test_user_scores = fetch_user_score(test_file_in, max_userId, testset=True)
    pred_user_scores = []
    pred_user_scores.append(fetch_user_score(os.path.join(result_dir, 'result_itemcf.txt.tN100_2'), max_userId))
    pred_user_scores.append(fetch_user_score(os.path.join(result_dir, 'result_v1.txt'), max_userId))
    ws = [0.0, 1.0]
    while(ws[0] <= 1.0):
        ws[1] = 1.0 - ws[0]
        total_num_of_testCases = 0
        right_num_of_testCases = 0
        for userId, itemset in test_user_scores.items():
            predCases = []       # 预测值,predCases[0] means itemId, predCases[1] means score
            for itemId, score in test_user_scores[userId].items():
                pred_score = 0.0
                for i in range(0, 2):
                    pred_score += ws[i]*pred_user_scores[i][userId][itemId]
                predCases.append([itemId, pred_score])
                total_num_of_testCases += 1
            # 对预测分数进行排序
            predCase_list = sorted(predCases, key=lambda x:x[1], reverse=True)
            for i in range(3):
                itemId = predCase_list[i][0]
                if test_user_scores[userId][itemId] != -1:
                    right_num_of_testCases += 2
        logger.info("weights: %f,%f" % (ws[0], ws[1]))
        prec = right_num_of_testCases / total_num_of_testCases
        logger.info("precision: %f" % (prec))
        # print "precision: %f" % (prec)
        ws[0] += 0.1

def test():
    max_userId = 10000
    test_file_in = os.path.join(source_dir, test_file)
    test_user_scores = fetch_user_score(test_file_in, max_userId, testset=True)
    pred_user_score = fetch_user_score(os.path.join(result_dir, 'result_v1.txt'), max_userId)
    total_num_of_testCases = 0
    right_num_of_testCases = 0
    for userId, itemset in test_user_scores.items():
        predCases = []       # 预测值,predCases[0] means itemId, predCases[1] means score
        for itemId, score in test_user_scores[userId].items():
            pred_score = pred_user_score[userId][itemId]
            predCases.append([itemId, pred_score])
            total_num_of_testCases += 1
        # 对预测分数进行排序
        predCase_list = sorted(predCases, key=lambda x:x[1], reverse=True)
        for i in range(3):
            itemId = predCase_list[i][0]
            if test_user_scores[userId][itemId] != -1:
                right_num_of_testCases += 2
    prec = right_num_of_testCases / total_num_of_testCases
    print "precision: %f" % (prec)

if __name__ == '__main__':
    ensemble_main()
    # test()
