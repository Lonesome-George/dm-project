#encoding=utf-8

import os
from preprocess import store_dir, user_item_data, item_user_data
from utils import proc_line

max_size  = 10000
half_size = max_size / 2

user_item_dict = {}
item_user_dict = {}

# 从文件中的userId项开始加载size项
def load_itemset(userId, size):
    user_item_file_in = os.path.join(store_dir, user_item_data)
    fi_user_item = open(user_item_file_in, 'r')
    start_line = userId
    idx = 0
    total_num = 0
    for line in fi_user_item:
        if idx >= start_line:
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
            total_num += 1
        idx += 1
        if total_num >= size:
            break
    fi_user_item.close()

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
    if not user_item_dict.has_key(userId):# 在字典中没有发现该key
        if len(user_item_dict) == 0:
            load_itemset(userId, max_size)
        else:
            # 删除half_size项
            remove_entryset(user_item_dict, half_size)
            # 从文件中读取half_size项
            load_itemset(userId, half_size)
    return user_item_dict[userId]

def get_itemset_topk(userId, topK):
    itemset = get_itemset(userId)
    itemset = sorted(itemset, key=lambda x:x[1], reverse=True)
    new_itemset = []
    for idx in range(topK):
        new_itemset.append(itemset[idx])
    return new_itemset

def load_userset(itemId, size):
    item_item_user_in = os.path.join(store_dir, item_user_data)
    fi_item_user = open(item_item_user_in, 'r')
    start_line = itemId
    idx = 0
    total_num = 0
    for line in fi_item_user:
        if idx >= start_line:
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
            total_num += 1
        idx += 1
        if total_num >= size:
            break
    fi_item_user.close()

def get_userset(itemId):
    if not item_user_dict.has_key(itemId):
        if len(item_user_dict) == 0:
            load_userset(itemId, max_size)
        else:
            # remove half_size entries
            remove_entryset(item_user_dict, half_size)
            # load half_size entries from file
            load_userset(itemId, half_size)
    return item_user_dict[itemId]


if __name__ == '__main__':
    itemset = get_itemset(0)
    itemset = get_itemset_topk(10000, 5)
    itemset = []