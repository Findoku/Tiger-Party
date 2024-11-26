from cgi import print_form
from traceback import print_tb

from app import app
import mariadb

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify

from app.DatabaseConnection import mysql
from app.GlobalVals import valid
from app.forms import LoginForm, DisplayForm, TeamForm, RegisterForm
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

@app.route('/team/Positions')
def Positions():
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID
    print("positions")
    rows = sqlComs.getRoster(team_name, year_id)

    return render_template('webPage/Positions.html', rows=rows)

@app.route('/team/Depth-Chart')
def DepthChart():
    team_name = GlobalVals.teamName
    year_id = GlobalVals.yearID
    print("depth")
    rows = sqlComs.getRoster(team_name, year_id)

    return render_template('webPage/DepthChart.html', rows=rows)


@app.route('/ImmaculateGridGuesser', methods=['GET', 'POST'])
def ImmacGrid():
    form1 = TeamForm()
    sql = 'SELECT DISTINCT teamID, team_name FROM teams'
    teams = sqlComs.getRowFromSQL(sql)
    form1.team1.choices = [(team[1], team[1]) for team in teams]  # Assuming you're fetching from a database
    form1.team2.choices = [(team[1], team[1]) for team in teams]  # Assuming you're fetching from a database

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
    teams = sqlComs.getRowFromSQL(sql)
    form.team_dropdown.choices = [(team[1], team[1]) for team in teams]

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
    print(form.year_dropdown.data)
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

    sql = ('SELECT nameFirst, nameLast, p_GS, p_CG, p_SHO, p_IPOuts, p_H, p_ER, p_HR, p_BB, p_SO, p_BAOpp, p_ERA, p_IBB, p_HBP, p_GF '
        'FROM {} NATURAL JOIN TEAMS NATURAL JOIN people WHERE team_name = \'{}\' AND yearid = {} '
        'GROUP BY playerID, yearID ORDER BY {} {}'.format(baseballRole,team_name,year_id, stat, sorting))

    print(sql)
    rows = sqlComs.getRowFromSQL(sql)
    print(rows)
    return jsonify(rows=rows)
