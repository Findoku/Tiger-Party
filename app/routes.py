

from app import app


from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from app import teams
from app.DatabaseConnection import mysql
from app.GlobalVals import valid
from app.forms import LoginForm, DisplayForm, TeamForm, RegisterForm, DepthForm, rosterForm, AdminForm
from app import sqlComs
from app import Caesar
from app import GlobalVals
from app import immacSQL
import json





@app.route('/', methods=['GET', 'POST'])
def startPage():
    print("hi")

    form = LoginForm()

    if form.validate_on_submit():
        user = sqlComs.getUser(form.username.data,form.password.data)
        print(user)

        if (user != []):
            GlobalVals.valid = 'true'
            GlobalVals.currentID = user[0][0]
            GlobalVals.bannedStatus = user[0][3]

            return redirect('/showTeams')

    return render_template('index.html', form=form)


@app.route('/adminLogin', methods=['GET', 'POST'])
def adminLogin():

    form = AdminForm()

    if form.validate_on_submit():

        user = sqlComs.getAdminUser(form.username.data,form.password.data)


        if (user != []):
            GlobalVals.valid = 'true'
            GlobalVals.admin = 'true'
            return redirect('/admin')

    return render_template('AdminLogin.html', form=form)


@app.route('/admin', methods=['GET', 'POST'])
def adminPage():

    sql = 'Select * from users'
    users = sqlComs.getRowFromSQL(sql)


    if(GlobalVals.admin == 'false'):
        return redirect(url_for('startPage'))

    return render_template('AdminPage.html',users=users)


