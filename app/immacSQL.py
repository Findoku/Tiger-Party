from numpy.testing.print_coercion_tables import print_coercion_table
from sqlalchemy.testing.plugin.plugin_base import start_test_class_outside_fixtures

from app import sqlComs

def positions(pos,team):
    if "teams" in team:
        sql = 'SELECT DISTINCT p.playerid as playerid,CONCAT(p.nameFirst, \' \', p.nameLast) AS PlayerName,f.teamid FROM people AS p JOIN fielding AS f ON  p.playerID = f.playerID WHERE f.position = \'{}\' '.format(
            pos)
        if pos == 'OF':
            sql = (
                'SELECT DISTINCT p.playerid as playerid,CONCAT(p.nameFirst, \' \', p.nameLast) AS PlayerName,f.teamid  FROM people AS p JOIN fielding AS f ON  p.playerID = f.playerID WHERE f.position = \'{}\''
                ' or f.position = \'CF\' or f.position = \'RF\' or f.position = \'LF\'  ').format(pos)

    else:
        sql = 'SELECT DISTINCT p.playerid as playerid,CONCAT(p.nameFirst, \' \', p.nameLast) AS PlayerName FROM people AS p JOIN fielding AS f ON  p.playerID = f.playerID WHERE f.position = \'{}\' '.format(
            pos)
        if pos == 'OF':
            sql = ('SELECT DISTINCT p.playerid as playerid,CONCAT(p.nameFirst, \' \', p.nameLast) AS PlayerName FROM people AS p JOIN fielding AS f ON  p.playerID = f.playerID WHERE f.position = \'{}\''
                   ' or f.position = \'CF\' or f.position = \'RF\' or f.position = \'LF\'  ').format(pos)
    return sql

def teams(team, other):
    print(other)
    if "season" in other.lower() or "seasonWar" in other.lower() or "position" in other.lower():
        sql = 'SELECT DISTINCT p.playerid as playerid,CONCAT(p.nameFirst, \' \', p.nameLast) AS PlayerName,t.teamid FROM people AS p JOIN batting AS b ON p.playerID = b.playerID JOIN teams AS t ON b.teamID = t.teamID AND t.yearID = b.yearID  WHERE t.team_name = \'{}\' '.format(team)
    elif 'awards' in other.lower():
        sql = 'SELECT DISTINCT p.playerid as playerid,CONCAT(p.nameFirst, \' \', p.nameLast) AS PlayerName,t.yearid FROM people AS p JOIN batting AS b ON p.playerID = b.playerID JOIN teams AS t ON b.teamID = t.teamID AND t.yearID = b.yearID  WHERE t.team_name = \'{}\' '.format(
            team)
    elif 'teams' in other.lower():
        sql = 'SELECT DISTINCT p.playerid as playerid,CONCAT(p.nameFirst, \' \', p.nameLast) AS PlayerName FROM people AS p JOIN batting AS b ON p.playerID = b.playerID JOIN teams AS t ON b.teamID = t.teamID AND t.yearID = b.yearID  WHERE t.team_name = \'{}\' '.format(
            team)
    else:
        sql = 'SELECT DISTINCT p.playerid as playerid,CONCAT(p.nameFirst, \' \', p.nameLast) AS PlayerName FROM people AS p JOIN batting AS b ON p.playerID = b.playerID JOIN teams AS t ON b.teamID = t.teamID AND t.yearID = b.yearID WHERE t.team_name = \'{}\' '.format(team)

    return sql


def battingStat(stat):
    if (stat == "Games"):
        stat = 'b_G'
    elif (stat == "At-Bats"):
        stat = 'b_AB'
    elif (stat == "Runs"):
        stat = 'b_R'
    elif (stat == "Hits"):
        stat = 'b_H'
    elif (stat == "Doubles"):
        stat = 'b_2B'
    elif (stat == "Triples"):
        stat = 'b_3B'
    elif (stat == "Home Runs"):
        stat = 'b_HR'
    elif (stat == "RBIs"):
        stat = 'b_RBI'
    elif (stat == "Stolen Bases"):
        stat = 'b_SB'
    elif (stat == "Caught Stealing"):
        stat = 'b_CS'
    elif (stat == "Walks"):
        stat = 'b_BB'
    elif (stat == "Intentional Walks"):
        stat = 'b_IBB'
    elif (stat == "Hit By Pitch"):
        stat = 'b_HBP'
    elif (stat == "Sac Flies"):
        stat = 'b_SF'
    elif (stat == "GIDPs"):
        stat = 'b_GIDP'
    return stat


