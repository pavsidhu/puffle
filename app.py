from flask import Flask, render_template, g, request, session, redirect, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config.from_object(__name__)

app.config['DATABASE'] = 'database.db'
app.config['SECRET_KEY'] = 'i1507802m1965d55a5d987c855ad5dc912c23e8a6248w464'

def connectDB():
    return sqlite3.connect(app.config['DATABASE'])

@app.route('/register', methods=['POST', 'GET'])
def register():
    try:
        session['id'] = session['id']
        return redirect('/')
    except:
        pass

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            g.db = connectDB()

            cur = g.db.execute("SELECT * FROM Accounts")
            usernames = [row[1] for row in cur.fetchall()]
            exists = False
            for x in usernames:
                if x == username and exists == False:
                    flash('Username already exists!')
                    exists = True

            if not exists:
                cur = g.db.execute("INSERT INTO Accounts (username, password) VALUES ('{}', '{}')".format(username, password))
                g.db.commit()

                cur = g.db.execute("SELECT * FROM Accounts WHERE username='{}' AND password='{}'".format(username, password))
                account = [dict(id=row[0], username=row[1], password=row[2]) for row in cur.fetchall()]
                session['id'] = account[0]['id']
                session['username'] = account[0]['username']
                g.db.close()
        except:
            g.db.close()
            flash('There was an error, please try again.')
        return redirect('/')

    return render_template('login.html', page='register')


@app.route('/login', methods=['POST', 'GET'])
def login():
    try:
        session['id'] = session['id']
        return redirect('/')
    except:
        pass

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            g.db = connectDB()
            cur = g.db.execute("SELECT * FROM Accounts WHERE username='{}' AND password='{}'".format(username, password))
            account = [dict(id=row[0], username=row[1], password=row[2]) for row in cur.fetchall()]
            session['id'] = account[0]['id']
            session['username'] = account[0]['username']
            g.db.close()
            print 2
        except:
            g.db.close()
            print 1
            flash('Your details are incorrect')

    return render_template('login.html', page='login')

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return redirect('/login')

@app.route('/')
def main():
    try:
        session['happiness'] = session['happiness']
    except:
        session['happiness'] = 3

    try:
        session['id'] = session['id']
    except:
        return redirect('/login')

    g.db = connectDB()
    cur = g.db.execute("SELECT * FROM Tasks WHERE userID={}".format(session['id']))
    tasks = [dict(task=row[1], deadline=row[2]) for row in cur.fetchall()]
    g.db.close()

    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST', 'GET'])
def add():
    g.db = connectDB()
    date = datetime.now()
    task = request.form['task']
    deadline = request.form['deadline']
    cur = g.db.execute("INSERT INTO Tasks (task, deadline, userID) VALUES ('{}', '{}', '{}')".format(task, deadline, session['id']))
    g.db.commit()
    g.db.close()
    return redirect('/')

@app.route('/badpage')
def badPage():
    session['happiness'] -= 1

    g.db = connectDB()
    cur = g.db.execute("SELECT * FROM Tasks WHERE userID={}".format(session['id']))
    tasks = [dict(task=row[1], deadline=row[2]) for row in cur.fetchall()]
    g.db.close()

    return render_template('index.html', badpage=True, tasks=tasks)


if __name__ == '__main__':
	app.run(debug=True)
