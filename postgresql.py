from psycopg2 import connect, extras
import os
import config


conText = f"\
    host={os.environ['DB_HOST']} \
    port={os.environ['DB_PORT']} \
    dbname={os.environ['DB_NAME']} \
    user={os.environ['DB_USER']} \
    password={os.environ['DB_PASSWORD']}"
connection = connect(conText)
cur = connection.cursor(cursor_factory=extras.DictCursor)


def delete_scriptinfo():
    sql = "delete from script_info"
    cur.execute(sql)
    connection.commit()


def insert_scriptinfo(info):
    columns = info.keys()
    sql = f"insert into\
        script_info({', '.join(columns)})\
        values(\
            '{info['id']}', \
            '{info['script']}', \
            {info['fontsize']}, \
            {info['starttime']}, \
            {info['endtime']}, \
            '{info['color']}', \
            '{info['xymode']}');"
    cur.execute(sql)
    connection.commit()


def select_scriptinfo():
    sql = "select * from script_info"
    cur.execute(sql)
    result = cur.fetchall()
    return [dict(i) for i in result]


def select_accountinfo():
    sql = "select * from account_info where id = 'gaccount'"
    cur.execute(sql)
    result = cur.fetchone()
    return dict(result)
