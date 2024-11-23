from app import app
import mariadb
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, flash, session
from app.forms import LoginForm
from app import teams


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
    # if conn.is_connected():
    #     print('Connected to MariaDB database')
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT playerID FROM people LIMIT 10")
    #
    #     rows = cursor.fetchall()
    #     print('Total number of rows in table:', cursor.rowcount)
    #
    #     for row in rows:
    #         print(row)
    # else:
    #     print('Failed to connect to MariaDB')

@app.route('/')
def roster():

    print("hi")

    return render_template('roster.html')


def getRoster(teamName, yearID):
    conn = connect()

    cur = conn.cursor()

    cur.execute(
        'SELECT DISTINCT nameFirst,nameLast FROM people p, batting b,teams t WHERE b.playerId = p.playerId AND b.teamID = t.teamID AND t.team_name = \'' + teamName+'\' AND b.yearID = '+yearID+' ORDER BY p.playerId ASC')
    rows = cur.fetchall()
    conn.close()
    return rows



@app.route('/index')
def index():
    team_name = request.args.get('teamName')
    year_id = request.args.get('yearID')
    print("we got this")
    rows = getRoster(team_name, year_id)
    print(rows)
    return render_template('index.html', rows=rows )




@app.route('/showTeams', methods=['GET', 'POST'])
def login():
    choice = request.form.get('choiceDropdown')
    form = LoginForm()
    print(form)


    if form.validate_on_submit():
        print(choice)
        print("here")
        return redirect(url_for('index', teamName=choice, yearID=form.password.data))


    return render_template('login.html', title='Sign In', form=form, choices=teams.teams)