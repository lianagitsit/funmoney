
from flask import Flask, render_template, redirect, url_for, session, escape, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# import the quote and other helper functions
import helperfunctions

# Save the module in a more friendly way for later use
get_quote = helperfunctions.get_quote
get_stock_list = helperfunctions.get_stock_list

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

# If running locally, use local DB. If running on heroku, use its DB.
if (os.environ.get('DATABASE_URL') is None):
    # print("Heyo! No database URL!")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
else:
    # print("Using heroku DBURL lolollll this will totally work")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Secret key used for sessions
app.secret_key = 'A0Za98j/3yX R~XHH!jmN]LWX/,?RT'

class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))
    cash = db.Column(db.Float)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cash = 10000

    def __repr__(self):
        return '<User: %r>' % self.username

class Portfolio(db.Model):
    __tablename__ = 'Portfolio'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    stock_name = db.Column(db.String(80))
    stock_ticker = db.Column(db.String(80))
    shares = db.Column(db.Integer)

    def __init__(self, user_id, stock_ticker, stock_name, shares):
        self.user_id = user_id
        self.stock_ticker = stock_ticker
        self.stock_name = stock_name
        self.shares = shares

    def __repr__(self):
        return '<User: %r>' % self.user_id

class Transactions(db.Model):
    __tablename__ = 'Transactions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    stock_name = db.Column(db.String(80))
    stock_ticker = db.Column(db.String(80))
    price = db.Column(db.Float)
    shares = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime())

    def __init__(self, user_id, stock_name, stock_ticker, price, shares):
        self.user_id = user_id
        self.stock_name = stock_name
        self.stock_ticker = stock_ticker
        self.price = price
        self.shares = shares
        self.timestamp = datetime.utcnow()

    def __repr__(self):
        return '<User: %r>' % self.user_id

@app.route('/jsonquote/<string:ticker>', methods=['GET'])
def jsonquote(ticker):
    ticker = ticker.upper()
    return jsonify(get_quote(ticker))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'GET':
        # Return an error if not logged in
        if 'username' not in session:
            return redirect(url_for('login'))
        # Only admin accounts can log in
        if session['username'] == 'admin' or session['username'] == 'Eric' or session['username'] == 'liana':
            users = Users.query.all()
            portfolio = Portfolio.query.all()
            transactions = Transactions.query.all() 
            return render_template('admin.html', users=users, portfolio=portfolio, transactions=transactions)
        return redirect(url_for('index'))
    
    # POST method for delete user feature
    if request.method == 'POST':
        users = Users.query.all()
        portfolio = Portfolio.query.all()
        transactions = Transactions.query.all()
        delete_user = request.form['delete']
        # print(delete_user)

        for user in users:
            # Error if username doesn't match a user
            if user.username == delete_user:      
                # Delete the user from all relevant tables:
                deaduser = Users.query.filter_by(id=user.id).first()
                deadstocks = Portfolio.query.filter_by(user_id=deaduser.id).all()
                deadtrans = Transactions.query.filter_by(user_id=deaduser.id).all()
                for stock in deadstocks:
                    db.session.delete(stock)
                for trans in deadtrans:
                    db.session.delete(trans)          
                db.session.delete(deaduser)
                db.session.commit()

                # re-render the template after deleting
                users = Users.query.all()
                portfolio = Portfolio.query.all()
                transactions = Transactions.query.all()
                return render_template('admin.html', users=users, portfolio=portfolio, transactions=transactions)
        
        # If we made it through the loop with no match, render an apology
        apology = "no such user found"
        return render_template('apology.html', apology=apology)

        

@app.route('/')
def index():
    if 'username' in session:
        # Get all of the user's stocks
        current_user = Users.query.filter_by(username=escape(session['username'])).first()
        # Safeguard against bugs
        if current_user is None:
                return redirect(url_for('login'))
        my_portfolio = Portfolio.query.filter_by(user_id=current_user.id)
        portfolio_dict_list = []
        # Get current share prices and values for all of user's stocks
        for stock in my_portfolio:
            portfolio_dict_list.append(stock.__dict__)
        for stock in portfolio_dict_list:
            stock["price"] = get_quote(stock["stock_ticker"])["price"]
        stock_total = get_stock_total(my_portfolio)
        return render_template('index.html', current_user=current_user, my_portfolio=portfolio_dict_list, stock_total=stock_total)
    return redirect(url_for('login'))

