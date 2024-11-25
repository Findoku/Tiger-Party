from app import app
from app import DatabaseConnection
import mariadb


def connect():
    print("s")
    maria = DatabaseConnection
    conn = mariadb.connect(
        user=maria.mysql["user"],
        password=maria.mysql["password"],
        host=maria.mysql["location"],
        port=3306,
        database=maria.mysql["database"]
    )

    return conn
def executeInsert(sql):
    conn = connect()

    cur = conn.cursor()

    cur.execute(sql)
    conn.commit()
    conn.close()



def getRowFromSQL(sql):
    conn = connect()

    cur = conn.cursor()

    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows

def getRoster(teamName, yearID):
    sql = ('SELECT DISTINCT nameFirst,nameLast FROM people p, batting b,teams t' +
           ' WHERE b.playerId = p.playerId AND b.teamID = t.teamID AND t.team_name = \''
           + str(teamName) + '\' AND b.yearID = ' + str(yearID) + ' ORDER BY p.playerId ASC')
    rows = getRowFromSQL(sql)

    return rows



class SQLRows:
    def __init__(self):
        self.sql = None
        self.rows = None




obj = SQLRows()


def getUser(username, password):
    sql = ('SELECT username,password FROM users WHERE username = \'' + username + '\' '
           + ' AND password = \'' + password + '\'')
    user = getRowFromSQL(sql)
    return user