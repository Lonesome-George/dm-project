# -*- coding: utf-8 -*-

import sqlite3


def connect_db(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    return conn, cursor


def process_train(conn, cursor):
    train_file = "./data/trainIdx2.txt"

    cursor.execute("CREATE TABLE IF NOT EXISTS user (id integer PRIMARY KEY autoincrement,\
        uid integer,type integer)")
    cursor.execute("CREATE TABLE IF NOT EXISTS train (id integer PRIMARY KEY autoincrement,\
        uid integer,iid integer,score integer)")
    conn.commit()

    fi = file(train_file, 'r')
    while True:
        u_line = fi.readline().strip()
        if len(u_line) == 0:
            break
        user, num = u_line.split('|')
        cursor.execute("INSERT INTO user VALUES(NULL, ?, ?)", (int(user), 0))
        items = []
        for x in xrange(int(num)):
            item_line = fi.readline().strip()
            item_id, score = item_line.split('\t')
            items.append(tuple([int(user), int(item_id), int(score)]))
        cursor.executemany("INSERT INTO train VALUES(NULL, ?, ?, ?)", items)
        conn.commit()


def process_track(conn, cursor):
    track_file = "./data/trackData2.txt"

    cursor.execute("CREATE TABLE IF NOT EXISTS track (id integer PRIMARY KEY autoincrement,\
        tid integer,alb_id integer,art_id integer)")
    cursor.execute("CREATE TABLE IF NOT EXISTS t_genre (id integer PRIMARY KEY autoincrement,\
        tid integer,gid integer)")
    conn.commit()

    fi = file(track_file, 'r')
    while True:
        line = fi.readline().strip()
        if len(line) == 0:
            break
        cont = line.split('|')
        # change string value 'None' to integer -1
        cont[1] = -1 if cont[1] == 'None' else cont[1]
        cont[2] = -1 if cont[2] == 'None' else cont[2]
        cursor.execute("INSERT INTO track VALUES(NULL, ?, ?, ?)", (int(cont[0]), int(cont[1]), int(cont[2])))
        genres = []
        for x in xrange(3, len(cont)):
            genres.append(tuple([int(cont[0]), int(cont[x])]))
        cursor.executemany("INSERT INTO t_genre VALUES(NULL, ?, ?)", genres)
        conn.commit()


def process_album(conn, cursor):
    track_file = "./data/albumData2.txt"

    cursor.execute("CREATE TABLE IF NOT EXISTS album (id integer PRIMARY KEY autoincrement,\
        alb_id integer,art_id integer)")
    cursor.execute("CREATE TABLE IF NOT EXISTS a_genre (id integer PRIMARY KEY autoincrement,\
        alb_id integer,gid integer)")
    conn.commit()

    fi = file(track_file, 'r')
    while True:
        line = fi.readline().strip()
        if len(line) == 0:
            break
        cont = line.split('|')
        cont[1] = -1 if cont[1]=='None' else cont[1]
        cursor.execute("INSERT INTO album VALUES(NULL, ?, ?)", (int(cont[0]), int(cont[1])))
        genres = []
        for x in xrange(2, len(cont)):
            genres.append(tuple([int(cont[0]), int(cont[x])]))
        cursor.executemany("INSERT INTO a_genre VALUES(NULL, ?, ?)", genres)
        conn.commit()


if __name__ == '__main__':
    db_file = "./data/kddcup2011_album.db"
    m_conn, m_cursor = connect_db(db_file)

    # process_train(conn, cursor)
    # process_track(m_conn, m_cursor)
    # process_album(m_conn, m_cursor)

    # m_cursor.execute("SELECT count(1) FROM user")
    # m_cursor.execute("SELECT count(1) FROM train")
    # print m_cursor.fetchone()

    m_cursor.close()
    m_conn.close()

    print 'Done!'