def battingSeason(stat,limit,team):
    stat = battingStat(stat)

    if ("teams" in team):
        sql = 'SELECT DISTINCT p.playerid as playerid, CONCAT(p.nameFirst, \' \', p.nameLast) AS PlayerName,b.teamid FROM people AS p JOIN batting AS b ON p.playerID = b.playerID GROUP BY p.playerID, b.yearID HAVING SUM( {} ) >= {} '.format(
            stat, limit)
    else:
        sql = 'SELECT DISTINCT p.playerid as playerid, CONCAT(p.nameFirst, \' \', p.nameLast) AS PlayerName FROM people AS p JOIN batting AS b ON p.playerID = b.playerID GROUP BY p.playerID, b.yearID HAVING SUM( {} ) >= {} '.format(
        stat, limit)

    return sql

def battingCareer(stat,limit):
    stat = battingStat(stat)

    sql = 'SELECT p.playerid as playerid, CONCAT(p.nameFirst, \' \', p.nameLast) as PlayerName FROM people AS p JOIN batting AS b ON p.playerID = b.playerID GROUP BY p.playerID HAVING SUM( {} ) >= {} '.format(stat,limit)
    return sql



def pitchingStat(stat):
    if (stat == 'Strikeouts'):
        stat = 'p_SO'
    elif (stat == 'Wins'):
        stat = 'p_W'
    elif (stat == 'Losses'):
        stat = 'p_L'
    elif (stat == 'Games'):
        stat = 'p_G'
    elif (stat == 'Games Started'):
        stat = 'p_GS'
    elif (stat == 'Saves'):
        stat = 'p_S'
    elif (stat == 'Innings Pitched Outs'):
        stat = 'p_IPOuts'
    elif (stat == 'Hits Allowed'):
        stat = 'p_G'
    elif (stat == 'Earned Runs'):
        stat = 'p_ER'
    elif (stat == 'Home Runs Allowed'):
        stat = 'p_HR'
    elif (stat == 'Walks'):
        stat = 'p_BB'
    elif (stat == 'Hitters Hit'):
        stat = 'p_HBP'
    elif (stat == 'Balks'):
        stat = 'p_BK'
    elif (stat == 'Shutouts'):
        stat = 'p_SHO'
    elif (stat == 'Sac Hits Allowed'):
        stat = 'p_SH'
    elif (stat == 'Sac Flys Allowed'):
        stat = 'p_SF'
    elif (stat == 'GIDPs'):
        stat = 'p_GIDP'
    elif (stat == 'ERA'):
        stat = 'p_ERA'
    elif (stat == 'Intentional Walks'):
        stat = 'p_IBB'
    return stat

def pitchingCareer(stat,limit):

    stat = pitchingStat(stat)

    sql = 'SELECT p.playerid as playerid,CONCAT(p.nameFirst, \' \', p.nameLast) as PlayerName FROM people AS p JOIN pitching AS pi  ON p.playerID = pi.playerID GROUP BY p.playerID HAVING SUM( {} ) >=  {} '.format(stat,limit )
    return sql


def pitchingSeason(stat,limit,team):
    stat = pitchingStat(stat)
    if ("teams" in team):
        sql = 'SELECT DISTINCT p.playerid as playerid,CONCAT(p.nameFirst, \' \', p.nameLast) AS PlayerName,pi.teamID FROM people AS p JOIN pitching AS pi ON p.playerID = pi.playerID GROUP BY p.playerID, pi.yearID HAVING SUM( {} ) >= {} '.format(
            stat, limit)
    else:
        sql = 'SELECT DISTINCT p.playerid as playerid,CONCAT(p.nameFirst, \' \', p.nameLast) AS PlayerName FROM people AS p JOIN pitching AS pi ON p.playerID = pi.playerID GROUP BY p.playerID, pi.yearID HAVING SUM( {} ) >= {} '.format(
        stat, limit)

    return sql


def fieldingStat(stat):
    if (stat == "Games"):
        stat = 'f_G'
    elif (stat == "Games Started"):
        stat = 'f_GS'
    elif (stat == "Inning Outs"):
        stat = 'f_InnOuts'
    elif (stat == "Put Outs"):
        stat = 'f_PO'
    elif (stat == "Assists"):
        stat = 'f_A'
    elif (stat == "Errors"):
        stat = 'f_E'
    elif (stat == "Double Plays"):
        stat = 'f_DP'
    elif (stat == "Catcher-Passed-Balls"):
        stat = 'f_PB'
    elif (stat == "Catcher-Stolen-Bases Allowed"):
        stat = 'f_SB'
    elif (stat == "Caught Stealing"):
        stat = 'f_CS'

    return stat

