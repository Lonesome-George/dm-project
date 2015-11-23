#coding=utf-8

# 将预处理数据保存至数据库

from __future__ import division
from base import *
from dataset_v2 import *
import time
import math

co_rated_table_creat = "CREATE TABLE IF NOT EXISTS %s (id integer PRIMARY KEY autoincrement,\
        iid1 integer, iid2 integer, co_rated_num integer)" % co_rated_table
item_rated_table_creat = "CREATE TABLE IF NOT EXISTS %s (id integer PRIMARY KEY autoincrement,\
        iid integer, rated_num integer)" % item_rated_table
simple_sim_table_creat = "CREATE TABLE IF NOT EXISTS %s (id integer PRIMARY KEY autoincrement,\
        iid1 integer, iid2 integer, sim_val numeric(6,4))" % simple_sim_table
cos_sim_table_creat = "CREATE TABLE IF NOT EXISTS %s (id integer PRIMARY KEY autoincrement,\
        iid1 integer, iid2 integer, sim_val numeric(6,4))" % cos_sim_table

def save_co_rated(co_rated_dict, conn):
    cursor = conn.cursor()
    co_rated_list = [] # 构造多元组,批量插入数据
    for itemIdi, related_items in co_rated_dict.items():
        for itemIdj, co_rated_num in related_items.items():
            co_rated_list.append((int(itemIdi), int(itemIdj), co_rated_num))
    cursor.executemany("INSERT INTO %s VALUES(NULL, ?, ?, ?)" % co_rated_table, co_rated_list)
    conn.commit()

def save_item_rated(item_voted_dict, conn):
    cursor = conn.cursor()
    item_voted_list = []
    for itemId, rated_num in item_voted_dict.items():
        item_voted_list.append((int(itemId), rated_num))
    cursor.executemany("INSERT INTO %s VALUES(NULL, ?, ?)" % item_rated_table, item_voted_list)
    conn.commit()

# 统计评分矩阵
def stat_rated_num(trainsize, topK, conn, cursor):
    cursor.execute(co_rated_table_creat)
    cursor.execute(item_rated_table_creat)
    conn.commit()
    # calculate co-rated users between items
    co_rated_dict = dict()   # item-item co-rated matrix
    item_voted_dict = dict() # number that each item was voted
    for userId in range(nUsers):
        if not userId % 2000:
            print 'current userId: %d' % userId
        if len(co_rated_dict) > max_size: # 为了防止内存溢出,将这部分数据保存到数据库
            save_co_rated(co_rated_dict, conn)
            co_rated_dict = {} # 清空字典
        if trainsize > 0 and userId > trainsize:
            break
        itemset = get_itemset_topk(userId, topK)
        # itemset = get_itemset(userId)
        if len(itemset) > topK: continue
        for itemi in itemset:
            itemIdi = itemi[0]
            if not item_voted_dict.has_key(itemIdi):
                item_voted_dict[itemIdi] = 0
            item_voted_dict[itemIdi] += 1
            for itemj in itemset:
                itemIdj = itemj[0]
                if itemIdi == itemIdj:
                    continue
                if not co_rated_dict.has_key(itemIdi):
                    co_rated_dict[itemIdi] = dict()
                if not co_rated_dict[itemIdi].has_key(itemIdj):
                    co_rated_dict[itemIdi][itemIdj] = 0
                co_rated_dict[itemIdi][itemIdj] += 1
    save_co_rated(co_rated_dict, conn)
    save_item_rated(item_voted_dict, conn)
    cursor.execute("CREATE INDEX co_idx ON %s(iid1,iid2)" % co_rated_table)
    cursor.execute("CREATE INDEX item_idx ON %s(iid)" % item_rated_table)
    conn.commit()

# calculate final similarity matrix
def calc_simple_sim(conn, cursor):
    cursor.execute(simple_sim_table_creat)
    conn.commit()
    sim_list = []
    for itemIdi in range(0, nItems):
        if not itemIdi % 2000:
            print 'current itemId: %d' % itemIdi
        itemi_rated = get_rated_num(itemIdi, conn)
        # 查找跟itemi共现过的所有item
        itemset = get_co_rated_itemset(itemIdi, conn)
        for itemj in itemset:
            itemIdj = itemj[0]
            co_rated_num = itemj[1]
            itemj_rated = get_rated_num(itemIdj, conn)
            # sim_val = co_rated_num / (itemi_rated + itemj_rated - co_rated_num + 1) # 加1防止出现除以0
            sim_val = co_rated_num / (math.sqrt(itemi_rated * itemj_rated) +1) # 加1防止出现除以0
            sim_list.append((itemIdi, itemIdj, sim_val))
        if len(sim_list) > 0:
            cursor.executemany("INSERT INTO %s VALUES(NULL, ?, ?, ?)" % simple_sim_table, sim_list)
            conn.commit()
        sim_list = []
    cursor.execute("CREATE INDEX sim_idx ON %s(iid1,iid2)" % simple_sim_table)
    conn.commit()

# 计算余弦相似度
def calc_cos_sim(conn, cursor):
    cursor.execute(cos_sim_table_creat)
    conn.commit()
    sim_list = []
    for itemIdi in range(0, nItems):
        if not itemIdi % 2000:
            print 'current itemId: %d' % itemIdi
        userseti = get_userset(itemIdi)
        len_userseti = len(userseti)
        for itemIdj in range(0, nItems):
            usersetj = get_userset(itemIdj)
            co_userset = [user for user in userseti if user in usersetj]
            sim_val = len(co_userset) / (len_userseti + len(usersetj) - len(co_userset))
            sim_list.append((itemIdi, itemIdj, sim_val))
        if len(sim_list) > 0:
            cursor.executemany("INSERT INTO sim VALUES(NULL, ?, ?, ?)", sim_list)
            conn.commit()
        sim_list = []
    cursor.execute("CREATE INDEX sim_idx ON sim(iid1,iid2)")
    conn.commit()

def preproc_main(trainsize, topK, db_conn, db_cursor):
    start_time = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
    stat_rated_num(trainsize, topK, db_conn, db_cursor)
    calc_simple_sim(db_conn, db_cursor)
    # calc_cos_sim(db_conn, db_cursor)
    end_time = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
    print 'start preprocess at ', start_time, ',end preprocess at ', end_time, '.'

if __name__ == '__main__':
    db_sim = "./data/kddcup2011_sim.test.db"
    db_conn, db_cursor = connect_db(db_sim)
    preproc_main(50, 50, db_conn, db_cursor)
    db_conn.close()
    db_cursor.close()