@app.route('/player')
def player():
    admin = None
    if GlobalVals.admin == 'true':
        admin = 1
    if GlobalVals.bannedStatus == 'Y':
        return redirect(url_for('banned'))
    player_id = request.args.get('player', 'No')

    sql = 'Select * FROM people WHERE playerid = \'' + player_id + '\''

    rows = sqlComs.getRowFromSQL(sql)

    sql = ('Select sum(b_G),sum(b_AB),sum(b_R),sum(b_h),sum(b_2b),sum(b_3b),sum(b_HR),sum(b_SB)'
           ' ,sum(b_SO),sum(b_IBB),sum(b_hbp),sum(b_SH),sum(b_SF), round(sum(b_H)*100/sum(b_ab)) '
           ',round(sum(b_R)*100/sum(b_AB)), round(sum(b_hr)*100/sum(b_AB),0), round(AVG(e.WAR),2) from batting LEFT JOIN extrastats e ON e.playerid = batting.playerid and e.yearid = batting.yearid AND e.teamid = batting.teamid where batting.playerid= \'' + player_id + '\'')
    battingRows = sqlComs.getRowFromSQL(sql)

    sql = ('SELECT SUM(p_W), SUM(p_L), SUM(p_G), SUM(p_GS), SUM(p_CG), SUM(p_SHO), SUM(p_SV), SUM(p_H), SUM(p_HR) '
           ' ,SUM(p_BB), SUM(p_SO), round(AVG(p_BAOpp),2), round(AVG(p_ERA),2), SUM(p_IBB), SUM(p_WP), SUM(p_HBP), SUM(p_BK), MAX(p_BFP)'
           ', SUM(p_R), SUM(p_SH), SUM(p_SF), CASE WHEN SUM(p_L) = 0 THEN NULL ELSE round(CAST(SUM(p_W) AS FLOAT) / SUM(p_L),2) END '
           ',round(AVG(e.WAR),2)  FROM pitching LEFT JOIN extrastats e ON e.playerid = pitching.playerid and e.yearid = pitching.yearid AND e.teamid = pitching.teamid  WHERE pitching.playerid = \'') + player_id + '\''
    pitchingRows = sqlComs.getRowFromSQL(sql)
    sql = ('SELECT SUM(f_G), SUM(f_GS), SUM(f_PO), SUM(f_A), SUM(f_E), SUM(f_DP), SUM(f_PB), SUM(f_SB), SUM(f_CS), AVG(f_ZR),round(AVG(WAR),2) '
           ' FROM fielding LEFT JOIN extrastats e ON e.playerid = fielding.playerid and e.yearid = fielding.yearid AND e.teamid = fielding.teamid  WHERE fielding.playerid = \'' + player_id + '\' ')
    fieldingRows = sqlComs.getRowFromSQL(sql)

    sql = 'SELECT Distinct Position FROM fielding WHERE playerid = \'' + player_id + '\''
    positions = sqlComs.getRowFromSQL(sql)



    sql = 'Select sum(manager_G),sum(manager_W),sum(manager_L) FROM managers WHERE playerid = \'' + player_id + '\''
    managerRows = sqlComs.getRowFromSQL(sql)

    sql = 'Select Distinct team_name FROM managers join teams using(teamId) WHERE playerid = \'' + player_id + '\''
    teamsManaged = sqlComs.getRowFromSQL(sql)

    sql = 'Select inducted from hallofFame where inducted = \'Y\' AND playerid = \'' + player_id + '\''
    halloffame = sqlComs.getRowFromSQL(sql)


    sql = ('SELECT b.yearID, team_name,b_G, b_AB, b_R,b_H, b_2B, b_3B,b_RBI, b_HR, b_SB, b_CS '
           ', b_BB, b_SO, b_IBB, b_HBP, b_SH, b_SF, round(e.WAR,2) FROM batting b Natural Join teams left join extrastats e on e.playerid = b.playerid AND e.yearid = b.yearid AND e.teamid = b.teamid'
           ' WHERE b.playerid = \'' + player_id + '\' ORDER BY b.yearID ASC')
    battingSeason = sqlComs.getRowFromSQL(sql)

    sql = ('SELECT p.yearid, team_name, p_W, p_L, p_G, p_GS, p_CG, p_SHO, p_SV, p_H, p_HR, p_BB,p_SO,p_BAOpp '
           ', p_ERA,p_IBB,p_WP,p_HBP, p_BK,p_R, p_SH,p_SF,round(e.WAR,2) FROM pitching p NATURAL JOIN TEAMS left join extrastats e on e.playerid = p.playerid AND e.yearid = p.yearid AND e.teamid = p.teamid'
           ' WHERE p.playerid = \'' + player_id + '\' order by p.yearid asc;')
    pitchingSeason = sqlComs.getRowFromSQL(sql)

    sql = (' SELECT f.yearid, team_name, position,f_G, f_GS, f_InnOuts, f_PO, f_A, f_E, f_DP, f_PB '
           ', f_WP, f_SB, f_CS,round(e.WAR,2) FROM fielding f natural join teams left join extrastats e on e.playerid = f.playerid AND e.yearid = f.yearid AND e.teamid = f.teamid'
           ' WHERE f.playerid = \'' + player_id + '\' ORDER BY f.yearID ASC')

    fieldingSeason = sqlComs.getRowFromSQL(sql)


    return render_template('playerStats.html', rows=rows,battingRows=battingRows,pitchingRows=pitchingRows,
                           fieldingRows=fieldingRows,positions=positions,managerRows=managerRows,teamsManaged=teamsManaged,
                           halloffame=halloffame,battingSeason=battingSeason,pitchingSeason=pitchingSeason,fieldingSeason=fieldingSeason,admin=admin)

@app.route('/team/roster', methods=['GET', 'POST'],endpoint='index')
def index():
    admin = None
    if GlobalVals.admin == 'true':
        admin = 1
    if GlobalVals.bannedStatus == 'Y':
        return redirect(url_for('banned'))
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID
    type = 'All'
    form = rosterForm()

    if(form.validate_on_submit()):
        type = form.rosterOptions.data

    print("roster")
    rows = sqlComs.getRoster(team_name, year_id,type)

    return render_template('webPage/mainPage.html', rows=rows,form=form,admin=admin)