def fieldingCaeer(stat,limit):
    stat = fieldingStat(stat)

    sql = 'SELECT p.playerid as playerid,CONCAT(p.nameFirst, \' \', p.nameLast) as PlayerName FROM people AS p JOIN fielding AS f ON p.playerID = f.playerID GROUP BY p.playerID HAVING SUM( {} ) >= {} '.format(stat,limit)
    return sql

def fieldingSeason(stat,limit,team):
    stat = fieldingStat(stat)
    if ("teams" in team):
        sql = 'SELECT DISTINCT p.playerid as playerid,CONCAT(p.nameFirst, \' \', p.nameLast) AS PlayerName,f.teamid FROM people AS p JOIN fielding AS f ON p.playerID = f.playerID GROUP BY p.playerID, f.yearID HAVING SUM( {} ) >= {} '.format(
            stat, limit)
    else:
        sql = 'SELECT DISTINCT p.playerid as playerid,CONCAT(p.nameFirst, \' \', p.nameLast) AS PlayerName FROM people AS p JOIN fielding AS f ON p.playerID = f.playerID GROUP BY p.playerID, f.yearID HAVING SUM( {} ) >= {} '.format(
            stat, limit)

    return sql


def awards(award,team):
    if "teams" in team:
        sql = 'SELECT DISTINCT p.playerid as playerid,CONCAT(p.nameFirst, \' \', p.nameLast),a.yearid AS PlayerName FROM people AS p JOIN awards AS a ON p.playerID = a.playerID WHERE awardID = \'{}\' '.format(
            award)
    else:
        sql = 'SELECT DISTINCT p.playerid as playerid,CONCAT(p.nameFirst, \' \', p.nameLast) AS PlayerName FROM people AS p JOIN awards AS a ON p.playerID = a.playerID WHERE awardID = \'{}\' '.format(
            award)

    return sql

def HallofFame():
    sql = 'SELECT DISTINCT p.playerid as playerid,CONCAT(p.nameFirst, \' \', p.nameLast) as PlayerName FROM people AS p JOIN halloffame AS h ON p.playerID = h.playerID WHERE inducted = \'y\' '
    return sql

def Nationality(natty):
    sql = 'SELECT DISTINCT p.playerid as playerid,CONCAT(p.nameFirst, \' \', p.nameLast) as PlayerName FROM people AS p WHERE birthCountry =  \'{}\' '.format(natty)
    return sql

def seriesStat(series):
    if(series == 'World Series Winner'):
        series = 'WS'
    elif(series == 'National League Winner'):
        series = 'NL'
    elif (series == 'American League Winner'):
        series = 'AL'

    return series

def SeriesWinner(series):
    series = seriesStat(series)

    sql = 'SELECT DISTINCT p.playerid as playerid,CONCAT(p.nameFirst, \' \', p.nameLast) AS PlayerName FROM people AS p JOIN batting AS b ON p.playerID = b.playerID JOIN seriespost AS s ON b.yearID = s.yearID WHERE b.teamID = s.teamIDwinner AND s.round LIKE \'%{}%\'  LIMIT 1'.format(series)
    return sql

def allStar():
    sql = 'SELECT DISTINCT p.playerid as playerid,CONCAT(p.nameFirst, \' \', p.nameLast) as PlayerName FROM people AS p JOIN allstarfull as a ON p.playerID = a.playerID'
    return sql


def warAVGCareer(stat):
    sql = 'SELECT DISTINCT p.playerid as playerid,CONCAT(p.nameFirst, \' \', p.nameLast) AS PlayerName FROM people AS p JOIN extrastats AS es ON p.playerID = es.playerID GROUP BY p.playerID HAVING (AVG(es.war)) >= {} '.format(
        stat)
    return sql


def warSeason(stat,team):


    if ('teams' in team):
        sql = 'SELECT distinct p.playerid as playerid,CONCAT(p.nameFirst, \' \', p.nameLast) AS PlayerName,es.teamID FROM people AS p JOIN extrastats AS es ON p.playerID = es.playerID WHERE es.war >= {} '.format(
            stat)
    else:
        sql = 'SELECT p.playerid as playerid,CONCAT(p.nameFirst, \' \', p.nameLast) AS PlayerName FROM people AS p JOIN extrastats AS es ON p.playerID = es.playerID WHERE es.war >= {} '.format(
        stat)

    return sql


def warCareer(stat):

    sql = 'SELECT p.playerid as playerid,CONCAT(p.nameFirst, \' \', p.nameLast) AS PlayerName FROM people AS p JOIN extrastats AS es ON p.playerID = es.playerID Group by es.playerid having sum(es.WAR) >= {} '.format(
    stat)

    return sql

