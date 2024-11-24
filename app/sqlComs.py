


def connect():
    print("s")
    conn = mariadb.connect(
        host='localhost',
        user='root',
        password='a',
        port=3306,
        database='baseball'
    )

    return conn

def getRowFromSQL(sql):
    conn = connect()

    cur = conn.cursor()

    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows


class SQLRows:
    def __init__(self):
        self.sql = None
        self.rows = None




obj = SQLRows()