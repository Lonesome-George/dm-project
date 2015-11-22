#coding=utf-8

import os
from base import *
from db_utils_v2 import connect_db

stat_dir = os.path.join(store_dir, 'stat')

# 获得用户对应的所有打分（包括对歌曲，歌手，专辑和曲风）
def get_votes(userId, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT iid, score FROM train WHERE uid=?", (userId,))
    return cursor.fetchall()

if __name__ == '__main__':
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