def get_stock_total(portfolio):
    total = 0
    # Get current share prices and values for all stocks
    for stock in portfolio:
        total += (stock.shares * get_quote(stock.stock_ticker)["price"])
    return total

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        password = request.form['password']
        username = request.form['username']

        if not username:
            apology = "username required"
            return render_template('apology.html', apology=apology)
        
        if not password:
            apology = "password required"
            return render_template('apology.html', apology=apology)

        user = Users.query.filter_by(username=username).first()
        if user is None:
            apology = 'you need to Register!'
            return render_template('apology.html', apology=apology)
            
        else:
            if check_password_hash(user.password, password) == False:
            #confirmpassword = (Users.query.filter_by(username=username).first()).password
            #if password != confirmpassword:
                apology = "incorrect password"
                return render_template('apology.html', apology=apology)
        
            else:
                session['username'] = username
                return redirect(url_for('index'))

    if request.method == 'GET':
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if not username:
            apology = "username required to register"
            return render_template('apology.html', apology=apology)

        if not password:
            apology = "password required to register"
            return render_template('apology.html', apology=apology)

        user = Users.query.filter_by(username=username).first()
        if user is None:
            hashedpass = generate_password_hash(password)
            newuser = Users(request.form['username'], hashedpass)
            db.session.add(newuser)
            db.session.commit()
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        else:
            apology = "username taken"
            return render_template('apology.html', apology=apology)
    
    if request.method == 'GET':
        return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/buy', methods=['GET', 'POST'])
def buy():
    # Return an error if not logged in
    if 'username' not in session:
        return redirect(url_for('login'))
    # check request method - if post:
    if request.method == 'POST':
        # ensure ticker and shares filled in
        ticker = request.form['ticker'].upper()
        shares = request.form['shares']

        if not ticker:
            apology = "stock ticker required"
            return render_template('apology.html', apology=apology)
        if not shares:
            apology = "number of shares required"
            return render_template('apology.html', apology=apology)

        # You can't buy negative shares
        if int(shares) <= 0:
            apology = "you can't buy less than one share"
            return render_template('apology.html', apology=apology)
        
        # calculate proposed trans value
        buyquote = get_quote(ticker)
        cost = buyquote["price"] * int(shares)

        # get user's cash and compare
        user = Users.query.filter_by(username=session['username']).first()
        if cost > user.cash:
            apology = "not enough cash"
            return render_template('apology.html', apology=apology)

        # update cash value in Users
        user.cash -= cost
        db.session.add(user)
        db.session.commit()

        # add trans to Transactions
        transaction = Transactions(user.id, buyquote["name"], buyquote["ticker"], buyquote["price"], shares)
        db.session.add(transaction)
        db.session.commit()

        # check if stock in Portfolio then add or update Portfolio
        # print("User id to filter: " + str(user.id))
        # print("Stock ticker to filter: " + ticker)
        mystock = Portfolio.query.filter_by(user_id=user.id).filter_by(stock_ticker=ticker).first()
        # print("Mystock is: " + str(mystock))
        # stock not in portfolio, create new entry
        if mystock is None:
            newstock = Portfolio(user.id, buyquote["ticker"], buyquote["name"], shares)
            db.session.add(newstock)
            db.session.commit()
        # stock in portfolio, update entry
        else:
            mystock.shares += int(shares)
            db.session.add(mystock)
            db.session.commit()

        # return index
        return redirect(url_for('index'))
  
    if request.method == 'GET':
        stock_list = get_stock_list()
        # get user's cash
        user = Users.query.filter_by(username=session['username']).first()
        return render_template('buy.html', stock_list=stock_list, mycash=user.cash)

