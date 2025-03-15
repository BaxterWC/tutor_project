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
    user_name = None

    if 'user_id' in session:
        con = connect_to_database(DATABASE)
        cur = con.cursor()
        query = "SELECT fname FROM user WHERE user_id = ?"
        cur.execute(query, (session['user_id'],))
        guy = cur.fetchone()
        con.close()

        if guy:
            user_name = guy[0]

    return render_template('home.html', user_name=user_name)

@app.route('/schedule')
def render_schedule():  # put application's code here
    con = connect_to_database(DATABASE)
    cur = con.cursor()
    query = """
           SELECT sessions.date, sessions.time, sessions.subject, user.fname || ' ' || user.lname AS tutor_name, sessions.location
           FROM sessions
           JOIN user ON sessions.tutor_id = user.user_id
           ORDER BY sessions.date, sessions.time;
       """

    cur.execute(query)
    sessions = cur.fetchall()
    con.close()

    session_list = [{'date': s[0], 'time': s[1], 'subject': s[2], 'tutor_name': s[3], 'location': s[4]} for s in
                    sessions]

    return render_template('schedule.html', sessions=session_list)


@app.route('/signup', methods=['POST', 'GET'])
def render_signup():  # put application's code here
    if request.method == 'POST':
        fname = request.form.get('user_fname').title().strip()
        lname = request.form.get('user_lname').title().strip()
        email = request.form.get('user_email').lower().strip()
        password = request.form.get('user_password')
        password2 = request.form.get('user_password2')
        role = request.form.get('user_role')

        if password != password2:
            return redirect("\signup?error=passwords+do+not+match")

        if len(password) < 8:
            return redirect("\signup?error=password+is+too+short")

        con = connect_to_database(DATABASE)
        quer_insert = "INSERT INTO user(fname, lname, email, password, role) VALUES (?, ?, ?, ?, ?)"
        cur = con.cursor()
        query1 = "SELECT email FROM user"
        cur.execute(query1)
        all_emails = cur.fetchall()
        if (email,) in all_emails:
            return redirect("\signup?error=email+already+in+use")
        cur.execute(quer_insert, (fname, lname, email, password, role))
        con.commit()
        con.close()

    return render_template('signup.html')


@app.route('/login', methods=['POST', 'GET'])
def render_login_page():
    if request.method == 'POST':
        email = request.form.get('user_email').lower().strip()
        password = request.form.get('user_password')

        con = connect_to_database(DATABASE)
        if con:
            cur = con.cursor()
            query = "SELECT user_id, email, password, fname FROM user WHERE email = ?"
            cur.execute(query, (email,))
            user_info = cur.fetchone()
            con.close()

            if user_info:

                if user_info[2] == password:
                    session['user_id'] = user_info[0]
                    session['email'] = user_info[1]
                    session['fname'] = user_info[3]
                    return redirect("/")

        return redirect("\login?error=invalid+credentials")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")


@app.route('/create_session', methods=['POST', 'GET'])
def create_session():
    if 'user_id' not in session:
        return redirect("\login?error=Please+log+in")

    con = connect_to_database(DATABASE)
    cur = con.cursor()

    cur.execute("SELECT role FROM user WHERE user_id = ?", (session['user_id'],))
    role = cur.fetchone()

    if role[0] == 'Tutor':
        if request.method == 'POST':
            subject = request.form.get('subject')
            date = request.form.get('date')
            time = request.form.get('time')
            location = request.form.get('location')

            query = "INSERT INTO sessions (tutor_id, subject, date, time, location) VALUES (?, ?, ?, ?, ?)"
            cur.execute(query, (session['user_id'], subject, date, time, location))
            con.commit()
            con.close()
            return redirect("/schedule")
    else:
        return redirect("\schedule?error=Only+tutors+can+create+sessions")
    con.close()

    return render_template('create_session.html')

if __name__ == '__main__':
    app.run()