@app.route('/feats', methods=['GET', 'POST'],endpoint='feats')
def feats():
    admin = None
    if GlobalVals.admin == 'true':
        admin = 1
    if GlobalVals.bannedStatus == 'Y':
        return redirect(url_for('banned'))
    form = rosterForm()

    if(form.validate_on_submit()):
        type = form.rosterOptions.data

    sql = 'select * from highestbattingstat'

    battingHigh = sqlComs.getRowFromSQL(sql)

    sql = 'SELECT * FROM highestpitchingstat'
    pitchingHigh = sqlComs.getRowFromSQL(sql)

    sql = 'SELECT * FROM highestfieldingstat'
    fieldingHigh = sqlComs.getRowFromSQL(sql)

    return render_template('feats.html', battingHigh=battingHigh,pitchingHigh=pitchingHigh,fieldingHigh=fieldingHigh,form=form,admin=admin)



@app.route('/team/Batting-Stats')
def battingStats():
    admin = None
    if GlobalVals.admin == 'true':
        admin = 1
    if GlobalVals.bannedStatus == 'Y':
        return redirect(url_for('banned'))
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID

    sql = ('SELECT nameFirst, nameLast, b_ab,b_r,b_h,b_2b,b_3b,b_hr,b_RBI,b_SB,b_CS,b_BB,b_SO,b_sh,b_SF,round(WAR,3)' +
             ' FROM batting b NATURAL JOIN TEAMS NATURAL JOIN people left join extrastats e on e.playerid = b.playerid AND e.yearid = b.yearid AND e.teamid = b.teamid WHERE team_name = '
            + '\'' + team_name + '\'  AND b.yearid = ' + year_id + ' Group By b.playerID')
    rows = sqlComs.getRowFromSQL(sql);


    return render_template('webPage/BattingStats.html', rows=rows,admin=admin)


@app.route('/team/Pitching-Stats')
def pitchingStats():
    admin = None
    if GlobalVals.admin == 'true':
        admin = 1
    if GlobalVals.bannedStatus == 'Y':
        return redirect(url_for('banned'))
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID
    sql = ('SELECT nameFirst, nameLast, p_GS,p_CG,p_SHO,p_IPOuts,p_H,p_Er,p_HR,p_BB,p_SO,p_BAOpp,p_ERA,p_IBB,p_HBP,p_GF,round(WAR,3)' +
             ' FROM pitching p NATURAL JOIN TEAMS NATURAL JOIN people left join extrastats e on e.playerid = p.playerid AND e.yearid = p.yearid AND e.teamid = p.teamid WHERE team_name = '
            + '\'' + team_name + '\'  AND p.yearid = ' + year_id + ' Group By p.playerID')
    rows = sqlComs.getRowFromSQL(sql)


    return render_template('webPage/PitchingStats.html', rows=rows,admin=admin)

@app.route('/team/Fielding')
def Fielding():
    admin = None
    if GlobalVals.admin == 'true':
        admin = 1
    if GlobalVals.bannedStatus == 'Y':
        return redirect(url_for('banned'))
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID

    sql = ('SELECT nameFirst, nameLast, f_G,f_GS,f_InnOuts,f_PO,f_A,f_E,f_DP,f_PB,f_SB,f_CS,f_ZR,round(WAR,3)' +
             ' FROM fielding f NATURAL JOIN TEAMS NATURAL JOIN people left join extrastats e on e.playerid = f.playerid AND e.yearid = f.yearid AND e.teamid = f.teamid WHERE team_name = '
            + '\'' + team_name + '\'  AND f.yearid = ' + year_id + ' Group By f.playerID')

    rows = sqlComs.getRowFromSQL(sql)


    return render_template('webPage/Fielding.html', rows=rows,admin=admin)