@app.route('/sell', methods=['GET', 'POST'])
def sell():

    # Return an error if not logged in
    if 'username' not in session:
        return redirect(url_for('login'))

     # check request method - if post:
    if request.method == 'POST':
        # ensure ticker and shares filled in
        ticker = request.form['ticker'].upper()
        shares = request.form['shares']

        if not ticker:
            apology = "stock ticker required"
            return render_template('apology.html', apology=apology)
        if not shares:
            apology = "number of shares required"
            return render_template('apology.html', apology=apology)
        
        # calculate proposed trans value       
        sellquote = get_quote(ticker)
        cost = sellquote["price"] * int(shares)
        print(cost)
        
        user = Users.query.filter_by(username=session['username']).first()
        mystock = Portfolio.query.filter_by(user_id=user.id).filter_by(stock_ticker=ticker).first()
        
        # stock not in portfolio
        if mystock is None:
            apology = "you do not own this stock"
            return render_template('apology.html', apology=apology)
        
        # shares entered greater than shares owned
        if int(shares) > mystock.shares:
            apology = "you don't own enough shares to sell"
            return render_template('apology.html', apology=apology)
        
        # shares entered negative
        if int(shares) <= 0:
            apology = "you must sell at least one share"
            return render_template('apology.html', apology=apology)
    
        # stock in portfolio, update entry
        else:
            mystock.shares -= int(shares)
            # if total shares = 0, remove stock from Portfolio
            if mystock.shares == 0:
                db.session.delete(mystock)
                db.session.commit()
            else:
                db.session.add(mystock)
                db.session.commit()

        # add to cash value in Users
        user.cash += cost
        db.session.add(user)
        db.session.commit()

        # add negative trans to Transactions
        transaction = Transactions(user.id, sellquote["name"], sellquote["ticker"], sellquote["price"], -int(shares))
        db.session.add(transaction)
        db.session.commit()

        # return portfolio
        return redirect(url_for('index'))

    # if method = get:
    if request.method == 'GET':
        # Get all of the user's stocks
        current_user = Users.query.filter_by(username=session['username']).first()
        my_portfolio = Portfolio.query.filter_by(user_id=current_user.id)
        portfolio_dict_list = []
        # Get current share prices and values for all of user's stocks
        for stock in my_portfolio:
            portfolio_dict_list.append(stock.__dict__)
        for stock in portfolio_dict_list:
            stock["price"] = get_quote(stock["stock_ticker"])["price"]
        # stock_total = get_stock_total(my_portfolio)
        return render_template('sell.html', current_user=current_user, my_portfolio=portfolio_dict_list)

@app.route('/history')
def history():
    # Return an error if not logged in
    if 'username' not in session:
        return redirect(url_for('login'))
    current_user = Users.query.filter_by(username=escape(session['username'])).first()
    transactions = Transactions.query.filter_by(user_id=current_user.id).all()
    return render_template('history.html', transactions=transactions)

# DEPRECATED - functionality duplicated in buy route
@app.route('/quote', methods=['GET', 'POST'])
def quote():
    # Return an error if not logged in
    if 'username' not in session:
        return redirect(url_for('login'))
    stock_list = get_stock_list()
    # POST route is deprecated - app now only does AJAX quotes. 
    if request.method == 'POST':
        userticker = request.form['ticker']
        userquote = get_quote(userticker)
        return render_template('quote.html', userquote=userquote, stock_list=stock_list)
    return render_template('quote.html', userquote=None, stock_list=stock_list)

@app.route('/leaderboard')
def leaderboard():
    # Return an error if not logged in
    if 'username' not in session:
        return redirect(url_for('login'))
    users = Users.query.all()
    user_dict_list = []
    # copy users to list of dictionaries
    for user in users:
        user_dict_list.append(user.__dict__)
    # print(user_dict_list)
    # loop through users
    for user in user_dict_list:
        # get this user's portfolio
        my_portfolio = Portfolio.query.filter_by(user_id=user['id'])
        # get this user's cash
        my_cash = user['cash']
        # get the value of this user's portfolio
        stock_total = get_stock_total(my_portfolio)
        # add (cash + portfolio value) as a key-value pair to this user's dict
        user["assets"] = my_cash + stock_total
    # render template with user's list of dictionaries
    sorted_user_dict_list = sorted(user_dict_list, key=lambda user: user["assets"], reverse=True)
    return render_template('leaderboard.html', users=sorted_user_dict_list)
