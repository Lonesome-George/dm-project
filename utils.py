#coding=utf-8

import os

def proc_line(line, sep):
    seg_list = line.split(sep)
    return seg_list

def find_filename(dir, prefix): # 返回一个可用的文件名
    filename_prefix = os.path.join(dir, prefix)
    filename = ''
    suffix = 0
    while True:
        suffix += 1
        filename = filename_prefix + '_' + str(suffix)
        if not os.path.isfile(filename):
            break
    return filename

def find_dirname(dir, prefix): # 返回一个可用的目录名
    dirname_prefix = os.path.join(dir, prefix)
    dirname = ''
    suffix = 0
    while True:
        suffix += 1
        dirname = dirname_prefix + '_' + str(suffix)
        if not os.path.isdir(dirname):
            break
    return dirname