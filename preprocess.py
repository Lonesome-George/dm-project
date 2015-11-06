#encoding=utf-8

import os
import numpy as np
from utils import proc_line

source_dir = '../../KDDCup2011/dataset/Webscope_C15/ydata-ymusic-kddcup-2011-track2'
trackData = 'trackData2.txt'
albumData = 'albumData2.txt'
artistData = 'artistData2.txt'
genreData = 'genreData2.txt'
trainIdx = 'trainIdx2.txt'
testIdx = 'testIdx2.txt'
stats = 'stats2.txt'

store_dir = './data'
track_data = 'track.txt'
album_data = 'album.txt'
artist_of_track_data = 'artist_of_track.txt'
album_of_track_data  = 'album_of_track.txt'
trackset_bto_artist_data = 'trackset_bto_artist.txt' # bto means belong to
trackset_bto_album_data  = 'trackset_bto_album.txt'
itemset_user_voted_data = 'itemset_user_voted.txt'
userset_voted_item_data = 'userset_voted_item.txt'
user_item_data = 'user_item.txt'
item_user_data = 'item_user.txt'

nUsers = 249012
nItems = 296111
track_set = set()                 # [trackId, trackId, ...]
album_set = set()                 # [albumId, albumId, ...]
album_of_track_dict  = dict()     # {trackId:albumId, trackId:albumId, ...}
artist_of_track_dict = dict()     # {trackId:artistId, trackId:artistId, ...}
trackset_bto_album_dict  = dict() # {artistId:[albumId, albumId, ...], artistId:[albumId, albumId, ...], ...}
trackset_bto_artist_dict = dict() # {artistId:[trackId, trackId, ...], artistId:[trackId, trackId, ...], ...}
# itemset_user_voted_dict = dict()  # {userId:[itemId, itemId, ...], userId:[itemId, itemId, ...]}
# userset_voted_item_dict = dict()  # {itemId:[userId, userId, ...], itemId:[userId, userId, ...]}
user_item_array = 0   # 2-dim matrix, means items user voted. row denotes userId,col denotes itemId
item_user_array = 0   # 2-dim matrix, means users voted item. row denotes itemId,col denotes userId
# item_total_array = 0  # item that voted for total number

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
        # add_to_album_set(seg_list[0])
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
            score = int(seg_list[1])
            # if userCurRating == 1:
            #     user_item_array[userId] = [0 for x in range(userRatings)]
            # item = [itemId, score]
            # user_item_array[userId][userCurRating-1] = item
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
    item_item_array = [[] for x in range(nItems)]
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
            item_item_array[itemId].append(userId)
            if userCurRating >= userRatings:
                line_is_score = False
    for itemId in range(nItems):
        userset = item_item_array[itemId]
        string = str(itemId) + ':'
        for userId in userset:
            string += str(userId) + ','
        string += '\n'
        fo_item_user.write(string)
    fi_train.close()
    fo_item_user.close()

if __name__ == '__main__':
    # 创建存储目录
    if not os.path.isdir(store_dir):
        os.mkdir(store_dir)

    # 读取统计信息


    # 预处理track数据
    # preproc_track()

    # 预处理album数据
    # preproc_album()

    # 预处理train数据
    preproc_user_item()
    preproc_item_user()