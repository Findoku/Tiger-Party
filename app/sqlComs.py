from app import app
from app import DatabaseConnection
import mariadb
from app import GlobalVals
from app import Caesar


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

def executeUpdate(sql):
    conn = connect()

    cur = conn.cursor()

    cur.execute(sql)
    conn.commit()
    conn.close()

def executeDelete(sql):
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


def getSQLRoster(teamName, yearID, type):
    if(type == 'All'):
        sql = ('(SELECT DISTINCT p.nameFirst, p.nameLast, p.playerid FROM people p JOIN batting b ON b.playerid = p.playerid JOIN teams t ON t.teamid = b.teamid WHERE t.team_name = \'' + teamName + '\' AND b.yearid = ' + yearID + ') '
                + ' UNION (SELECT DISTINCT p.nameFirst, p.nameLast, p.playerid FROM people p JOIN fielding f ON f.playerid = p.playerid JOIN teams t ON t.teamid = f.teamid WHERE t.team_name = \'' + teamName + '\' AND f.yearid = ' + yearID + ') '
                + ' UNION (SELECT DISTINCT p.nameFirst, p.nameLast, p.playerid FROM people p JOIN pitching pi ON pi.playerid = p.playerid JOIN teams t ON t.teamid = pi.teamid WHERE t.team_name = \'' + teamName + '\' AND pi.yearid = ' + yearID + ') '
                + ' UNION (SELECT DISTINCT p.nameFirst, p.nameLast, p.playerid FROM people p JOIN managers m ON m.playerID = p.playerid JOIN teams t ON t.teamid = m.teamid WHERE t.team_name = \'' + teamName + '\' AND m.yearid = ' + yearID + ') ORDER BY playerid ASC')
    elif(type == 'Managers'):
        sql = 'SELECT DISTINCT p.nameFirst, p.nameLast, p.playerid FROM people p JOIN managers m ON m.playerID = p.playerid JOIN teams t ON t.teamid = m.teamid WHERE t.team_name = \'' + teamName + '\' AND m.yearid = ' + yearID + ''
    elif (type == 'Pitchers'):
        sql = 'SELECT DISTINCT p.nameFirst, p.nameLast, p.playerid FROM people p JOIN pitching pi ON pi.playerid = p.playerid JOIN teams t ON t.teamid = pi.teamid WHERE t.team_name = \'' + teamName + '\' AND pi.yearid = ' + yearID
    elif (type == 'Batters'):
        sql = 'SELECT DISTINCT p.nameFirst, p.nameLast, p.playerid FROM people p JOIN fielding f ON f.playerid = p.playerid JOIN teams t ON t.teamid = f.teamid WHERE t.team_name = \'' + teamName + '\' AND f.yearid = ' + yearID
    elif (type == 'Fielding Players'):
        sql = 'SELECT DISTINCT p.nameFirst, p.nameLast, p.playerid FROM people p JOIN batting b ON b.playerid = p.playerid JOIN teams t ON t.teamid = b.teamid WHERE t.team_name = \'' + teamName + '\' AND b.yearid = ' + yearID


    return sql

def getRoster(teamName, yearID,type):
    sql = getSQLRoster(teamName, yearID,type)

    rows = getRowFromSQL(sql)

    return rows



class SQLRows:
    def __init__(self):
        self.sql = None
        self.rows = None




obj = SQLRows()


def getUser(username, password):
    sql = ('SELECT id,username,password FROM users WHERE username = \'' + username + '\'')

    user = getRowFromSQL(sql)
    print(user)
    if user:
        id = user[0][0]
        psswd = user[0][2]
        e = Caesar.caesar_cipher(password, id)

        if (e == psswd):
            return user

    return []


def getAdminUser(username, password):
    sql = ('SELECT username,password FROM admin WHERE username = \'' + username + '\' '
           + ' AND password = \'' + password + '\'')

    user = getRowFromSQL(sql)



    return user

def getType(type):
    if (type == 'Games Played'):

        type = 'f_G'
    elif(type == 'Games Started'):
        type = 'f_GS'
    elif(type == 'Total Outs Caused'):
        type = 'f_InnOuts'
    elif(type == 'wRC+'):
        type = 'wRCPlus'


    return type

