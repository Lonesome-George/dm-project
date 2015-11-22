#coding=utf-8

# 将预处理数据保存至数据库

from __future__ import division
from base import *
from dataset_v2 import *
from itemcf_model_v2 import trainSize, topK
import time

# item共现表
co_rated_table = "CREATE TABLE IF NOT EXISTS co_rated (id integer PRIMARY KEY autoincrement,\
        iid1 integer, iid2 integer, co_rated_num integer)"
# item评分表
item_rated_table = "CREATE TABLE IF NOT EXISTS item_rated (id integer PRIMARY KEY autoincrement,\
        iid integer, rated_num integer)"
# similarity相似度表
sim_table = "CREATE TABLE IF NOT EXISTS sim (id integer PRIMARY KEY autoincrement,\
        iid1 integer, iid2 integer, sim_val numeric(6,4))"

def save_co_rated(co_rated_dict, conn):
    cursor = conn.cursor()
    co_rated_list = [] # 构造多元组,批量插入数据
    for itemIdi, related_items in co_rated_dict.items():
        for itemIdj, co_rated_num in related_items.items():
            co_rated_list.append((int(itemIdi), int(itemIdj), co_rated_num))
    cursor.executemany("INSERT INTO co_rated VALUES(NULL, ?, ?, ?)", co_rated_list)
    conn.commit()

def save_item_rated(item_voted_dict, conn):
    cursor = conn.cursor()
    item_voted_list = []
    for itemId, rated_num in item_voted_dict.items():
        item_voted_list.append((int(itemId), rated_num))
    cursor.executemany("INSERT INTO item_rated VALUES(NULL, ?, ?)", item_voted_list)
    conn.commit()

# 统计评分矩阵
def stat_rated_num(conn, cursor):
    cursor.execute(co_rated_table)
    cursor.execute(item_rated_table)
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
        if userId > trainSize:
            save_co_rated(co_rated_dict, conn)
            break
            # 构造多元组,批量插入数据
            # co_rated_list = []
            # for itemIdi, related_items in co_rated_dict.items():
            #     for itemIdj, co_rated_num in related_items.items():
            #         # records = get_co_rated_num(int(itemIdi), int(itemIdj), conn)
            #         # if len(records) != 0:# 如果已经存在记录,则将统计数据叠加
            #         #     del_co_rated_num(int(itemIdi), int(itemIdj), conn)
            #         #     co_rated_num += records[0][0]
            #         co_rated_list.append((int(itemIdi), int(itemIdj), co_rated_num))
            # cursor.executemany("INSERT INTO co_rated VALUES(NULL, ?, ?, ?)", co_rated_list)
            # conn.commit()
            # # co_rated_list = sorted(co_rated_dict.items(), key=lambda x:x[0]) # 按itemId值排序,方便查找
            # # for item in co_rated_list:
            # #     itemIdi = item[0]
            # #     related_items = item[1]
            # #     for itemIdj, co_rated_num in related_items.items():
            # #         records = get_co_rated_num(int(itemIdi), int(itemIdj), conn)
            # #         if len(records) != 0:# 如果已经存在记录,则将统计数据叠加
            # #             co_rated_num += records[0][0]
            # #             update_co_rated_num(int(itemIdi), int(itemIdj), co_rated_num, conn)
            # #         else:
            # #             cursor.execute("INSERT INTO co_rated VALUES(NULL, ?, ?, ?)",
            # #                        (int(itemIdi), int(itemIdj), co_rated_num))
            # #         conn.commit()
            # co_rated_list = []
            # co_rated_dict = {} # 清空字典
        itemset = get_itemset_topk(userId, topK)
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
    # item_voted_list = sorted(item_voted_dict.items(), key=lambda x:x[0])
    save_item_rated(item_voted_dict, conn)
    cursor.execute("CREATE INDEX co_idx ON co_rated(iid1,iid2)")
    cursor.execute("CREATE INDEX item_idx ON item_rated(iid)")
    conn.commit()
    # item_voted_list = []
    # for itemId, rated_num in item_voted_dict.items():
    #     item_voted_list.append((int(itemId), rated_num))
    # cursor.executemany("INSERT INTO item_rated VALUES(NULL, ?, ?)", item_voted_list)
    # conn.commit()
    # # item_voted_list = sorted(item_voted_dict.items(), key=lambda x:x[0])
    # # for item in item_voted_list:
    # #     itemId = item[0]
    # #     ratedNum = item[1]
    # #     cursor.execute("INSERT INTO item_rated VALUES(NULL, ?, ?)", (int(itemId), ratedNum))
    # #     conn.commit()

# calculate final similarity matrix
def calc_similarity(conn, cursor):
    cursor.execute(sim_table)
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
            sim_val = co_rated_num / (itemi_rated + itemj_rated - co_rated_num + 1) # 加1防止出现除以0
            sim_list.append((itemIdi, itemIdj, sim_val))
        if len(sim_list) > 0:
            cursor.executemany("INSERT INTO sim VALUES(NULL, ?, ?, ?)", sim_list)
            conn.commit()
        sim_list = []
    cursor.execute("CREATE INDEX sim_idx ON sim(iid1,iid2)")
    conn.commit()

# def preproc_item_item_sim(conn, cursor):
#     stat_rated_num(conn, cursor)
#     calc_similarity(conn, cursor)

def preproc_main():
    start_time = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
    db_file = "./data/kddcup2011_sim.db"
    m_conn, m_cursor = connect_db(db_file)
    stat_rated_num(m_conn, m_cursor)
    calc_similarity(m_conn, m_cursor)
    m_cursor.close()
    m_conn.close()
    end_time = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
    print 'start preprocess at ', start_time, ',end preprocess at ', end_time, '.'

if __name__ == '__main__':
    preproc_main()