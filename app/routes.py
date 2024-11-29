from cgi import print_form
from traceback import print_tb

from sqlalchemy import false, true

from app import app
import mariadb

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from app import teams
from app.DatabaseConnection import mysql
from app.GlobalVals import valid
from app.forms import LoginForm, DisplayForm, TeamForm, RegisterForm, DepthForm
from app import sqlComs
from app import GlobalVals




@app.route('/', methods=['GET', 'POST'])
def startPage():
    print("hi")

    form = LoginForm()

    if form.validate_on_submit():
        print("worked")
        user = sqlComs.getUser(form.username.data,form.username.data)

        print(user)
        if (user != []):

            GlobalVals.valid = 'true'
            print()
            return redirect('/showTeams')

    return render_template('index.html', form=form)



@app.route('/player')
def player():
    player_id = request.args.get('player', 'No')
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID
    sql = 'Select * FROM people WHERE playerid = \'' + player_id + '\''

    rows = sqlComs.getRowFromSQL(sql)

    sql = ('Select sum(b_G),sum(b_AB),sum(b_R),sum(b_h),sum(b_2b),sum(b_3b),sum(b_HR),sum(b_SB)'
           ' ,sum(b_SO),sum(b_IBB),sum(b_hbp),sum(b_SH),sum(b_SF), round(sum(b_H)*100/sum(b_ab)) '
           ',round(sum(b_R)*100/sum(b_AB)), round(sum(b_hr)*100/sum(b_AB),0) from batting where playerid= \'' + player_id + '\'')
    battingRows = sqlComs.getRowFromSQL(sql)
    sql = ('SELECT SUM(p_W), SUM(p_L), SUM(p_G), SUM(p_GS), SUM(p_CG), SUM(p_SHO), SUM(p_SV), SUM(p_H), SUM(p_HR) '
           ' ,SUM(p_BB), SUM(p_SO), round(AVG(p_BAOpp),2), round(AVG(p_ERA),2), SUM(p_IBB), SUM(p_WP), SUM(p_HBP), SUM(p_BK), MAX(p_BFP)'
           ', SUM(p_R), SUM(p_SH), SUM(p_SF), CASE WHEN SUM(p_L) = 0 THEN NULL ELSE round(CAST(SUM(p_W) AS FLOAT) / SUM(p_L),2) END FROM pitching WHERE playerid = \'') + player_id + '\''
    pitchingRows = sqlComs.getRowFromSQL(sql)
    sql = 'SELECT SUM(f_G), SUM(f_GS), SUM(f_PO), SUM(f_A), SUM(f_E), SUM(f_DP), SUM(f_PB), SUM(f_SB), SUM(f_CS), AVG(f_ZR) FROM fielding WHERE playerid = \'' + player_id + '\''
    fieldingRows = sqlComs.getRowFromSQL(sql)

    sql = 'SELECT Distinct Position FROM fielding WHERE playerid = \'' + player_id + '\''
    positions = sqlComs.getRowFromSQL(sql)


    sql = 'Select sum(manager_G),sum(manager_W),sum(manager_L) FROM managers WHERE playerid = \'' + player_id + '\''
    managerRows = sqlComs.getRowFromSQL(sql)

    sql = 'Select Distinct team_name FROM managers join teams using(teamId) WHERE playerid = \'' + player_id + '\''
    teamsManaged = sqlComs.getRowFromSQL(sql)

    sql = 'Select inducted from hallofFame where inducted = \'Y\' AND playerid = \'' + player_id + '\''
    halloffame = sqlComs.getRowFromSQL(sql)

    return render_template('playerStats.html', rows=rows,battingRows=battingRows,pitchingRows=pitchingRows,
                           fieldingRows=fieldingRows,positions=positions,managerRows=managerRows,teamsManaged=teamsManaged,
                           halloffame=halloffame)

@app.route('/team/roster')
def index():
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID
    print("roster")
    rows = sqlComs.getRoster(team_name, year_id)

    return render_template('webPage/mainPage.html', rows=rows)

@app.route('/team/Batting-Stats')
def battingStats():
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID
    print("batting")
    sql = ('SELECT nameFirst, nameLast, b_ab,b_r,b_h,b_2b,b_3b,b_hr,b_RBI,b_SB,b_CS,b_BB,b_SO,b_sh,b_SF' +
           ' FROM batting NATURAL JOIN TEAMS NATURAL JOIN people WHERE team_name = '
           + '\'' + team_name + '\'  AND yearid = ' + year_id + ' Group By playerID,yearID;')
    rows = sqlComs.getRowFromSQL(sql);


    return render_template('webPage/BattingStats.html', rows=rows)


