#coding=utf-8

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
item_item_sim_data = 'item_item_sim.txt'

co_rated_dir_prefix = 'co_rated' # co_rated dir prefix
co_rated_data_prefix = 'co_rated'
item_voted_data = 'item_voted'

nUsers = 249012
nItems = 296111

max_size  = 10000

# -------database--------
# item共现表
co_rated_table = "co_rated"
# item评分表
item_rated_table = "item_rated"
# 简单相似度表
simple_sim_table = "simple_sim"
# 余弦相似度表
cos_sim_table = "cos_sim"
# 相似度类型
sim_tables = [simple_sim_table, cos_sim_table]

ISOTIMEFORMAT = '%Y-%m-%d %X'


# log
import logging
import logging.config

LOG_FILENAME = 'logging.conf'
logging.config.fileConfig(LOG_FILENAME)
logger = logging.getLogger("TRAIN")