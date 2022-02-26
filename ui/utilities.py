import sqlite3


def get_list(sql): 
    connection = sqlite3.connect("db/csdl.db")
    cursor = connection.execute(sql)
    list = []
    for row in cursor:
        list.append(row)
    connection.close()
    return list 