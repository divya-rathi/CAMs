from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os

app = Flask(__name__)

#Firebase
from firebase import firebase
firebase = firebase.FirebaseApplication('https://cams-da440.firebaseio.com/', None)
crendentials = firebase.get('/credentials', None)


@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_admin_login():
    temp = -1
    username = request.form['uname']
    password = request.form['pass']
    for i in crendentials:
        if username in crendentials[i]['username'] and password in crendentials[i]['password']:
            temp += 1
            session['logged in'] = True
            return "Logged In"
    if temp == -1:
        return "Invalid"

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