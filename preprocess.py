#coding=utf-8

from __future__ import division
import os
import math
from base import *
from utils import proc_line, find_filename
from dataset import get_itemset, get_itemset_topk, topK_itemset
from itemcf_model import sim, topK

track_set = set()                 # [trackId, trackId, ...]
album_set = set()                 # [albumId, albumId, ...]
album_of_track_dict  = dict()     # {trackId:albumId, trackId:albumId, ...}
artist_of_track_dict = dict()     # {trackId:artistId, trackId:artistId, ...}
trackset_bto_album_dict  = dict() # {artistId:[albumId, albumId, ...], artistId:[albumId, albumId, ...], ...}
trackset_bto_artist_dict = dict() # {artistId:[trackId, trackId, ...], artistId:[trackId, trackId, ...], ...}
user_item_array = 0     # 2-dim matrix, means items that user voted; row denotes userId,col denotes itemId
item_user_array = 0     # 2-dim matrix, means users that voted item; row denotes itemId,col denotes userId
item_item_sim_array = 0 # 2-dim matrix, means item-item similarity.

def add_to_track_set(trackId):
    track_set.add(trackId)

def preproc_track():
    trackData_file_in = os.path.join(source_dir, trackData)
    trackData_file_out = os.path.join(store_dir, track_data)
    album_of_track_file_out = os.path.join(store_dir, album_of_track_data)
    artist_of_track_file_out = os.path.join(store_dir, artist_of_track_data)
    trackset_bto_album_file_out = os.path.join(store_dir, trackset_bto_album_data)
    trackset_bto_artist_file_out = os.path.join(store_dir, trackset_bto_artist_data)

    fi_track = open(trackData_file_in, 'r')
    fo_track = open(trackData_file_out, 'w')
    fo_album_of_track = open(album_of_track_file_out, 'w')
    fo_artist_of_track = open(artist_of_track_file_out, 'w')
    for line in fi_track:
        line = line.rstrip('\n')
        seg_list = proc_line(line, '|')
        # add_to_track_set(seg_list[0])
        trackId = seg_list[0]
        albumId = seg_list[1]
        artistId = seg_list[2]
        str1 = trackId + '\n'
        str2 = trackId + '|' + albumId + '\n'
        str3 = trackId + '|' + artistId + '\n'
        fo_track.write(str1)
        fo_album_of_track.write(str2)
        fo_artist_of_track.write(str3)
        if not trackset_bto_album_dict.has_key(albumId):
            trackset_bto_album_dict[albumId] = []
        trackset_bto_album_dict[albumId].append(trackId)
        if not trackset_bto_artist_dict.has_key(artistId):
            trackset_bto_artist_dict[artistId] = []
        trackset_bto_artist_dict[artistId].append(trackId)
    fi_track.close()
    fo_track.close()
    fo_album_of_track.close()
    fo_artist_of_track.close()

    fo_trackset_bto_album = open(trackset_bto_album_file_out, 'w')
    for albumId in trackset_bto_album_dict:
        string = albumId + ':'
        trackset = trackset_bto_album_dict[albumId]
        for trackId in trackset:
            string += trackId + ','
        string += '\n'
        fo_trackset_bto_album.write(string)
    fo_trackset_bto_album.close()

    fo_trackset_bto_artist = open(trackset_bto_artist_file_out, 'w')
    for artistId in trackset_bto_artist_dict:
        string = artistId + ':'
        trackset = trackset_bto_artist_dict[artistId]
        for trackId in trackset:
            string += trackId + ','
        string += '\n'
        fo_trackset_bto_artist.write(string)
    fo_trackset_bto_artist.close()

def preproc_album():
    albumData_file_in = os.path.join(source_dir, albumData)
    albumData_file_out = os.path.join(store_dir, album_data)
    if os.path.isfile(albumData_file_out):
        return
    fi_album = open(albumData_file_in, 'r')
    fo_album = open(albumData_file_out, 'w')
    for line in fi_album:
        line = line.rstrip('\n')
        seg_list = proc_line(line, '|')
        string = seg_list[0] + '\n'
        fo_album.write(string)
    fi_album.close()
    fo_album.close()

