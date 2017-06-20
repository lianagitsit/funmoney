# FunMoney

Visit the app live at: https://funmoney.herokuapp.com/



# Helpful tips for development: 

==========Startup Instructions==========

> To start virtual environment:

. venv/bin/activate

> To start flask in debug mode:

export FLASK_APP=app.py 

export FLASK_DEBUG=1 

flask run

> To exit:

venv deactivate


=========Eric tips for Heroku etc.==========

(0) Install virtualenv

sudo pip install virtualenv

virtualenv venv

Turn on the virtual env (below)

Install Flask and dependencies WITH VENV ON:

pip install Flask

pip install Flask-SQLAlchemy

pip install psycopg2

(0.5) Ensure postgres is installed and running

(0.6) Create the SQL database (see below)

(0.7) Import DB to create all after running python

(ensure virtual environment is started)

from yourapplication import db

db.create_all()


(1) Turn on the virtual environment:

. venv/bin/activate

(2) Turn /off/ the virtual environment:

deactivate

Installation Steps:

1. Turn on venv, then pip install flask

postgres setup URL adapted from: 

https://www.theodo.fr/blog/2017/03/developping-a-flask-web-app-with-a-postresql-database-making-all-the-possible-errors/

postgres commands used:

sudo -i -u postgres psql

postgres=# ALTER USER postgres WITH ENCRYPTED PASSWORD

'password';

postgres=# CREATE DATABASE my_database;

DEPLOY AN APP:

(0) Get Gunicorn

-> Run app w/ 

gunicorn via gunicorn app:app 

(0.5)

requirements.txt file in root will create a dependency thingy. Create one with pip freeze to requirements.txt. 

pip freeze > requirements.txt

(1) Log in to heroku

heroku login

(2) Create an app to prepare reception 

heroku create [appname]


(3) Push to heroku

git add *

git commit -m "version to deploy to heroku"

git push heroku master

For your own:

(1) Define a proc file like:

web: gunicorn gettingstarted.wsgi --log-file -

MY TEST: web gunicorn app:app

Dynos can scale it up! 



If you just cloned an ap and want it to run locally, use pip install -r requirements.txt to install teh requirements

(2) Set heroku up for postgres

heroku addons:create heroku-postgresql:hobby-dev

(mine this time) postgresql-closed-41978

To establish a remote session witgh the DB:

heroku pg:psql

=====

The ultimate copy shenanigan: Run as a normal command line command

PGUSER=postgres PGPASSWORD=password heroku pg:push funmoney postgresql-closed-41978 --app funmoney

^ THAT WILL WORK ^ 

AFter setting edit privs to md5 via

sudo nano /etc/postgresql/9.5/main/pg_hba.conf

And then 

sudo service postgresql restart