@app.route('/team/Depth-Chart', methods=['GET', 'POST'])
def DepthChart():
    admin = None

    if GlobalVals.admin == 'true':
        admin = 1

    if GlobalVals.bannedStatus == 'Y':
        return redirect(url_for('banned'))
    form = DepthForm()
    if request.method == 'POST':

        if 'option' in request.form:
            option = request.form.get('option', None)
            GlobalVals.DepthChartOption = option


    if not form.is_submitted():
        form.depth_dropdown.data = GlobalVals.DepthChartOption

    OFs = sqlComs.getOF(GlobalVals.DepthChartOption)
    CFs = sqlComs.getCF(GlobalVals.DepthChartOption)
    LFs = sqlComs.getLF(GlobalVals.DepthChartOption)
    RFs = sqlComs.getRF(GlobalVals.DepthChartOption)
    SSs = sqlComs.getSS(GlobalVals.DepthChartOption)
    secBs = sqlComs.get2B(GlobalVals.DepthChartOption)
    thirdBs = sqlComs.get3B(GlobalVals.DepthChartOption)
    firstBs = sqlComs.get3B(GlobalVals.DepthChartOption)
    Cs = sqlComs.get3B(GlobalVals.DepthChartOption)
    Ps = sqlComs.getP(GlobalVals.DepthChartOption)

    return render_template('webPage/DepthChart.html',OFs=OFs, CFs=CFs, LFs=LFs, RFs=RFs, SSs=SSs, secBs=secBs, thirdBs=thirdBs,
                           firstBs=firstBs, Cs=Cs, Ps=Ps, form=form,admin=admin)

@app.route('/team/Team-Stats', methods = ['GET','POST'])
def TeamStats():
    admin = None
    if GlobalVals.admin == 'true':
        admin = 1

    if GlobalVals.bannedStatus == 'Y':
        return redirect(url_for('banned'))
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID
    sql = ('SELECT nameFirst, nameLast, sum(p_SHO),sum(p_IPOuts),sum(p_H),sum(p_SO),ROUND(sum(p_BAOpp)/count(playerid),3),ROUND(sum(p_ERA)/count(playerid),3),sum(p_IBB),sum(p_HBP)'
           ' FROM pitching NATURAL JOIN TEAMS NATURAL JOIN people WHERE team_name = \''+team_name +'\' AND yearID = ' + year_id +' Group BY yearId')

    pitchingRows = sqlComs.getRowFromSQL(sql)



    sql = ('SELECT nameFirst, nameLast,sum(b_AB),sum(b_R), round(sum(b_R)/sum(b_AB),3),sum(b_h),sum(b_2B),sum(b_3B),sum(b_HR),round(sum(b_HR)/sum(b_AB),3),sum(b_SB),sum(b_BB),sum(b_SO),sum(b_SH),sum(b_SF)'
           ' FROM batting NATURAL JOIN TEAMS NATURAL JOIN people WHERE team_name = \''+team_name +'\' AND yearID = ' + year_id +' Group BY yearId')


    battingRows = sqlComs.getRowFromSQL(sql)


    sql = ('SELECT nameFirst, nameLast, sum(f_PO),sum(f_A), sum(f_E),sum(f_CS)'
           ' FROM fielding NATURAL JOIN TEAMS NATURAL JOIN people  WHERE team_name = \''+team_name +'\' AND yearID = ' + year_id +' Group BY yearId')
    fieldingRows = sqlComs.getRowFromSQL(sql)


    sql = 'Select wins,round,team_name,yearid From seriespost NATURAL JOIN teams WHERE teams.teamid = teamIdwinner AND round = \'WS\' AND team_name = \'' +  team_name+ '\';'
    WSs = sqlComs.getRowFromSQL(sql)



    if not WSs:  # Set default if empty
        WSs = [['a','b','c','Never Won a World Series']]
    return render_template('webPage/TeamStats.html',pitchingRows=pitchingRows,battingRows=battingRows,fieldingRows=fieldingRows, WSs=WSs,admin=admin)



