from virtualenv.config.convert import get_type

from app import app
from app import DatabaseConnection
import mariadb
from app import GlobalVals


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


def getType(type):
    if (type == 'Games Played'):
        print('HOLLOW')
        type = 'f_G'
    elif(type == 'Games Started'):
        print('HO GS')
        type = 'f_GS'
    elif(type == 'Total Outs Caused'):
        type = 'f_InnOuts'


    return type


def getCF(type):
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID
    print("depth")
    position = 'CF'
    type = getType(type)

    sql = ('Select distinct nameFirst,nameLast,' + type + ',position,yearId From fielding f Natural Join teams natural join people'
            + ' where position = \'' + position + ' \' and team_name = \'' + team_name + '\' AND yearid = ' + year_id + ' AND ' + type +' > 0 ORDER BY ' + type + ' Desc')
    CFs = getRowFromSQL(sql)

    return CFs


def getLF(type):
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID
    print("depth")
    position = 'LF'
    type = getType(type)

    sql = (
                'Select distinct nameFirst,nameLast,' + type + ',position,yearId From fielding f Natural Join teams natural join people'
                + ' where position = \'' + position + ' \' and team_name = \'' + team_name + '\' AND yearid = ' + year_id + ' AND ' + type +' > 0 ORDER BY ' + type + ' Desc')
    CFs = getRowFromSQL(sql)

    return CFs



def getRF(type):
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID
    print("depth")
    position = 'RF'
    type = getType(type)

    sql = (
                'Select distinct nameFirst,nameLast,' + type + ',position,yearId From fielding f Natural Join teams natural join people'
                + ' where position = \'' + position + ' \' and team_name = \'' + team_name + '\' AND yearid = ' + year_id + ' AND ' + type +' > 0 ORDER BY ' + type + ' Desc')
    CFs = getRowFromSQL(sql)

    return CFs


def getSS(type):
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID
    print("depth")
    position = 'SS'
    type = getType(type)

    sql = (
                'Select distinct nameFirst,nameLast,' + type + ',position,yearId From fielding f Natural Join teams natural join people'
                + ' where position = \'' + position + ' \' and team_name = \'' + team_name + '\' AND yearid = ' + year_id + ' AND ' + type +' > 0 ORDER BY ' + type + ' Desc')
    CFs = getRowFromSQL(sql)

    return CFs


def get2B(type):
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID
    print("depth")
    position = '2B'
    type = getType(type)

    sql = (
                'Select distinct nameFirst,nameLast,' + type + ',position,yearId From fielding f Natural Join teams natural join people'
                + ' where position = \'' + position + ' \' and team_name = \'' + team_name + '\' AND yearid = ' + year_id + ' AND ' + type +' > 0 ORDER BY ' + type + ' Desc')
    CFs = getRowFromSQL(sql)

    return CFs


def get3B(type):
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID
    print("depth")
    position = '3B'
    type = getType(type)

    sql = ('Select distinct nameFirst,nameLast,' + type + ',position,yearId From fielding f Natural Join teams natural join people'
            + ' where position = \'' + position + ' \' and team_name = \'' + team_name + '\' AND yearid = ' + year_id + ' AND ' + type +' > 0 ORDER BY ' + type + ' Desc')
    CFs = getRowFromSQL(sql)

    return CFs



def get3B(type):
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID
    print("depth")
    position = '3B'
    type = getType(type)

    sql = ('Select distinct nameFirst,nameLast,' + type + ',position,yearId From fielding f Natural Join teams natural join people'
                + ' where position = \'' + position + ' \' and team_name = \'' + team_name + '\' AND yearid = ' + year_id + ' AND ' + type +' > 0 ORDER BY ' + type + ' Desc')
    CFs = getRowFromSQL(sql)

    return CFs


def get1B(type):
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID
    print("depth")
    position = '1B'
    type = getType(type)

    sql = ('Select distinct nameFirst,nameLast,' + type + ',position,yearId From fielding f Natural Join teams natural join people'
                + ' where position = \'' + position + ' \' and team_name = \'' + team_name + '\' AND yearid = ' + year_id + ' AND ' + type +' > 0 ORDER BY ' + type + ' Desc')
    CFs = getRowFromSQL(sql)

    return CFs


def getC(type):
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID
    print("depth")
    position = 'C'
    type = getType(type)

    sql = ('Select distinct nameFirst,nameLast,' + type + ',position,yearId From fielding f Natural Join teams natural join people'
                + ' where position = \'' + position + ' \' and team_name = \'' + team_name + '\' AND yearid = ' + year_id + ' AND ' + type +' > 0 ORDER BY ' + type + ' Desc')
    CFs = getRowFromSQL(sql)

    return CFs



def getP(type):
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID
    print("depth")
    position = 'P'
    type = getType(type)

    sql = ('Select distinct nameFirst,nameLast,' + type + ',position,yearId From fielding f Natural Join teams natural join people'
                + ' where position = \'' + position + ' \' and team_name = \'' + team_name + '\' AND yearid = ' + year_id + ' AND ' + type +' > 0 ORDER BY ' + type + ' Desc')
    CFs = getRowFromSQL(sql)

    return CFs
