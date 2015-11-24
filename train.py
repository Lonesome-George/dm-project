#coding=utf-8

#迭代训练调参

import os
from base import *
from utils import find_dirname
from preprocess import preproc_main
from itemcf_model import test_model
from test_prec import test_prec

def train():
    topKs = [50, 75, 100]
    topNs = [50, 75] # 预测的时候对每个用户所选取的top item数目
    co_rated_dir_prefix = "co_rated_dir"
    for topK in topKs:
        co_rated_dir = find_dirname(store_dir, '%s.tk%d' %(co_rated_dir_prefix, topK))
        logger.info('topK: %d.' %(topK))
        logger.info('Start preprocess')
        preproc_main(co_rated_dir, topK)
        logger.info('End preprocess.')
        for topN in topKs:
            logger.info('Start test model')
            test_model(co_rated_dir, topN)
            logger.info('End test model')
            logger.info('Start predict.')
            prec = test_prec(co_rated_dir, topN)
            logger.info('End predict(precision: %f).' % prec)

# 测试不同参数的效果
def test_param():
    topKs = [50, 75, 100] # 训练的时候对每个用户所选取的top item数目
    topNs = [50, 75] # 预测的时候对每个用户所选取的top item数目
    co_rated_dir_prefix = "co_rated_dir"
    for topK in topKs:
        co_rated_dir = os.path.join(store_dir, '%s.tk%d_1' %(co_rated_dir_prefix, topK))
        for topN in topNs:
            logger.info('Start test model')
            test_model(co_rated_dir, topN)
            logger.info('End test model')
            logger.info('Start predict.')
            prec = test_prec(co_rated_dir, topN)
            logger.info('End predict(precision: %f).' % prec)

if __name__ == '__main__':
    test_param()