@app.route('/ImmaculateGridGuesser', methods=['GET', 'POST'])
def ImmacGrid():
    db_connection = sqlComs.connect()
    cursor = db_connection.cursor()

    #Teams
    cursor.execute("SELECT DISTINCT team_name FROM teams")
    teams = [row[0] for row in cursor.fetchall()]

    #Awards
    cursor.execute("SELECT DISTINCT awardID FROM awards")
    awards = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT position FROM fielding;")
    positions = [row[0] for row in cursor.fetchall()]
    positions.append("DH")

    batting_stats = ['Games', 'At-Bats', 'Runs', 'Hits', 'Doubles', 'Triples', 'Home Runs', 'RBIs', 'Stolen Bases',
                        'Caught Stealing', 'Walks', 'Strike Outs', 'Intentional Walks', 'Hit By Pitch', 'Sac Hits',
                        'Sac Flys', 'GIDPs']
    print(batting_stats)

    pitching_stats = ['Wins', 'Losses', 'Games', 'Games Started', 'Saves', 'Innings Pitched Outs', 'Hits Allowed', 'Strikeouts', 'Earned Runs',
                        'Home Runs Allowed', 'Shutouts','Walks', 'ERA', 'Intentional Walks', 'Hitters Hit', 'Balks', 'Sac Hits Allowed',
                        'Sac Flys Allowed', 'GIDPs']

    print(pitching_stats)

    fielding_stats = ['Games', 'Games Started', 'Inning Outs', 'Put Outs', 'Assists', 'Errors', 'Double Plays', 
                        'Catcher-Passed Balls', 'Catcher-Stolen Bases Allowed', 'Caught Stealing']

    hallOfFame = ['Inducted']

    cursor.execute("SELECT DISTINCT birthCountry FROM people;")
    countries = [row[0] for row in cursor.fetchall()]

    seriesWinner = ['World Series Winner', 'National League Winner', 'American League Winner']

    allStar = ['All Star']

    calculatedStats = ['Season Batting Avg', 'Career Batting Avg', 'Career WAR Avg']

    war = ['WAR']

    db_connection.close()
    
    columns = ['Column 1', 'Column 2', 'Column 3']
    rows = ['Row 1', 'Row 2', 'Row 3']

    teamsJSON = json.dumps(teams)
    awardsJSON = json.dumps(awards)
    positionJSON = json.dumps(positions)
    battingJSON = json.dumps(batting_stats)
    pitchingJSON = json.dumps(pitching_stats)
    fieldingJSON = json.dumps(fielding_stats)
    hofJSON = json.dumps(hallOfFame)
    countriesJSON = json.dumps(countries)
    seriesJSON = json.dumps(seriesWinner)
    allJSON = json.dumps(allStar)
    cAVGJSON = json.dumps(calculatedStats)
    warJSON = json.dumps(war)


    R1 = ['','a','b','c']
    R2 = ['', 'd', 'e', 'f']
    R3 = ['', 'g', 'h', 'i']

    if request.method == 'POST':

        selections = request.form.to_dict()
        limRow1 = request.form.get('limRow1')
        limRow2 = request.form.get('limRow2')
        limRow3 = request.form.get('limRow3')
        limCol1 = request.form.get('limCol1')
        limCol2 = request.form.get('limCol2')
        limCol3 = request.form.get('limCol3')

        col1 = request.form.get('col1')
        col2 = request.form.get('col2')
        col3 = request.form.get('col3')

        subcol1 = request.form.get('subcol1')
        subcol2 = request.form.get('subcol2')
        subcol3 = request.form.get('subcol3')

        row1 = request.form.get('row1')
        row2 = request.form.get('row2')
        row3 = request.form.get('row3')

        subrow1 = request.form.get('subrow1')
        subrow2 = request.form.get('subrow2')
        subrow3 = request.form.get('subrow3')

        print(col1)
        print(subcol1)
        print(row1)
        print(subrow1)



        R1[1] = immacSQL.spot(col1, subcol1, limCol1, row1, subrow1, limRow1)
        print(R1[1])

        R2[1] = immacSQL.spot(col2, subcol2, limCol2, row1, subrow1, limRow1)
        print(R2[1])
        R3[1] = immacSQL.spot(col3, subcol3, limCol3, row1, subrow1, limRow1)
        print(R3[1])

        R1[2] = immacSQL.spot(col1, subcol1, limCol1, row2, subrow2, limRow2)
        print(R1[2])
        R2[2] = immacSQL.spot(col2, subcol2, limCol2, row2, subrow2, limRow2)
        print(R2[2])
        R3[2] = immacSQL.spot(col3, subcol3, limCol3, row2, subrow2, limRow2)
        print(R3[2])

        R1[3] = immacSQL.spot(col1, subcol1, limCol1, row3, subrow3, limRow3)
        print(R1[3])
        R2[3] = immacSQL.spot(col2, subcol2, limCol2, row3, subrow3, limRow3)
        print(R2[3])
        R3[3] = immacSQL.spot(col3, subcol3, limCol3, row3, subrow3, limRow3)
        print(R3[3])

        print("input")
        print("Selections:")


        print(selections)


    return render_template('ImmaculateGrid.html', allJSON=allJSON, seriesJSON=seriesJSON, fieldingJSON=fieldingJSON, countriesJSON=countriesJSON,
                            hofJSON=hofJSON, pitchingJSON=pitchingJSON, battingJSON=battingJSON, positionsJSON=positionJSON, warJSON=warJSON,
                            teamJSON=teamsJSON, awardJSON=awardsJSON, awardOptions=awards, cAVGJSON=cAVGJSON,teamOptions=teams, columns=columns,
                            rows=rows, R1=R1,R3=R3,R2=R2)

