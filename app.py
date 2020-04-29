from flask import Flask
from flask import *     #Flask, flash, redirect, render_template, request, session, abort
import os
import pyrebase

config = {
    "apiKey" : "AIzaSyAIsSHOuNkfoGuUrJ5xQM2t6jNVT5TlHx8",
    "authDomain" : "cams-da440.firebaseapp.com",
    "databaseURL" : "https://cams-da440.firebaseio.com",
    "projectId" : "cams-da440",
    "storageBucket" : "cams-da440.appspot.com",
    "messagingSenderId" : "592415369968"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

app = Flask(__name__)

global active,credentials
#Firebase
from firebase import firebase
firebase = firebase.FirebaseApplication('https://cams-da440.firebaseio.com/', None)
credentials = firebase.get('/credentials', None)
cutoff = firebase.get('/Cutoff', None)

@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('home.html', cf = cutoff)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.form == 'POST':
        global active
        temp = -1
        username = request.form['uname']
        password = request.form['pass']
        for i in credentials:
            if username in credentials[i]['EmailId'] and password in credentials[i]['Password']:
                temp += 1
                session['logged_in'] = True
                active = username
                if active == 'kaviya@gmail.com':  ##admin
                    return render_template('home_admin.html', u = active)
                else:
                    return render_template('home_user.html', u = active)

        if temp == -1:
            return render_template('login.html', msg = "Invalid Credentials")
    else:
        return render_template('login.html')


@app.route('/register',methods=['POST', 'GET'])
def register():
    if request.method =='POST':
        username = request.form['uname']
        password = request.form['pass']   ## DO IT here
        for i in credentials:
            if username in credentials[i]['EmailId']:
                flash('User with this email already exits :/ ')
                return render_template('register.html')
        else:
            print("Registered user credentials")
            print("Username: ",username)
            print("Password: ",password)
            lenOfCred = len(credentials)
            userId = "CAMS"
            if lenOfCred <= 9:
                k = "000" +str(lenOfCred+1)
            elif lenOfCred >= 10 and lenOfCred <= 99:
                k = "00" +str(lenOfCred+1)
            elif lenOfCred >=100 and  lenOfCred <= 999:
                k = "0" + str(lenOfCred+1)
            db.child("credentials").child(userId + k).push({"EmailId": username, "Password": password})
            global crendentials
            crendentials = firebase.get('/credentials', None)
            flash('Successfully Registered:) Go ahead and login')
            return render_template('register.html')
    return render_template('register.html')

@app.route('/application', methods=['POST', 'GET'])
def application():
    return render_template("application.html")
@app.route('/error')
def err():
    flash("Wrong password entered")
    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    global active
    active = None
    return home()

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
