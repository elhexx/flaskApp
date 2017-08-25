from flask import Flask, render_template, jsonify, request, make_response
from flask_mysqldb import  MySQL
from database import Database

app = Flask(__name__)

"""-----Config MySQL---------"""
app.config["MYSQL_HOST"] = 'localhost'
app.config["MYSQL_USER"] = 'root'
app.config["MYSQL_PASSWORD"] = 'toor'
app.config["MYSQL_DB"] = 'test'
app.config["MYSQL_CURSORCLASS"] = 'DictCursor'

"""-----Init MySQL---------"""
mysql = MySQL(app)
database = Database(mysql)


languages = [{'name':'java'},{'name':'Python'},{'name':'flask'}, {'name':'XD'},{'name':'XD'}]

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/json")
def json():
    return jsonify({'languages':languages})


"""-----ADDING DATA---------"""


@app.route("/add", methods=['GET', 'POST'])
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
def get():
    jsonObject = database.get()

    #return jsonObject
    return render_template('dashboard.html', data=jsonObject)

    #return render_template('test.html', data=jsonObject)

@app.route("/del", methods=['GET','POST'])
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



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