def battingAVGSeason(stat,team):

    if("teams" in team):
        sql = 'SELECT DISTINCT p.playerid as playerid,CONCAT(p.nameFirst, \' \', p.nameLast) AS PlayerName,b.teamID FROM people AS p JOIN batting AS b ON p.playerID = b.playerID WHERE b.b_AB > 100 GROUP BY p.playerID, b.yearID HAVING (SUM(b.b_H) * 1.0 / SUM(b.b_AB)) > {} '.format(
            stat)
    else:
        sql = 'SELECT DISTINCT p.playerid as playerid,CONCAT(p.nameFirst, \' \', p.nameLast) AS PlayerName FROM people AS p JOIN batting AS b ON p.playerID = b.playerID WHERE b.b_AB > 100 GROUP BY p.playerID, b.yearID HAVING (SUM(b.b_H) * 1.0 / SUM(b.b_AB)) > {} '.format(
        stat)

    return sql


def battingAVGCareer(stat):
    sql = 'SELECT DISTINCT p.playerid as playerid,CONCAT(p.nameFirst, \' \', p.nameLast) AS PlayerName FROM people AS p JOIN batting AS b ON p.playerID = b.playerID WHERE b.b_AB > 100 GROUP BY p.playerID HAVING ((SUM(b.b_H) * 1.0) / (SUM(b.b_AB)*1.0)) > {} '.format(stat)
    return sql

def intersect(sql1,sql2):
    sql = 'SELECT CONCAT(po.nameFirst, \' \', po.nameLast) AS PlayerName,p.debutDate From (({}) Intersect ({})) AS players JOIN popularity as po on players.playerid = po.playerid join people p on p.playerid = players.playerid WHERE NOT PlayerName = \'None\' ORDER BY popularityValue ASC'.format(sql1,sql2)

    print("INTERSECTING: :: :adas FDA")
    print(sql)
    rows = sqlComs.getRowFromSQL(sql)
    print(rows)
    return rows


def getSQL(col, subcol, limCol,other,subOther):
    sql = col

    if(other == 'calculatedAvg'):
        other = subOther
    print('Debug TIEM:')
    print(col)
    if (col == "teams"):

        sql = teams(subcol,other)
    elif (col == "awards"):
        sql = awards(subcol,other)
    elif (col == "positions"):
        sql = positions(subcol,other)
    elif (col == "seasonBatting"):
        if limCol == '':
            return 'error'
        sql = battingSeason(subcol, limCol,other)
    elif (col == "careerBatting"):
        if limCol == '':
            return 'error'
        sql = battingCareer(subcol, limCol)
    elif (col == "seasonPitching"):
        if limCol == '':
            return 'error'
        sql = pitchingSeason(subcol, limCol,other)
    elif (col == "careerPitching"):
        if limCol == '':
            return 'error'
        sql = pitchingCareer(subcol, limCol)
    elif (col == "seasonFielding"):
        if limCol == '':
            return 'error'
        sql = fieldingSeason(subcol, limCol,other)
    elif (col == "careerFielding"):
        if limCol == '':
            return 'error'
        sql = fieldingCaeer(subcol, limCol)
    elif (col == "hallOfFame"):
        sql = HallofFame()
    elif (col == "country"):
        sql = Nationality(subcol)
    elif (col == "seriesWinner"):
        sql = SeriesWinner(subcol)
    elif (col == "allStar"):
        sql = allStar()
    elif (col == "calculatedAvg"):
        if limCol == '':
            return 'error'
        if subcol == 'Season Batting Avg':
            sql = battingAVGSeason(limCol,other)
        if subcol == 'Career Batting Avg':
            sql = battingAVGCareer(limCol)
        if subcol == 'Career WAR Avg':
            sql = warAVGCareer(limCol)
    elif (col == "seasonWar"):
        print('SEASONLIMCOL:')
        print(limCol)
        sql = warSeason(limCol, other)
    elif (col == "careerWar"):
        print('CAREERLIMCOL:')
        print(limCol)
        sql = warCareer(limCol)

    return sql

def spot(col, subcol, limCol, row, subrow, limRow):

    if col == None:
        return ''
    elif row == None:
        return ''
    elif subcol == None:
        return ''
    elif subrow == None:
        return ''

    sql1 = getSQL(col, subcol, limCol, row,subrow)
    if sql1 == 'error':
        return ''
    sql2 = getSQL(row, subrow, limRow, col,subcol)
    if sql2 == 'error':
        return ''
    print('Debug TIEM:')
    print('Debug TIEM sql1:')
    print(sql1)
    print('Debug TIEM sqlp2:')
    print(sql2)
    rows = intersect(sql1,sql2)

    if(rows != []):
        val = [rows[0][0], str(rows[0][1])]
        print("theval")
        print(val)
    else:
        val = ''

    return val
