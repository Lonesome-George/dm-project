#coding=utf-8

import os
from base import *
from utils import proc_line

load_size = 5 # num of items that load each time

user_item_lines = '' # 'user_item.txt'文件内容
item_user_lines = '' # 'item_user.txt'文件内容
item_item_sim_lines = '' # 'item_item_sim.txt'文件内容
user_item_dict = {}
item_item_sim_dict = {}
item_user_dict = {}

# 从文件中的userId项开始加载size项
def load_itemset(userId, size):
    global user_item_lines
    if user_item_lines == '':
        user_item_file_in = os.path.join(store_dir, user_item_data)
        fi_user_item = open(user_item_file_in, 'r')
        user_item_lines = fi_user_item.readlines()
        fi_user_item.close()
    line_idx = userId - 1
    for idx in range(size):
        line_idx += 1
        if line_idx >= len(user_item_lines):
            break
        line = user_item_lines[line_idx]
        line = line.rstrip('\n')
        seg_list = proc_line(line, ':')
        uId = int(seg_list[0])
        user_item_dict[uId] = []
        seg_list = proc_line(seg_list[1], ';')
        for seg in seg_list:
            if seg == '':
                break
            sp_list = proc_line(seg, ',')
            itemId = int(sp_list[0])
            score = int(sp_list[1])
            user_item_dict[uId].append([itemId, score])

def load_all_itemset(): # MemoryError
    load_itemset(0, nUsers)

# 从第一位开始删除size项
def remove_entryset(entry_dict, size):
    total_num = 0
    for key in entry_dict.keys():
        entry_dict.pop(key)
        total_num += 1
        if total_num >= size:
            break

def get_itemset(userId):
    global user_item_dict
    if not user_item_dict.has_key(userId):# 在字典中没有发现该key
        if len(user_item_dict) >= max_size:
            user_item_dict = {}
        load_itemset(userId, load_size)
    return user_item_dict[userId]

def get_itemset_topk(userId, topK):
    itemset = get_itemset(userId)
    return topK_itemset(itemset, topK)

def topK_itemset(itemset, topK):
    itemset = sorted(itemset, key=lambda x:x[1], reverse=True)
    max_idx = len(itemset) - 1 # 列表的最大下标
    new_itemset = []
    for idx in range(topK):
        if idx < max_idx:
            new_itemset.append(itemset[idx])
        else:
            break
    return new_itemset

def load_userset(itemId, size):
    global item_user_lines
    if item_user_lines == '':
        item_user_file_in = os.path.join(store_dir, item_user_data)
        fi_item_user = open(item_user_file_in, 'r')
        item_user_lines = fi_item_user.readlines()
        fi_item_user.close()
    line_idx = itemId - 1
    for idx in range(size):
        line_idx += 1
        if line_idx >= len(item_user_lines):
            break
        line = item_user_lines[line_idx]
        line = line.rstrip('\n')
        seg_list = proc_line(line, ':')
        iId = int(seg_list[0])
        item_user_dict[iId] = []
        seg_list = proc_line(seg_list[1], ',')
        for seg in seg_list:
            if seg == '':
                break
            userId = int(seg)
            item_user_dict[iId].append(userId)

def get_userset(itemId):
    global item_user_dict
    if not item_user_dict.has_key(itemId):
        if len(item_user_dict) >= max_size:
            item_user_dict = {}
        load_userset(itemId, load_size)
    return item_user_dict[itemId]

def load_simset(itemId, size):
    global item_item_sim_lines
    if item_item_sim_lines == '':
        item_item_sim_file_in = os.path.join(store_dir, item_item_sim_data)
        fi_item_item_sim = open(item_item_sim_file_in, 'r')
        item_item_sim_lines = fi_item_item_sim.readlines()
        fi_item_item_sim.close()
    line_idx = itemId - 1
    for idx in range(size):
        line_idx += 1
        if line_idx >= len(item_item_sim_lines):
            break
        line = item_item_sim_lines[line_idx]
        line = line.rstrip('\n')
        if line == '':
            continue
        seg_list = proc_line(line, ':')
        iId1 = int(seg_list[0])
        item_item_sim_dict[iId1] = {}
        seg_list = proc_line(seg_list[1], ';')
        for seg in seg_list:
            if seg == '':
                break
            sp_list = proc_line(seg, ',')
            iId2 = int(sp_list[0])
            simVal = float(sp_list[1])
            item_item_sim_dict[iId1][iId2] = simVal

def get_simVal(itemId1, itemId2):
    itemId_min = min(itemId1, itemId2)
    itemId_max = max(itemId1, itemId2)
    global item_item_sim_dict
    if not item_item_sim_dict.has_key(itemId_min):
        if len(item_item_sim_dict) >= max_size:
            item_item_sim_dict = {}
        load_simset(itemId_min, load_size)
    if not item_item_sim_dict.has_key(itemId_min): # 加载结束依然没有该key,说明该项与Id大于它的所有项的相似度都为0
        return 0.0
    if not item_item_sim_dict[itemId_min].has_key(itemId_max):
        return 0.0
    return item_item_sim_dict[itemId_min][itemId_max]


if __name__ == '__main__':
    # itemset = get_itemset(0)
    itemset = get_itemset_topk(10000, 5)
    itemset = []