def preproc_user_item():
    trainIdx_file_in = os.path.join(source_dir, trainIdx)
    user_item_file_out = os.path.join(store_dir, user_item_data)
    if os.path.isfile(user_item_file_out):
        return
    # user_item_array = [[] for x in range(nUsers)]
    itemset = []
    fi_train = open(trainIdx_file_in, 'r')
    fo_user_item = open(user_item_file_out, 'w')
    lastUserId = -1 # 前一个user的Id值,userId并不是连续的
    userId = 0
    userRatings = 0   # 用户的总评分数目
    userCurRating = 0 # 当前行是用户的第几个评分
    line_is_score = False
    for line in fi_train:
        line = line.rstrip('\n')
        if not line_is_score:
            seg_list = proc_line(line, '|')
            userId = int(seg_list[0])
            if (lastUserId + 1) != userId: # userId遇到跳跃,为不存在的userId插入空行,方便以后根据userId快速定位文件行
                for idx in range(lastUserId+1, userId):
                    string = str(idx) + ':;\n'
                    fo_user_item.write(string)
            lastUserId = userId
            userRatings = int(seg_list[1])
            userCurRating = 0
            line_is_score = True
        else:
            userCurRating += 1
            seg_list = proc_line(line, '\t')
            itemId = int(seg_list[0])
            score = int(seg_list[1])
            if userCurRating == 1:
                itemset = []
            item = [itemId, score]
            itemset.append(item)
            if userCurRating >= userRatings:
                string = str(userId) + ':'
                for item in itemset:
                    string += str(item[0]) + ',' + str(item[1]) + ';'
                string += '\n'
                fo_user_item.write(string)
                line_is_score = False
    # for userId in range(nUsers):
    #     itemset = user_item_array[userId]
    #     string = str(userId) + ':'
    #     for item in itemset:
    #         string += str(item[0]) + ',' + str(item[1]) + ';'
    #     string += '\n'
    #     fo_user_item.write(string)
    fi_train.close()
    fo_user_item.close()

def preproc_item_user():
    trainIdx_file_in = os.path.join(source_dir, trainIdx)
    item_user_file_out = os.path.join(store_dir, item_user_data)
    if os.path.isfile(item_user_file_out):
        return
    item_user_array = [[] for x in range(nItems)]
    fi_train = open(trainIdx_file_in, 'r')
    fo_item_user = open(item_user_file_out, 'w')
    userId = 0
    userRatings = 0   # 用户的总评分数目
    userCurRating = 0 # 当前行是用户的第几个评分
    line_is_score = False
    for line in fi_train:
        line = line.rstrip('\n')
        if not line_is_score:
            seg_list = proc_line(line, '|')
            userId = int(seg_list[0])
            userRatings = int(seg_list[1])
            userCurRating = 0
            line_is_score = True
        else:
            userCurRating += 1
            seg_list = proc_line(line, '\t')
            itemId = int(seg_list[0])
            item_user_array[itemId].append(userId)
            if userCurRating >= userRatings:
                line_is_score = False
    for itemId in range(nItems):
        userset = item_user_array[itemId]
        string = str(itemId) + ':'
        for userId in userset:
            string += str(userId) + ','
        string += '\n'
        fo_item_user.write(string)
    fi_train.close()
    fo_item_user.close()

# 统计共现矩阵
def stat_co_rated_num():
    co_rated_dir = os.path.join(store_dir, co_rated_temp_dir)
    if not os.path.isdir(co_rated_dir):
        os.mkdir(co_rated_dir)
    if os.listdir(co_rated_dir):
        print 'Directory \'%s\' not empty.' % co_rated_dir
        return
    # calculate co-rated users between items
    co_rated_dict = dict()   # item-item co-rated matrix
    item_voted_dict = dict() # number that each item was voted
    for userId in range(nUsers):
        if not userId % 2000:
            print 'current userId: %d' % userId
        if len(co_rated_dict) > max_size: # 为了防止内存溢出,将这部分数据写入文件
            co_rated_list = sorted(co_rated_dict.items(), key=lambda x:x[0]) # 按itemId值排序,方便查找
            filename = find_filename(co_rated_dir, co_rated_data_prefix)
            fo_co_rated = open(filename, 'w')
            for item in co_rated_list:
                itemIdi = item[0]
                related_items = item[1]
                string = str(itemIdi) + ':'
                for itemIdj, co_rated_num in related_items.items():
                    string += str(itemIdj) + ',' + str(co_rated_num) + ';'
                string += '\n'
                fo_co_rated.write(string)
            fo_co_rated.close()
            co_rated_dict = {} # 清空字典
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
    item_voted_file_out = os.path.join(co_rated_dir, item_voted_data)
    fo_item_voted = open(item_voted_file_out, 'w')
    item_voted_list = sorted(item_voted_dict.items(), key=lambda x:x[0])
    string = ''
    for item in item_voted_list:
        itemId = item[0]
        votedNum = item[1]
        string += str(itemId) + ':' + str(votedNum) + ';'
    string += '\n'
    fo_item_voted.write(string)
    fo_item_voted.close()

