from app import app
import mariadb
import mysql.connector


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

    cur.execute('SELECT nameFirst,nameLast FROM people WHERE nameFirst = \'babe\' AND nameLast = \'ruth\'  LIMIT 10')
    rows = cur.fetchall()
    conn.close()

    firstName = {'id': rows[0][0]}
    lastName = {'id': rows[0][1]}

    return '''
<html>
    <head>
        <title>Home Page - Microblog</title>
    </head>
    <body>
    <p> hi ''' + firstName['id']+'''  '''+ lastName['id']  + '''</p>
    
    </body>
</html>'''