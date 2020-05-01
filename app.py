import firebase as firebase
from firebase import firebase
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
active = None
#Firebase
from firebase import firebase
firebase = firebase.FirebaseApplication('https://cams-da440.firebaseio.com/', None)
credentials = firebase.get('/credentials', None)
cutoff = firebase.get('/Cutoff', None)
applications = firebase.get('/application', None)

@app.route('/', methods=['POST', 'GET'])
def home():
    global active
    return render_template('home.html', u= active, cf = cutoff)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        temp = -1
        username = request.form['uname']
        password = request.form['pass']
        for i in credentials:
            if username in credentials[i]['EmailId'] and password in credentials[i]['Password']:
                temp += 1
                print("Yes")
                session['logged_in'] = True
                global active
                active = username
                if active == 'admin@gmail.com':  ##admin
                    applications = firebase.get('/application', None)
                    return render_template('home_admin.html', u = active, cutoff = cutoff, form = applications)
                else:
                    print("logged")
                    return redirect("/")

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
            lenOfCred = len(credentials)
            userId = "CAMS"
            if lenOfCred <= 9:
                k = "000" +str(lenOfCred)
            elif lenOfCred >= 10 and lenOfCred <= 99:
                k = "00" +str(lenOfCred)
            elif lenOfCred >=100 and  lenOfCred <= 999:
                k = "0" + str(lenOfCred)
            db.child("credentials").child(userId + k).set({"EmailId": username, "Password": password})
            global crendentials
            crendentials = firebase.get('/credentials', None)
            flash('Successfully Registered:) Go ahead and login')
            return render_template('register.html')
    return render_template('register.html')

@app.route('/home_admin',methods=['POST','GET'])
def home_admin():
    global active

    if request.method == 'POST':
        choose = request.form['tab']
        if choose == 'Add College Details':
            print('works')
        if choose == 'View & Register Students':
            print('works')
        if choose == 'Create CutOff List':
            print('works')
        if choose == 'View Final Selected Students':
            print('works')
    return render_template('home_admin.html')

@app.route('/removeStud/<string:d_id>',methods=['POST','GET'])
def removeStud(d_id):
    #print(d_id)
    db.child("application").child(d_id).remove()
    applications = firebase.get('/application', None)
    return render_template('home_admin.html', u = active, cutoff = cutoff, form = applications)

@app.route('/application',methods=['POST', 'GET'])
def application():
    global active
    print(active)
    if active != None:
        for i in credentials:
            if active in credentials[i]['EmailId']:
                idno = i
                break
        applications = firebase.get('/application', None)
        for i in applications:
            if i == idno:
                return render_template('congrats.html')
        if request.method == 'POST':
            username = request.form['studname']
            perc12 = request.form['studPerc']
            branch = request.form.get("branch", None)
            db.child("application").child(idno).set({"EmailId":active , "Name":username, "12thPercentage": perc12, "BranchChosen": branch})
            return render_template('congrats.html')
        return render_template('application.html', emailId = active, stream = cutoff)
    return render_template('login.html')

@app.route('/dashboard',methods=['POST', 'GET'])
def dashboard():
    global active
    if active == 'admin@gmail.com':  ##admin
        return render_template('home_admin.html', u = active, cutoff = cutoff, form = applications)
    return render_template('student_dashboard.html', u= active)

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