def positionSQL(type,position,team_name,year_id):
    if (type == "WAR" or type == "PA" or type=="wRCPlus"):
        sql = ('Select distinct nameFirst,nameLast,round(' + type + ',2),position,e.yearId From fielding f Natural Join teams t natural join people join extrastats e using(playerid) '
                ' where position = \'' + position + ' \' and team_name = \'' + team_name + '\' AND e.yearid = ' + year_id + ' AND t.teamid = e.teamid order by ' + type + ' desc')
    else:
        sql = ('Select distinct nameFirst,nameLast,' + type + ',position,yearId From fielding f Natural Join teams natural join people'
                + ' where position = \'' + position + ' \' and team_name = \'' + team_name + '\' AND yearid = ' + year_id + ' AND '
                + type + ' > 0 ORDER BY ' + type + ' Desc')

    return sql;




def getOF(type):
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID
    position = 'OF'
    type = getType(type)

    sql = positionSQL(type, position, team_name, year_id)
    CFs = getRowFromSQL(sql)

    return CFs

def getCF(type):
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID
    position = 'CF'
    type = getType(type)

    sql = positionSQL(type, position, team_name, year_id)

    CFs = getRowFromSQL(sql)

    return CFs


def getLF(type):
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID
    position = 'LF'
    type = getType(type)

    sql = positionSQL(type, position, team_name, year_id)
    CFs = getRowFromSQL(sql)

    return CFs



def getRF(type):
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID

    position = 'RF'
    type = getType(type)

    sql = positionSQL(type, position, team_name, year_id)
    CFs = getRowFromSQL(sql)

    return CFs


def getSS(type):
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID

    position = 'SS'
    type = getType(type)

    sql = positionSQL(type, position, team_name, year_id)
    CFs = getRowFromSQL(sql)

    return CFs


def get2B(type):
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID

    position = '2B'
    type = getType(type)

    sql = positionSQL(type, position, team_name, year_id)
    CFs = getRowFromSQL(sql)

    return CFs


def get3B(type):
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID

    position = '3B'
    type = getType(type)

    sql = positionSQL(type, position, team_name, year_id)
    CFs = getRowFromSQL(sql)

    return CFs



def get3B(type):
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID

    position = '3B'
    type = getType(type)

    sql = positionSQL(type, position, team_name, year_id)
    CFs = getRowFromSQL(sql)

    return CFs


def get1B(type):
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID

    position = '1B'
    type = getType(type)

    sql = positionSQL(type, position, team_name, year_id)

    CFs = getRowFromSQL(sql)

    return CFs


def getC(type):
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID

    position = 'C'
    type = getType(type)

    sql = positionSQL(type, position, team_name, year_id)

    CFs = getRowFromSQL(sql)

    return CFs



def getP(type):
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID

    position = 'P'
    type = getType(type)


    sql = positionSQL(type,position,team_name,year_id)

    CFs = getRowFromSQL(sql)

    return CFs



def registerAccount(username, password):

    sql = 'select id from users where username = \'' +  username + '\''
    rows = getRowFromSQL(sql)
    if(rows  == []):
        sql = """INSERT INTO users(username,password) values( \'""" + username + """\', \'""" + password + """\')"""

        executeInsert(sql)

        sql = 'Select id, password from users where username = \'' + username + '\''
        rows = getRowFromSQL(sql)
        id = rows[0][0]
        password = rows[0][1]

        e = Caesar.caesar_cipher(password, id)

        sql = """UPDATE users SET password = '""" + e + """' WHERE id = """ + str(id)
        executeUpdate(sql)
    else:
        return 'Error: username Already taken'


def insertHistory(admin):

    if(admin is not None):
        sql = ("""Insert into userHistory(id,username,teamSearched,yearid) values (""" + str(-9999) + """,'""" +
               'greg' + """','""" + GlobalVals.teamName + """',""" + str(GlobalVals.yearID) + """) """)
        executeInsert(sql)
    else:
        sql = 'Select username from users where id = ' + str(GlobalVals.currentID)
        rows = getRowFromSQL(sql)

        sql = """Insert into userHistory(id,username,teamSearched,yearid) values (""" + str(GlobalVals.currentID) + """,'""" + str(
            rows[0][0]) + """','""" + GlobalVals.teamName + """',""" + str(GlobalVals.yearID) + """) """
        executeInsert(sql)
