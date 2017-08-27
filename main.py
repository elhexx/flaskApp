from flask import Flask, render_template, flash, request, url_for, redirect, session, jsonify
from wtforms import Form, BooleanField, TextField, PasswordField, validators, StringField
from passlib.hash import sha256_crypt
import gc

from flask_mysqldb import  MySQL
from MySQLdb import escape_string as thwart
from database import Database
from functools import wraps
app = Flask(__name__)

"""-----Config MySQL---------"""
app.config["MYSQL_HOST"] = 'localhost'
app.config["MYSQL_USER"] = 'root'
app.config["MYSQL_PASSWORD"] = 'toor'
app.config["MYSQL_DB"] = 'test'
app.config["MYSQL_CURSORCLASS"] = 'DictCursor'
app.secret_key = "hello"

"""-----Init MySQL---------"""
mysql = MySQL(app)
database = Database(mysql)


languages = [{'name':'java'},{'name':'Python'},{'name':'flask'}, {'name':'XD'},{'name':'XD'}]

"""--------Security-----------"""
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/json")
def json():
    return jsonify({'languages':languages})


"""-----ADDING DATA---------"""


@app.route("/add", methods=['GET', 'POST'])
@is_logged_in
def add():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        ch = 0
        msg = "User added successfully"
        try:
            database.insert(fname, lname, ch)
            jsonObject = database.get()
            return render_template('add.html', msg=msg, data = jsonObject)
        except Exception as e:
            return e.message
    if request.method == 'GET':
        jsonObject = database.get()
        return render_template('add.html', data = jsonObject)

"""-----UPDATING DATA---------"""


@app.route("/upd", methods=['GET','POST'])
def upd():
    fname = request.form['fname']
    lname = request.form['lname']
    try:
        database.update(fname, lname)
        return "Done"
    except Exception as e:
        return e.message


"""-----GET DATA---------"""

@app.route("/dashboard")
@is_logged_in
def get():
    jsonObject = database.get()

    #return jsonObject
    return render_template('dashboard.html', data=jsonObject)

    #return render_template('test.html', data=jsonObject)

#"""----- DELETE DATA---------"""
@app.route("/del", methods=['GET','POST'])
@is_logged_in
def Del():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        try:
            database.Del(fname, lname)
            jsonObject = database.get()
            return render_template('del.html', data=jsonObject)
        except Exception as e:
            return e.message
    if request.method == 'GET':
        jsonObject = database.get()
        return render_template('del.html', data=jsonObject)


#-------------Login Route-----------

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM admins WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('get'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')




#-------------Logout Route-----------
@app.route('/logout')
def logout():
    session.clear()
    flash('you are logged out', 'success')
    return redirect(url_for('login'))

#-------------Register Route-----------

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=20)])
    password = PasswordField('New Password', [
        validators.data_required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'GET':
        return render_template('register.html', form=form)

    if request.method == 'POST':
        try:
            username = form.username.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            database.addAdmin(thwart(username), thwart(password))
            gc.collect()
            session['logged_in'] = True
            session['username'] = username

            return render_template('index.html')
        except Exception as e:
            return (str(e))






if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
