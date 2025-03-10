from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def render_home():  # put application's code here
    return render_template('home.html')


@app.route('/schedule')
def render_schedule():  # put application's code here
    return render_template('schedule.html')


@app.route('/login', methods=['POST, GET'])
def render_login():  # put application's code here
    return render_template('login.html')


@app.route('/about')
def render_about():  # put application's code here
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
