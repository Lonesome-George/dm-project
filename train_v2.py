#coding=utf-8

#迭代训练调参

import logging
import logging.config
import time
from base import store_dir, sim_tables, ISOTIMEFORMAT
from utils import find_filename
from db_utils_v2 import connect_db
from preprocess_v2 import preproc_main
from test_prec_v2 import test_prec

logger = None

def init_log():
    global logger
    LOG_FILENAME = 'logging.conf'
    logging.config.fileConfig(LOG_FILENAME)
    logger = logging.getLogger("TRAIN_V2")

if __name__ == '__main__':
    init_log()
    trainsizes = [10000, 50000, 100000, 300000]
    topKs = [50, 75, 100]
    db_prefix = "kddcup2011_sim.db"
    for trainsize in trainsizes:
        for topK in topKs:
            db_sim_file = find_filename(store_dir, '%s.ts%d.tk%d' %(db_prefix, trainsize, topK))
            db_conn, db_cursor = connect_db(db_sim_file)
            logger.info('trainsize: %d,topK: %d.' %(trainsize, topK))
            logger.info('Start preprocess')
            preproc_main(trainsize, topK, db_conn, db_cursor)
            end_time = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
            logger.info('End preprocess.')
            logger.info('Start test.')
            prec = test_prec(sim_tables[0], db_conn)
            logger.info('End test(precision: %f).' % prec)
