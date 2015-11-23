#coding=utf-8

from db_utils_v2 import connect_db

db_train = "./data/kddcup2011_train.db"
conn_train, cursor_train = connect_db(db_train)

# 查找跟item[iid]共现过的所有item
def get_co_rated_itemset(iid, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT iid2,co_rated_num FROM co_rated WHERE iid1=?", (iid,))
    records = cursor.fetchall()
    co_rated_itemset = []
    for record in records:
        co_rated_itemset.append(record)
    return co_rated_itemset

def get_co_rated_num(iid1, iid2, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT co_rated_num FROM co_rated WHERE iid1=? and iid2=?", (iid1,iid2))
    records = cursor.fetchall() # 这里可能返回多条记录
    co_rated_num = 0
    for record in records:
        co_rated_num += record[0]
    return co_rated_num

def update_co_rated_num(iid1, iid2, num, conn):
    cursor = conn.cursor()
    cursor.execute("UPDATE co_rated set co_rated_num=? WHERE iid1=? and iid2=?", (num,iid1,iid2))
    conn.commit()

def del_co_rated_num(iid1, iid2, conn):
    cursor = conn.cursor()
    cursor.execute("DELETE from co_rated where iid1=? and iid2=?", (iid1,iid2))
    conn.commit()

def get_rated_num(iid, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT rated_num FROM item_rated WHERE iid=?", (iid,))
    records = cursor.fetchall()
    rated_num = 0
    for record in records:
        rated_num += record[0]
    return rated_num

def get_itemset(uid):
    cursor = conn_train.cursor()
    cursor.execute("SELECT iid,score FROM train WHERE uid=?", (uid,))
    itemset = cursor.fetchall()
    return itemset

def get_itemset_topk(uid, topK):
    cursor = conn_train.cursor()
    cursor.execute("SELECT iid,score FROM train WHERE uid=?", (uid,))
    records = cursor.fetchall()
    record_list = sorted(records, key=lambda x:x[1], reverse=True)
    itemset = record_list[0:topK]
    return itemset

def get_userset(iid):
    cursor = conn_train.cursor()
    cursor.execute("SELECT uid,score FROM train WHERE iid=?", (iid,))
    userset = cursor.fetchall()
    return userset

def get_userset_topk(iid, topK):
    cursor = conn_train.cursor()
    cursor.execute("SELECT uid,score FROM train WHERE iid=?", (iid,))
    records = cursor.fetchall()
    record_list = sorted(records, key=lambda x:x[1], reverse=True)
    userset = record_list[0:topK]
    return userset

def get_simVal(iid1, iid2, sim_table, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT sim_val FROM %s WHERE iid1=? and iid2=?" % sim_table, (iid1,iid2))
    records = cursor.fetchall()
    sim_val = 0.0
    for record in records:
        sim_val += record[0]
    return sim_val
