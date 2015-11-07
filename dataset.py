#coding=utf-8

import os
from base import store_dir, user_item_data, item_user_data, item_item_sim_data
from utils import proc_line

max_size  = 300000
half_size = max_size / 2
load_size = 50 # num of items that load every time

user_item_contents = '' # 'user_item.txt'文件内容
item_user_contents = '' # 'item_user.txt'文件内容
item_item_sim_contents = '' # 'item_item_sim.txt'文件内容
user_item_dict = {}
item_user_dict = {}
item_item_sim_dict = {}

# 从文件中的userId项开始加载size项
def load_itemset(userId, size):
    global user_item_contents
    if user_item_contents == '':
        user_item_file_in = os.path.join(store_dir, user_item_data)
        fi_user_item = open(user_item_file_in, 'r')
        user_item_contents = fi_user_item.readlines()
        fi_user_item.close()
    start_line = userId
    idx = 0
    total_num = 0
    # lines = fi_user_item.readlines()
    for idx in range(size):
        line_idx = idx + start_line
        if line_idx >= len(user_item_contents):
            break
        content = user_item_contents[line_idx]
        content = content.rstrip('\n')
        seg_list = proc_line(content, ':')
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
    # for content in fi_user_item:
    #     if idx >= start_line:
    #         content = content.rstrip('\n')
    #         seg_list = proc_line(content, ':')
    #         uId = int(seg_list[0])
    #         user_item_dict[uId] = []
    #         seg_list = proc_line(seg_list[1], ';')
    #         for seg in seg_list:
    #             if seg == '':
    #                 break
    #             sp_list = proc_line(seg, ',')
    #             itemId = int(sp_list[0])
    #             score = int(sp_list[1])
    #             user_item_dict[uId].append([itemId, score])
    #         total_num += 1
    #     idx += 1
    #     if total_num >= size:
    #         break
    # fi_user_item.close()

# 从第一位开始删除size项
def remove_entryset(entry_dict, size):
    total_num = 0
    for key in entry_dict.keys():
        entry_dict.pop(key)
        total_num += 1
        if total_num >= size:
            break

# def remove_itemset(size):
#     total_num = 0
#     for userId in user_item_dict.keys():
#         user_item_dict.pop(userId)
#         total_num += 1
#         if total_num >= size:
#             break

def get_itemset(userId):
    global user_item_dict
    if not user_item_dict.has_key(userId):# 在字典中没有发现该key
        # if len(user_item_dict) == 0:
        #     load_itemset(userId, max_size)
        # else:
        #     # remove half_size entries
        #     remove_entryset(user_item_dict, load_size)
        #     # load half_size entries from file
        #     load_itemset(userId, load_size)
        if len(user_item_dict) >= max_size:
            user_item_dict = {}
        load_itemset(userId, load_size)
    return user_item_dict[userId]

def get_itemset_topk(userId, topK):
    itemset = get_itemset(userId)
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
    global item_user_contents
    if item_user_contents == '':
        item_user_file_in = os.path.join(store_dir, item_user_data)
        fi_item_user = open(item_user_file_in, 'r')
        item_user_contents = fi_item_user.readlines()
        fi_item_user.close()
    start_line = itemId
    idx = 0
    total_num = 0
    # lines = fi_item_user.readlines()
    for idx in range(size):
        line_idx = idx + start_line
        if line_idx >= len(item_user_contents):
            break
        content = item_user_contents[line_idx]
        content = content.rstrip('\n')
        seg_list = proc_line(content, ':')
        iId = int(seg_list[0])
        item_user_dict[iId] = []
        seg_list = proc_line(seg_list[1], ',')
        for seg in seg_list:
            if seg == '':
                break
            userId = int(seg)
            item_user_dict[iId].append(userId)
    # for content in fi_item_user:
    #     if idx >= start_line:
    #         content = content.rstrip('\n')
    #         seg_list = proc_line(content, ':')
    #         iId = int(seg_list[0])
    #         item_user_dict[iId] = []
    #         seg_list = proc_line(seg_list[1], ',')
    #         for seg in seg_list:
    #             if seg == '':
    #                 break
    #             userId = int(seg)
    #             item_user_dict[iId].append(userId)
    #         total_num += 1
    #     idx += 1
    #     if total_num >= size:
    #         break
    # fi_item_user.close()

def get_userset(itemId):
    global item_user_dict
    if not item_user_dict.has_key(itemId):
        # if len(item_user_dict) == 0:
        #     load_userset(itemId, max_size)
        # else:
        #     # remove half_size entries
        #     remove_entryset(item_user_dict, load_size)
        #     # load half_size entries from file
        #     load_userset(itemId, load_size)
        if len(item_user_dict) >= max_size:
            item_user_dict = {}
        load_userset(itemId, load_size)
    return item_user_dict[itemId]

def load_simset(itemId, size):
    global item_item_sim_contents
    if item_item_sim_contents == '':
        item_item_sim_file_in = os.path.join(store_dir, item_item_sim_data)
        fi_item_item_sim = open(item_item_sim_file_in, 'r')
        item_item_sim_contents = fi_item_item_sim.readlines()
        fi_item_item_sim.close()
    start_line = itemId
    for idx in range(size):
        line_idx = idx + start_line
        if line_idx >= len(item_item_sim_contents):
            break
        content = item_item_sim_contents[line_idx]
        content = content.rstrip('\n')
        seg_list = proc_line(content, ':')
        iId1 = int(seg_list[0])
        item_item_sim_dict[iId1] = {}
        seg_list = proc_line(seg_list[1], ';')
        for seg in seg_list:
            if seg == '':
                break
            sp_list = proc_line(seg, ',')
            iId2 = int(sp_list[0])
            simVal = float(sp_list[1])
            user_item_dict[iId1][iId2] = simVal

def get_simVal(itemId1, itemId2):
    itemId_min = min(itemId1, itemId2)
    itemId_max = max(itemId1, itemId2)
    global item_item_sim_dict
    if not item_item_sim_dict.has_key(itemId_min):
        if len(item_item_sim_dict) >= max_size:
            item_item_sim_dict = {}
        load_simset(itemId_min, load_size)
    idx = itemId_max - itemId_min - 1
    if not item_item_sim_dict[itemId_min].has_key(idx):
        return 0.0
    return item_item_sim_dict[itemId_min][idx]


if __name__ == '__main__':
    itemset = get_itemset(0)
    itemset = get_itemset_topk(10000, 5)
    itemset = []