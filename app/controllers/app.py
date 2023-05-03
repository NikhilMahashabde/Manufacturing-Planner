# file: app.py

import sys
sys.path.insert(0, '..')
from flask import Flask, render_template, session, redirect, url_for, request, g
from datetime import timedelta
import os
from models.userAuthService import *

app = Flask(__name__, template_folder='../templates')
app.secret_key = 'laalaaland'
app.config['SECRET_KEY'] = 'laalaaland'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=20)

publicRoutes = ['/login', '/about', '/contact']

@app.context_processor
def templateData():
    appData = dict(

    session = session.get("user_id", ""),
    userAuthId = UserAuthService().getUserAuthName(session),
    userAuthData = UserAuthService().getUserAuthData(session) if session.get("user_id", "") else ""
    )
    return appData

@app.before_request
def launch():
    if (request.path not in publicRoutes) and (not session.get("user_id", "")): return redirect(url_for("routeLogin"))
    g.userAuth:UserAuthInterface = UserAuthService()
    None

######################################## public routes

@app.route("/login")
def routeLogin():
    return (render_template('login.html') if not session.get("user_id", "") else redirect(url_for('routeLanding')))

@app.route("/login", methods=["POST"])
def routeCheckLogin():
    return (redirect (url_for('routeMenu')) if (g.userAuth.checkLogin(request, session)) else redirect(url_for('routeLogin')))

@app.route("/about")
def routeAbout():
    return render_template('about.html')

@app.route("/contact")
def routeContact():
    return render_template('contact.html')

######################################### private routes

@app.route("/")
def routeLanding():
    # return (render_template(url_for('routeLogin')) if not session.get("user_id", "") else redirect(url_for('routeMenu')))
    # connection = psycopg2.connect(host=os.getenv("PGHOST"), user=os.getenv("PGUSER"), password=os.getenv("PGPASSWORD"), port=os.getenv("PGPORT"), dbname=os.getenv("PGDATABASE"))
    return render_template('index.html')


# @app.route('/')
# def index():
#     # connection = psycopg2.connect(host=os.getenv("PGHOST"), user=os.getenv("PGUSER"), password=os.getenv("PGPASSWORD"), port=os.getenv("PGPORT"), dbname=os.getenv("PGDATABASE"))
#     connection = psycopg2.connect(os.getenv("DATABASE_URL"))
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM userauth;")
#     results = cursor.fetchall()
#     connection.close()
#     return f"{results[0]}"

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