def calc_similarity(co_rated_dir):
    item_item_sim_file_out = os.path.join(store_dir, item_item_sim_data)
    if os.path.isfile(item_item_sim_file_out):
        print 'File \'%s\' exists.' % item_item_sim_file_out
        return
    fo_item_item_sim = open(item_item_sim_file_out, 'w') # for saving similarity
    # calculate final similarity matrix item_item_sim_dict
    # 假设统计数据一共保存在n个文件中,则按itemId的顺序每次计算max_size个item与其他item的相似度并写入文件
    co_rated_files = []
    for parent,dirnames,filenames in os.walk(co_rated_dir):
        for filename in filenames:
            if filename.startswith(co_rated_data_prefix): # 忽略不以指定prefix为前缀的文件
                co_rated_files.append(os.path.join(parent, filename))

    # 读取item的voted用户数
    item_voted_dict = {}
    item_voted_file_in = os.path.join(co_rated_dir, item_voted_data)
    fi_item_voted = open(item_voted_file_in, 'r')
    for line in fi_item_voted:
        line = line.rstrip('\n')
        seg_list = proc_line(line, ';')
        for seg in seg_list:
            if seg == '':
                break
            sp_list = proc_line(seg, ':')
            itemId = int(sp_list[0])
            votedNum = int(sp_list[1])
            item_voted_dict[itemId] = votedNum
    fi_item_voted.close()

    # 遍历文件,按区间每次读取max_size个item
    co_rated_dict = {}
    loop = 0 # 循环次数
    while True:
        print 'loop %d' % loop
        startId = max_size * loop
        if startId >= nItems: # 读取结束
            break
        endId = max_size * (loop + 1) - 1
        for filename in co_rated_files:
            f = open(filename, 'r')
            for line in f:
                seg_list = proc_line(line, ':')
                itemId1 = int(seg_list[0])
                if itemId1 < startId:
                    continue
                elif itemId1 > endId:
                    break
                else:
                    if not co_rated_dict.has_key(itemId1):
                        co_rated_dict[itemId1] = {}
                    seg_list = proc_line(seg_list[1].rstrip('\n'), ';')
                    for seg in seg_list:
                        if seg == '':
                            break
                        sp_list = proc_line(seg, ',')
                        itemId2 = int(sp_list[0])
                        co_rated_num = int(sp_list[1])
                        if not co_rated_dict[itemId1].has_key(itemId2):
                            co_rated_dict[itemId1][itemId2] = 0
                        co_rated_dict[itemId1][itemId2] += co_rated_num
            f.close()
        # 将这部分数据写入文件
        item_item_sim_dict = {}
        for itemIdi, related_items in co_rated_dict.items():
            max_sim = 0.0
            for itemIdj, co_rated_num in related_items.items():
                if not item_item_sim_dict.has_key(itemIdi):
                    item_item_sim_dict[itemIdi] = {}
                item_item_sim_dict[itemIdi][itemIdj] = co_rated_num / math.sqrt(item_voted_dict[itemIdi] * item_voted_dict[itemIdj])
                if item_item_sim_dict[itemIdi][itemIdj] > max_sim:
                    max_sim = item_item_sim_dict[itemIdi][itemIdj]
            # normalize
            for itemIdj in item_item_sim_dict[itemIdi]:
                item_item_sim_dict[itemIdi][itemIdj] /= max_sim

        item_item_sim_list = sorted(item_item_sim_dict.items(), key=lambda x:x[0])
        last_itemId = startId - 1
        for itemi in item_item_sim_list:
            itemIdi = itemi[0]
            related_items = itemi[1]
            if itemIdi - last_itemId > 1:
                for idx in range(last_itemId + 1, itemIdi):
                    fo_item_item_sim.write('\n') # 补空行
            last_itemId = itemIdi
            string = str(itemIdi) + ':'
            related_items_list = sorted(related_items.items(), key=lambda x:x[0])# 按itemId排序
            for itemj in related_items_list:
                itemIdj = itemj[0]
                sim_val = itemj[1]
                if itemIdj > itemIdi: # 根据对称性,只记录上三角部分
                    string += '%d,%.4f;' % (itemIdj, sim_val)
            string += '\n'
            fo_item_item_sim.write(string)
        for idx in range(last_itemId + 1, endId + 1):
            fo_item_item_sim.write('\n') # 补空行

        # 清空字典并进入下一轮
        co_rated_dict = {}
        item_item_sim_dict = {}
        loop += 1
    fo_item_item_sim.close()