@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()
    val = None
    if form.validate_on_submit():
        val = sqlComs.registerAccount(form.username.data, form.password.data)
        if val is None:
            return redirect(url_for('startPage'))

    return render_template('register.html', form=form, val=val)


@app.route('/showTeams', methods=['GET', 'POST'])
def showTeams():
    admin = None
    if GlobalVals.admin == 'true':
        admin = 1

    if (GlobalVals.valid == 'none'):
        return redirect(url_for('startPage'))

    if (GlobalVals.bannedStatus == 'Y'):
        return redirect(url_for('banned'))


    form = DisplayForm()
    sql = 'SELECT DISTINCT teamID, team_name FROM teams'

    form.team_dropdown.choices = teams.teams

    if form.team_dropdown.data is not None and form.year_dropdown is not None:


        GlobalVals.teamName = form.team_dropdown.data

        GlobalVals.yearID =form.year_dropdown.data
        sqlComs.insertHistory(admin)
        return redirect(url_for('index' ))



    if request.method == 'POST':

        if 'teamName' in request.form:

            team_name = request.form.get('teamName', None)

            # Logic to determine years based on team selection
            sql = "SELECT yearID FROM teams WHERE team_name = '{}'".format(team_name)

            years = sqlComs.getRowFromSQL(sql)

            form.year_dropdown.choices = years
            return jsonify(years=years)

    return render_template('showTeams.html', title='Sign In', form=form, choices=teams, admin=admin)


