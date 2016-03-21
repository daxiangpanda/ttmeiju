#!/usr/bin/env python
# encoding: utf-8

import cPickle as pickle
import sqlite3
import os
import re


def get_conn(path):
    '''获取到数据库的连接对象，参数为数据库文件的绝对路径
    如果传递的参数是存在，并且是文件，那么就返回硬盘上面改
    路径下的数据库文件的连接对象；否则，返回内存中的数据接
    连接对象'''
    conn = sqlite3.connect(path)
    if os.path.exists(path) and os.path.isfile(path):
        print('硬盘上面:[{}]'.format(path))
        return conn
    else:
        conn = None
        print('内存上面:[:memory:]')
        return sqlite3.connect(':memory:')


def get_cursor(conn):
    '''该方法是获取数据库的游标对象，参数为数据库的连接对象
    如果数据库的连接对象不为None，则返回数据库连接对象所创
    建的游标对象；否则返回一个游标对象，该对象是内存中数据
    库连接对象所创建的游标对象'''
    if conn is not None:
        return conn.cursor()
    else:
        return get_conn('').cursor()


def close_all(conn, cu):
    '''关闭数据库游标对象和数据库连接对象'''
    try:
        if cu is not None:
            cu.close()
    finally:
        if cu is not None:
            cu.close()


def create_table(conn,name_table):
    '''创建数据库表'''
    print name_table
    if name_table is not None and name_table != '':
        cu = get_cursor(conn)
        print('创建表%s'.decode('utf-8')%name_table)
        sql = '''CREATE TABLE '%s'(
                          `name` varchar(100) NOT NULL,
                          `link` varchar(500) DEFAULT NULL,
                          `size` varchar(100) DEFAULT NULL,
                          `format` varchar(100) DEFAULT NULL
                        )''' %name_table
        print sql
        cu.execute(sql)
        conn.commit()
        print('创建数据库表%s成功!'.decode('utf-8')%name_table)
        close_all(conn, cu)
    else:
        print('the [{}] is empty or equal None!'.format(sql))


def save(conn,table,data):
    '''插入数据'''
    conn.text_factory = str
    sql = '''INSERT INTO %s values (?, ?, ?, ?)'''%table
    print sql
    if sql is not None and sql != '':
        if data is not None:
            cu = get_cursor(conn)
            for d in data:
                # if SHOW_SQL:
                #     print('执行sql:[{}],参数:[{}]'.format(sql, d))
                cu.execute(sql, d)
                conn.commit()
            close_all(conn, cu)
    else:
        print('the [{}] is empty or equal None!'.format(sql))


def database_isexist(conn,name_table):
    sql = "SELECT * FROM sqlite_master WHERE type='table'"
    cu = get_cursor(conn)
    return name_table in [i[1] for i in cu.execute(sql).fetchall()]


def tochinese(num):
    _MAPPING = (u'零', u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九', )
    res = ''
    for i in list(str(num)):
        res+=_MAPPING[int(i)]
    return res


def tosql(name):
    print 1
    print name
    data = pickle.load(file(name,'r'))
    name = name.split('.')[0]
    num = re.findall('^[0-9]+',name)
    if len(num) == 1:
        name = tochinese(num[0])+name.lstrip(num[0])
    # print database_isexist(conn,'num24小时'.decode('utf-8'))
    print database_isexist(conn,name)
    if not database_isexist(conn,name):
        create_table(conn,name)
    save(conn,name,data)


SHOW_SQL = 1
path = 'database_res.db'
conn = get_conn(path)
# create_table(conn,u'无耻1')
database_isexist(conn,'s')

if __name__ == '__main__':
    tosql(u'1无耻家庭.pick')
with open(u'1无耻家庭.pick','r') as f:
    result = f.read()

# for i in pickle.loads(result):
#     name = i[0]
#     link = ''
#     for ii in i[1]:
#         link+=ii[0]+ii[1]
#     size = i[2]
#     format = i[3]
#     print name
#     print link
#     print size
#     print format
