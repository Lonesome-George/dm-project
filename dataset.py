#encoding=utf-8

import os
from preprocess import store_dir, user_item_data
from utils import proc_line

max_size  = 5000
half_size = 2500

user_item_dict = {}
item_user_dict = {}

def get_itemset_1(userId):
    if not user_item_dict.has_key(userId):# 在字典中没有发现该key
        # 删除half_size项
        total_num = 0
        for userId in user_item_dict.keys():
            user_item_dict.pop(userId)
            total_num += 1
            if total_num >= half_size:
                break
        # 从文件中读取half_size项
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
            if total_num >= half_size:
                break
        fi_user_item.close()
    return user_item_dict[userId]

def get_itemset_2(userId, topK):
    itemset = get_itemset_1(userId)
    # itemset = itemset.sort(key=lambda x:x[1], reverse=True)
    new_itemset = []
    sorted(itemset, key=lambda x:x[1], reverse=True)
    for idx in range(topK):
        new_itemset.append(itemset[idx])
    return new_itemset

def item(itemId):
    pass

def user(userId):
    pass


if __name__ == '__main__':
    itemset = get_itemset_1(0)
    itemset = get_itemset_2(10000, 5)
    itemset = []