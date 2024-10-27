from app import app
import mariadb
import mysql.connector
from flask import render_template


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
@app.route('/index')
def index():

    print("hi")
    conn = connect()

    cur = conn.cursor()

    cur.execute('SELECT nameFirst,nameLast FROM people p, batting b WHERE b.playerId = p.playerId AND b.teamID = \'det\' AND b.yearID = 2019 ORDER BY p.playerId ASC')
    rows = cur.fetchall()
    conn.close()

    firstName = {'id': rows[0][0]}
    lastName = {'id': rows[0][1]}
    user = {'username': firstName}

    posts = rows
    print(posts)
    return render_template('roster.html', firstName=firstName, lastName=lastName,
                            user = user, rows = rows)