@app.route('/team/Pitching-Stats')
def pitchingStats():
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID
    sql = ('SELECT nameFirst, nameLast, p_GS,p_CG,p_SHO,p_IPOuts,p_H,p_Er,p_HR,p_BB,p_SO,p_BAOpp,p_ERA,p_IBB,p_HBP,p_GF' +
            ' FROM pitching NATURAL JOIN TEAMS NATURAL JOIN people WHERE team_name = '
            + '\'' + team_name + '\'  AND yearid = ' + year_id + ' Group By playerID,yearID;')
    rows = sqlComs.getRowFromSQL(sql)
    print("pitching")

    return render_template('webPage/PitchingStats.html', rows=rows)

@app.route('/team/Fielding')
def Fielding():
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID
    sql = ('SELECT nameFirst, nameLast, f_G,f_GS,f_InnOuts,f_PO,f_A,f_E,f_DP,f_PB,f_SB,f_CS,f_ZR FROM Fielding NATURAL JOIN TEAMS NATURAL JOIN people WHERE team_name = '
           + '\'{}\'  AND yearid = {} Group By playerID,yearID;'.format(team_name, year_id))
    print(sql)
    rows = sqlComs.getRowFromSQL(sql)
    print("fielding")

    return render_template('webPage/Fielding.html', rows=rows)


@app.route('/team/Depth-Chart', methods=['GET', 'POST'])
def DepthChart():
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID
    print("depth")
    form = DepthForm()
    posting = 'false'
    if request.method == 'POST':
        print("depth OPTION KID")
        if 'option' in request.form:
            option = request.form.get('option', None)
            GlobalVals.DepthChartOption = option
            print("OPTION: " + option)

    if not form.is_submitted():
        form.depth_dropdown.data = GlobalVals.DepthChartOption

    print(GlobalVals.DepthChartOption)
    CFs = sqlComs.getCF(GlobalVals.DepthChartOption)
    LFs = sqlComs.getLF(GlobalVals.DepthChartOption)
    RFs = sqlComs.getRF(GlobalVals.DepthChartOption)
    SSs = sqlComs.getSS(GlobalVals.DepthChartOption)
    secBs = sqlComs.get2B(GlobalVals.DepthChartOption)
    thirdBs = sqlComs.get3B(GlobalVals.DepthChartOption)
    firstBs = sqlComs.get3B(GlobalVals.DepthChartOption)
    Cs = sqlComs.get3B(GlobalVals.DepthChartOption)
    Ps = sqlComs.get3B(GlobalVals.DepthChartOption)

    return render_template('webPage/DepthChart.html', CFs=CFs, LFs=LFs, RFs=RFs, SSs=SSs, secBs=secBs, thirdBs=thirdBs,
                           firstBs=firstBs, Cs=Cs, Ps=Ps, form=form)

@app.route('/team/Team-Stats', methods = ['GET','POST'])
def TeamStats():
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID
    sql = ('SELECT nameFirst, nameLast, sum(p_SHO),sum(p_IPOuts),sum(p_H),sum(p_SO),ROUND(sum(p_BAOpp)/count(playerid),3),ROUND(sum(p_ERA)/count(playerid),3),sum(p_IBB),sum(p_HBP)'
           ' FROM pitching NATURAL JOIN TEAMS NATURAL JOIN people WHERE team_name = \''+team_name +'\' AND yearID = ' + year_id +' Group BY yearId')

    pitchingRows = sqlComs.getRowFromSQL(sql)
    print(sql)


    sql = ('SELECT nameFirst, nameLast,sum(b_AB),sum(b_R), round(sum(b_R)/sum(b_AB),3),sum(b_h),sum(b_2B),sum(b_3B),sum(b_HR),round(sum(b_HR)/sum(b_AB),3),sum(b_SB),sum(b_BB),sum(b_SO),sum(b_SH),sum(b_SF)'
           ' FROM batting NATURAL JOIN TEAMS NATURAL JOIN people WHERE team_name = \''+team_name +'\' AND yearID = ' + year_id +' Group BY yearId')
    print(sql)

    battingRows = sqlComs.getRowFromSQL(sql)


    sql = ('SELECT nameFirst, nameLast, sum(f_PO),sum(f_A), sum(f_E),sum(f_CS)'
           ' FROM fielding NATURAL JOIN TEAMS NATURAL JOIN people  WHERE team_name = \''+team_name +'\' AND yearID = ' + year_id +' Group BY yearId')
    fieldingRows = sqlComs.getRowFromSQL(sql)


    sql = 'Select wins,round,team_name,yearid From seriespost NATURAL JOIN teams WHERE teams.teamid = teamIdwinner AND round = \'WS\' AND team_name = \'' +  team_name+ '\';'
    WSs = sqlComs.getRowFromSQL(sql)



    if not WSs:  # Set default if empty
        WSs = [['a','b','c','Never Won a World Series']]

    print(WSs[0][3])

    return render_template('webPage/TeamStats.html',pitchingRows=pitchingRows,battingRows=battingRows,fieldingRows=fieldingRows, WSs=WSs)



