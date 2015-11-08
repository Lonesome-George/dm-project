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

co_rated_temp_dir = 'co_rated_sim' # temp dir for storing co_rated num
co_rated_data_prefix = 'co_rated'
item_voted_data = 'item_voted'

nUsers = 249012
nItems = 296111

max_size  = 5000
half_size = max_size / 2