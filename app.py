from flask import Flask, render_template, request, redirect, session
import sqlite3
from sqlite3 import Error

DATABASE = "tutor_db"
app = Flask(__name__)
app.secret_key = "secret_key"

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
        query1 = "SELECT email FROM user"
        cur.execute(query1)
        all_emails = cur.fetchall()
        if (email,) in all_emails:
            return redirect("\signup?error=email+already+in+use")
        cur.execute(quer_insert, (fname, lname, email, password))
        con.commit()
        con.close()

    return render_template('signup.html')


@app.route('/login', methods=['POST', 'GET'])
def render_login():  # put application's code here
    if request.method == 'POST':
        email = request.form['user_email'].lower().strip()
        password = request.form['user_password']

        query2 = "SELECT user_id, fname, password FROM user WHERE email = ?"
        con = connect_to_database(DATABASE)
        cur = con.cursor()
        cur.execute(query2, (email, ))
        user_info = cur.fetchall()
        con.close()

        session['user_id'] = user_info[0]
        session['email'] = user_info[1]

        if password in user_info:
            return redirect("home.html")
        else:
            return redirect("\signup?error=email+already+in+use")

    return render_template('login.html')




if __name__ == '__main__':
    app.run()