@app.route('/ImmaculateGridGuesser', methods=['GET', 'POST'])
def ImmacGrid():
    form1 = TeamForm()
    sql = 'SELECT DISTINCT teamID, team_name FROM teams'
    #teams = sqlComs.getRowFromSQL(sql)
    form1.team1.choices = teams.teams  # Assuming you're fetching from a database
    form1.team2.choices = teams.teams  # Assuming you're fetching from a database

    if form1.validate_on_submit():
        print('players kid')
        sql = ('Select DISTINCT nameFirst,nameLast FROM people where playerID IN ' +
               '(SELECT playerID From batting NATURAL JOIN teams WHERE team_name = \'' + form1.team1.data + '\')'
               + 'AND playerID IN ' + '(SELECT playerID From batting NATURAL JOIN teams WHERE team_name = \'' + form1.team2.data + '\')')
        players = sqlComs.getRowFromSQL(sql)
        print(sql)
        return render_template('ImmaculateGrid.html', form1=form1, players=players)

    return render_template('ImmaculateGrid.html', form1=form1, players=[])


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        print('registering')
        sql = """INSERT INTO users(username,password) values( \'""" + form.username.data + """\', \'""" + form.password.data + """\')"""
        print(sql)
        sqlComs.executeInsert(sql)
        return redirect(url_for('startPage'))

    return render_template('register.html', form=form)


@app.route('/showTeams', methods=['GET', 'POST'])
def showTeams():

    if (GlobalVals.valid == 'none'):
        return redirect(url_for('startPage'))

    form = DisplayForm()
    sql = 'SELECT DISTINCT teamID, team_name FROM teams'

    form.team_dropdown.choices = teams.teams

    if form.team_dropdown.data is not None and form.year_dropdown is not None:
        print("here")

        GlobalVals.teamName = form.team_dropdown.data

        GlobalVals.yearID =form.year_dropdown.data
        return redirect(url_for('index' ))



    if request.method == 'POST':
        print('post')
        if 'teamName' in request.form:

            team_name = request.form.get('teamName', None)
            print(team_name)
            # Logic to determine years based on team selection
            sql = "SELECT yearID FROM teams WHERE team_name = '{}'".format(team_name)
            print(sql)
            years = sqlComs.getRowFromSQL(sql)

            form.year_dropdown.choices = years
            return jsonify(years=years)

    if request.method == 'GET':
        print('get')


    print("follow")
    print(form.team_dropdown.data)
    return render_template('showTeams.html', title='Sign In', form=form, choices=teams)





@app.route('/logout', methods=['GET', 'POST'])
def logout():
    data = request.get_json()

    if data and data.get('action') == 'logout':
        print('logging out for real this time')
        GlobalVals.valid = 'true'
        return redirect( url_for('startPage'))


@app.route('/sort', methods=['GET', 'POST'])
def sort():
    print('Sorting')
    data = request.get_json()
    baseballRole = data.get('type')
    sorting = data.get('action')
    stat = data.get('stat')
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID
    print(baseballRole)
    print(sorting)
    print(stat)

    if(baseballRole == 'pitching'):
        sql = ('SELECT nameFirst, nameLast, p_GS, p_CG, p_SHO, p_IPOuts, p_H, p_ER, p_HR, p_BB, p_SO, p_BAOpp, p_ERA, p_IBB, p_HBP, p_GF '
            'FROM {} NATURAL JOIN TEAMS NATURAL JOIN people WHERE team_name = \'{}\' AND yearid = {} '
            'GROUP BY playerID, yearID ORDER BY {} {}'.format(baseballRole, team_name, year_id, stat, sorting))
    elif(baseballRole == 'batting'):
        sql = ('SELECT nameFirst, nameLast, b_ab,b_r,b_h,b_2b,b_3b,b_hr,b_RBI,b_SB,b_CS,b_BB,b_SO,b_sh,b_SF '
               'FROM {} NATURAL JOIN TEAMS NATURAL JOIN people WHERE team_name = \'{}\' AND yearid = {} '
               'GROUP BY playerID, yearID ORDER BY {} {}'.format(baseballRole, team_name, year_id, stat, sorting))
    elif (baseballRole == 'fielding'):
        sql = ('SELECT nameFirst, nameLast, f_G,f_GS,f_InnOuts,f_PO,f_A,f_E,f_DP,f_PB,f_SB,f_CS,f_ZR '
               'FROM {} NATURAL JOIN TEAMS NATURAL JOIN people WHERE team_name = \'{}\' AND yearid = {} '
               'GROUP BY playerID, yearID ORDER BY {} {}'.format(baseballRole, team_name, year_id, stat, sorting))

    print(sql)
    rows = sqlComs.getRowFromSQL(sql)
    print(rows)
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