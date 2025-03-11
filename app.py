from flask import Flask, render_template, request, redirect
import sqlite3
from sqlite3 import Error

DATABASE = "tutor_db"
app = Flask(__name__)


def connect_to_database(db_file):
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error:
        print("an error has occurred connecting to the database")
    return


@app.route('/')
def render_home():  # put application's code here
    return render_template('home.html')


@app.route('/schedule')
def render_schedule():  # put application's code here
    return render_template('schedule.html')


@app.route('/signup', methods=['POST', 'GET'])
def render_signup():  # put application's code here
    if request.method == 'POST':
        fname = request.form.get('user_fname').title().strip()
        lname = request.form.get('user_lname').title().strip()
        email = request.form.get('user_email').lower().strip()
        password = request.form.get('user_password')
        password2 = request.form.get('user_password2')

        if password != password2:
            return redirect("\signup?error=passwords+do+not+match")

        if len(password) < 8:
            return redirect("\signup?error=password+is+too+short")

        con = connect_to_database(DATABASE)
        quer_insert = "INSERT INTO user(fname, lname, email, password) VALUES (?, ?, ?, ?)"
        cur = con.cursor()
        cur.execute(quer_insert, (fname, lname, email, password))
        con.commit()
        con.close()

    return render_template('signup.html')


@app.route('/login', methods=['POST', 'GET'])
def render_login():  # put application's code here
    return render_template('login.html')


@app.route('/about')
def render_about():  # put application's code here
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
