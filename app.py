
from flask import Flask, render_template, redirect, url_for, session, escape, request
from flask_sqlalchemy import SQLAlchemy
import os

POSTGRES = {
    'user': 'postgres',
    'pw': 'password',
    'db': 'funmoney',
    'host': 'localhost',
    'port': '5432',
}

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
# %(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lianamancini:n0w a butterfly*@localhost/yournewdb'

# If running locally, use local DB. If running on heroku, use its DB.
if (os.environ.get('DATABASE_URL') is None):
    print("Heyo! No database URL!")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
else:
    print("Using heroku DBURL lolollll this will totally work")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']



app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))
    cash = db.Column(db.Integer)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cash = 10000

    def __repr__(self):
        return '<User: %r>' % self.username

@app.route('/')
def index():
    if 'username' in session:
        current_user = Users.query.filter_by(username=escape(session['username'])).first()
        # return 'Logged in as %s' % escape(session['username'])
        return render_template('index.html', current_user=current_user)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        session['username'] = request.form['username']
        newuser = Users(request.form['username'], request.form['password'])
        db.session.add(newuser)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

app.secret_key = 'A0Za98j/3yX R~XHH!jmN]LWX/,?RT'