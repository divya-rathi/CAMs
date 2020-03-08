from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_admin_login():
    '''
    global active
    global email
    if request.form['choice'] == 'user':
        if request.form['username'] in user and user[request.form['username']] == request.form['password']:
            active = request.form['username']
            session['logged_in'] = True
        else:
            return redirect('/error')
        return render_template('home.html',email=active)

    elif request.form['choice'] == 'admin':
        if request.form['username'] in admin and admin[request.form['username']] == request.form['password']:
            active = request.form['username']
            session['logged_in'] = True
        else:
            return redirect('/error')
        return render_template('home.html',email=active)
'''
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