def preproc_item_item_sim():
    co_rated_dir = os.path.join(store_dir, co_rated_temp_dir)
    stat_co_rated_num(co_rated_dir)
    calc_similarity(co_rated_dir)

# save co_rated dict to a file
def save_co_rated_dict(co_rated_dir, co_rated_dict):
    co_rated_list = sorted(co_rated_dict.items(), key=lambda x:x[0]) # 按itemId值排序,方便查找
    filename = find_filename(co_rated_dir, co_rated_data_prefix)
    fo_co_rated = open(filename, 'w')
    for item in co_rated_list:
        itemIdi = item[0]
        related_items = item[1]
        string = str(itemIdi) + ':'
        for itemIdj, co_rated_num in related_items.items():
            string += str(itemIdj) + ',' + str(co_rated_num) + ';'
        string += '\n'
        fo_co_rated.write(string)
    fo_co_rated.close()

# stat co_rated items
def stat_co_rated_item(itemset, item_voted_dict, co_rated_dict):
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

def save_item_voted(co_rated_dir, item_voted_dict):
    item_voted_file_out = os.path.join(co_rated_dir, item_voted_data)
    fo_item_voted = open(item_voted_file_out, 'w')
    item_voted_list = sorted(item_voted_dict.items(), key=lambda x:x[0])
    string = ''
    for item in item_voted_list:
        itemId = item[0]
        votedNum = item[1]
        string += str(itemId) + ':' + str(votedNum) + ';'
    string += '\n'
    fo_item_voted.write(string)
    fo_item_voted.close()

# 统计共现矩阵,忽略评分超过1000条的用户,对剩余的用户只取前50条评分进行计算
def stat_co_rated_num2(co_rated_dir):
    if not os.path.isdir(co_rated_dir):
        os.mkdir(co_rated_dir)
    if os.listdir(co_rated_dir):
        print 'Directory \'%s\' not empty.' % co_rated_dir
        return
    # calculate co-rated users between items
    co_rated_dict = dict()   # item-item co-rated matrix
    item_voted_dict = dict() # number that each item was voted
    for userId in range(nUsers):
        if not userId % 2000:
            print 'current userId: %d' % userId
        if len(co_rated_dict) > max_size: # 为了防止内存溢出,将这部分数据写入文件
            save_co_rated_dict(co_rated_dir, co_rated_dict)
            co_rated_dict = {} # 清空字典
        itemset = get_itemset(userId)
        if len(itemset) > 1000:
            continue
        itemset = topK_itemset(itemset, topK)
        # 统计共现项目
        stat_co_rated_item(itemset, co_rated_dict, item_voted_dict)
    save_item_voted(co_rated_dir, item_voted_dict)
    item_voted_dict = {}

def preproc_item_item_sim2():
    co_rated_dir = os.path.join(store_dir, co_rated_temp_dir + '2')
    stat_co_rated_num2(co_rated_dir)
    calc_similarity(co_rated_dir)


if __name__ == '__main__':
    # 创建存储目录
    if not os.path.isdir(store_dir):
        os.mkdir(store_dir)

    # 预处理track数据
    # preproc_track()

    # 预处理album数据
    # preproc_album()

    # 预处理train数据
    preproc_user_item()
    preproc_item_user()

    # 预处理生成并保存item-item的相似度
    # preproc_item_item_sim()

    preproc_item_item_sim2()