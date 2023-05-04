# file: app.py

import sys
sys.path.insert(0, '..')
from flask import Flask, render_template, session, redirect, url_for, request, g
from datetime import timedelta
import os
from models.userAuthService import *
from models.workOrderService import *
import json



app = Flask(__name__, template_folder='../templates')
app.secret_key = 'laalaaland'
app.config['SECRET_KEY'] = 'laalaaland'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=1800)

publicRoutes = ['/login', '/about', '/contact', '/forms/user/add' , '/api/user/add']
adminRoutes = ['/forms/userAuth/update', '/api/userAuth/update']


@app.before_request
def launch():
    if (request.path not in publicRoutes) and (not session.get("user_id", "")): return redirect(url_for("routeLogin"))
    g.userAuth:UserAuthInterface = UserAuthService()
    g.workOrders: WorkOrderServiceInterface = WorkOrderService()
    None


@app.context_processor
def templateData():
    items = g.workOrders.getAllWorkOrders()
    allWorkOrders = [json.loads(order) for order in items]

    appData = dict(

    session = session.get("user_id", ""),
    userAuthId = UserAuthService().getUserAuthName(session),
    userAuthData = UserAuthService().getUserAuthData(session) if session.get("user_id", "") else "",
    allWorkOrders = allWorkOrders


    )
    return appData
######################################## public routes

@app.route("/login")
def routeLogin():
    return (render_template('login.html') if not session.get("user_id", "") else redirect(url_for('routeLanding')))

@app.route("/login", methods=["POST"])
def routeCheckLogin():
    return (redirect (url_for('routeLanding')) if (g.userAuth.checkLogin(request, session)) else redirect(url_for('routeLogin')))

@app.route("/about")
def routeAbout():
    return render_template('about.html')

@app.route("/contact")
def routeContact():
    return render_template('contact.html')

@app.route("/logout")
def routeLogout():
    session.pop('user_id', None)
    return redirect(url_for("routeLogin"))

@app.route("/forms/user/add")
def routeAddUserAuthForm():
    return render_template('AddUser.html')

@app.route("/api/user/add", methods=['POST'])
def routeApiAddUserAuth():
    if not (request.form['password'] == request.form['password-verify']): return redirect (url_for('routeAddUserAuthForm'))
    if (g.userAuth.addUserAuth(request)):
        return redirect(url_for('routeLogin')) 
    else:
        return redirect(url_for('routeAddUserAuthForm'))
    
######################################### private routes

@app.route("/")
def routeLanding():
    # return (render_template(url_for('routeLogin')) if not session.get("user_id", "") else redirect(url_for('routeMenu')))
    # connection = psycopg2.connect(host=os.getenv("PGHOST"), user=os.getenv("PGUSER"), password=os.getenv("PGPASSWORD"), port=os.getenv("PGPORT"), dbname=os.getenv("PGDATABASE"))
    return render_template('workorders.html')


######################################### admin routes ################################################


@app.route("/forms/userAuth/update")
def routeUpdateUserAuthForm():
    return render_template('updateUsers.html', allUserAuthData = g.userAuth.getAllUserAuthData())

@app.route("/api/userAuth/update", methods=['POST'])
def routeUpdateUserAuthApi():
    g.userAuth.updateAllUserAuthData(request)
    return  redirect(url_for('routeUpdateUserAuthForm'))


@app.route("/api/user/delete", methods=['POST'])
def routeDeleteUserAuthApi():
    g.userAuth.deleteUserAuthData(request)
    return  redirect(url_for('routeUpdateUserAuthForm'))
    

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
