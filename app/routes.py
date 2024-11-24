from sqlalchemy import false

from app import app
import mariadb
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_wtf.csrf import CSRFProtect
from app.forms import LoginForm, DisplayForm
from app import teams

valid = 'false'

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
            return redirect('/showTeams')


    return render_template('roster.html',form=form)


def getRowFromSQL(sql):
    conn = connect()

    cur = conn.cursor()

    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows


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
    return render_template('index.html', rows=rows )



@app.route('/process_team_change', methods=['POST'])
def process_team_change():
    team_name = request.form['teamName']
    # Process the team change, e.g., fetch relevant data
    response_data = team_name
    print('DID IT')
    return jsonify(response_data)




@app.route('/showTeams', methods=['GET', 'POST'])
def showTeams():

    if(valid == 'false'):
        return redirect(url_for('startPage'))

    submit = request.form.get('submit', None)

    form = DisplayForm()


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
    return render_template('showTeams.html', title='Sign In', form=form, choices=teams.teams)