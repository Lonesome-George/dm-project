#coding=utf-8

import os
from base import *
from db_utils_v2 import connect_db
import logging
import logging.config

stat_dir = os.path.join(store_dir, 'stat')

# 获得用户对应的所有打分（包括对歌曲，歌手，专辑和曲风）
def get_votes(userId, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT iid, score FROM train WHERE uid=?", (userId,))
    return cursor.fetchall()

def stat():
    if not os.path.isdir(stat_dir):
        os.mkdir(stat_dir)
    m_db_train = "./data/kddcup2011_train.db"
    file_out = os.path.join(stat_dir, 'train_stat.csv')
    conn_train, cursor_2 = connect_db(m_db_train)
    fo = open(file_out, 'w')
    for userId in range(0, nUsers):
        votes = get_votes(userId, conn_train)
        string = str(userId) + ',' + str(len(votes)) + '\n'
        fo.write(string)
    fo.close()

def test_log():
    #日志初始化
    LOG_FILENAME = 'logging.conf'
    logging.config.fileConfig(LOG_FILENAME)
    logger = logging.getLogger("simple_log_example")

    #测试代码
    logger.debug("debug message")
    logger.info("info message")
    logger.warn("warn message")
    logger.error("error message")
    logger.critical("critical message")


if __name__ == '__main__':
    test_log()