@app.route('/banned')
def banned():
    return render_template('BannedPage.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    data = request.get_json()

    if data and data.get('action') == 'logout':

        GlobalVals.valid = 'false'
        GlobalVals.admin = 'false'
        GlobalVals.bannedStatus = 'N'
        return redirect(url_for('startPage'))


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    data = request.get_json()

    if data and data.get('id'):
        id = data.get('id')
        sql = 'DELETE FROM users WHERE id = ' + str(id)
        sqlComs.executeDelete(sql)

    sql = 'SELECT * FROM users'
    updated_users = sqlComs.getRowFromSQL(sql)

    return jsonify([{
        'id': user[0],
        'username': user[1],
        'password': user[2],  # Consider security implications
        'status': user[3]
    } for user in updated_users])


@app.route('/ban', methods=['POST'])
def ban():
    data = request.get_json()
    # Logic to toggle the ban status
    if data and data.get('id'):
        id = data.get('id')
        sql = 'Update users SET bannedStatus = \'Y\' WHERE id = ' + str(id)
        sqlComs.executeUpdate(sql)

    # Fetch updated users list
    sql = 'SELECT * FROM users'
    updated_users = sqlComs.getRowFromSQL(sql)

    return jsonify([{
        'id': user[0],
        'username': user[1],
        'password': user[2],  # Consider security implications
        'status': user[3]
    } for user in updated_users])


@app.route('/unban', methods=['POST'])
def unban():
    data = request.get_json()
    # Logic to toggle the ban status
    if data and data.get('id'):
        id = data.get('id')
        sql = 'Update users SET bannedStatus = \'N\' WHERE id = ' + str(id)
        sqlComs.executeUpdate(sql)

    # Fetch updated users list
    sql = 'SELECT * FROM users'
    updated_users = sqlComs.getRowFromSQL(sql)

    return jsonify([{
        'id': user[0],
        'username': user[1],
        'password': user[2],  # Consider security implications
        'status': user[3]
    } for user in updated_users])




@app.route('/sort', methods=['GET', 'POST'])
def sort():

    data = request.get_json()
    baseballRole = data.get('type')
    sorting = data.get('action')
    stat = data.get('stat')
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID


    if(baseballRole == 'pitching'):
        sql = ('SELECT nameFirst, nameLast, p_GS, p_CG, p_SHO, p_IPOuts, p_H, p_ER, p_HR, p_BB, p_SO, p_BAOpp, p_ERA, p_IBB, p_HBP, p_GF,round(WAR,3) '
            'FROM pitching a NATURAL JOIN TEAMS NATURAL JOIN people left join extrastats e on e.playerid = a.playerid AND a.yearid = e.yearid  AND e.teamid = a.teamid WHERE team_name = \'{}\' AND a.yearid = {} '
            'GROUP BY a.playerID, a.yearID ORDER BY {} {}'.format( team_name, year_id, stat, sorting))
    elif(baseballRole == 'batting'):
        sql = ('SELECT nameFirst, nameLast, b_ab,b_r,b_h,b_2b,b_3b,b_hr,b_RBI,b_SB,b_CS,b_BB,b_SO,b_sh,b_SF,round(WAR,3) '
               'FROM {} a NATURAL JOIN TEAMS NATURAL JOIN people left join extrastats e on e.playerid = a.playerid AND a.yearid = e.yearid AND e.teamid = a.teamid WHERE team_name = \'{}\' AND a.yearid = {} '
               'GROUP BY a.playerID, a.yearID ORDER BY {} {}'.format(baseballRole, team_name, year_id, stat, sorting))
    elif (baseballRole == 'fielding'):
        sql = ('SELECT nameFirst, nameLast, f_G,f_GS,f_InnOuts,f_PO,f_A,f_E,f_DP,f_PB,f_SB,f_CS,f_ZR,round(WAR,3) '
               'FROM {} a NATURAL JOIN TEAMS NATURAL JOIN people left join extrastats e on e.playerid = a.playerid AND a.yearid = e.yearid AND e.teamid = a.teamid WHERE team_name = \'{}\' AND a.yearid = {} '
               'GROUP BY a.playerID, a.yearID ORDER BY {} {}'.format(baseballRole, team_name, year_id, stat, sorting))


    rows = sqlComs.getRowFromSQL(sql)

    return jsonify(rows=rows)


@app.route('/sort', methods=['GET', 'POST'])
def switchDep():
    CFs = sqlComs.getCF(GlobalVals.DepthChartOption)
    LFs = sqlComs.getLF(GlobalVals.DepthChartOption)
    RFs = sqlComs.getRF(GlobalVals.DepthChartOption)
    SSs = sqlComs.getSS(GlobalVals.DepthChartOption)
    secBs = sqlComs.get2B(GlobalVals.DepthChartOption)
    thirdBs = sqlComs.get3B(GlobalVals.DepthChartOption)
    firstBs = sqlComs.get3B(GlobalVals.DepthChartOption)
    Cs = sqlComs.get3B(GlobalVals.DepthChartOption)
    Ps = sqlComs.get3B(GlobalVals.DepthChartOption)
    jsonify(CFs=CFs, LFs=LFs, RFs=RFs, SSs=SSs, secBs=secBs, thirdBs=thirdBs,
            firstBs=firstBs, Cs=Cs, Ps=Ps)
