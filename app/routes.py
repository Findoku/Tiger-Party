from cgi import print_form

from app import app
import mariadb

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify

from app.forms import LoginForm, DisplayForm, TeamForm, RegisterForm
from app import teams

valid = 'false'

def connect():
    print("s")
    conn = mariadb.connect(
        host='localhost',
        user='root',
        password='bob',
        port=3306,
        database='baseball'
    )

    return conn
@app.route('/', methods=['GET', 'POST'])
def startPage():

    print("hi")

    form=LoginForm()

    if form.validate_on_submit():
        print("worked")

        sql = ('SELECT username,password FROM users WHERE username = \'' + form.username.data + '\' '
               + ' AND password = \'' + form.password.data + '\'')
        rows = getRowFromSQL(sql)
        print(rows)
        if(rows != []):
            global valid
            valid = 'true'
            print()
            return redirect('/showTeams')


    return render_template('index.html', form=form)


def getRowFromSQL(sql):
    conn = connect()

    cur = conn.cursor()

    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows

def executeInsert(sql):
    conn = connect()

    cur = conn.cursor()

    cur.execute(sql)
    conn.commit()
    conn.close()


def getRoster(teamName, yearID):

    sql = ('SELECT DISTINCT nameFirst,nameLast FROM people p, batting b,teams t'+
           ' WHERE b.playerId = p.playerId AND b.teamID = t.teamID AND t.team_name = \''
           + str(teamName) + '\' AND b.yearID = ' + str(yearID) + ' ORDER BY p.playerId ASC')
    rows = getRowFromSQL(sql)

    return rows



@app.route('/index')
def index():
    team_name = request.args.get('teamName')
    year_id = request.args.get('yearID')
    print("we got this")
    rows = getRoster(team_name, year_id)
    print(rows)
    return render_template('rosterPage.html', rows=rows)



@app.route('/ImmaculateGridGuesser',methods=['GET', 'POST'])
def ImmacGrid():
    form1 = TeamForm()
    sql = 'SELECT DISTINCT teamID, team_name FROM teams'
    teams = getRowFromSQL(sql)
    form1.team1.choices = [(team[1], team[1]) for team in teams]  # Assuming you're fetching from a database
    form1.team2.choices = [(team[1], team[1]) for team in teams]  # Assuming you're fetching from a database

    if form1.validate_on_submit():
        print('players kid')
        sql = ('Select DISTINCT nameFirst,nameLast FROM people where playerID IN ' +
               '(SELECT playerID From batting NATURAL JOIN teams WHERE team_name = \'' + form1.team1.data + '\')'
               + 'AND playerID IN ' + '(SELECT playerID From batting NATURAL JOIN teams WHERE team_name = \'' + form1.team2.data + '\')')
        players = getRowFromSQL(sql)
        print(sql)
        return render_template('ImmaculateGrid.html',form1=form1, players=players)



    return render_template('ImmaculateGrid.html', form1=form1, players=[])

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        print('registering')
        sql = """INSERT INTO users(username,password) values( \'""" + form.username.data + """\', \'"""+ form.password.data +"""\')"""
        print(sql)
        executeInsert(sql)
        return redirect(url_for('startPage'))

    return render_template('register.html', form = form)

@app.route('/showTeams', methods=['GET', 'POST'])
def showTeams():

    if(valid == 'false'):
        return redirect(url_for('startPage'))

    form = DisplayForm()
    sql = 'SELECT DISTINCT teamID, team_name FROM teams'
    teams = getRowFromSQL(sql)
    form.team_dropdown.choices = [(team[1], team[1]) for team in teams]


    if form.team_dropdown.data is not None and form.year_dropdown is not None:
        print("here")
        return redirect(url_for('index', teamName=form.team_dropdown.data, yearID=form.year_dropdown.data))

    if request.method == 'POST':
        if 'teamName' in request.form:
            selected_team = request.form.get('team_dropdown')
            team_name = request.form.get('teamName', None)
            print(team_name)
            # Logic to determine years based on team selection
            sql = "SELECT yearID FROM teams WHERE team_name = '{}'".format(team_name)
            print(sql)
            years = getRowFromSQL(sql)
            print(years)
            form.year_dropdown.choices = years
            return jsonify(years=years)


    print("follow")
    print(form.team_dropdown.data)
    print(form.year_dropdown.data)
    return render_template('showTeams.html', title='Sign In', form=form, choices=teams)