from flask import jsonify
import json

class Database(object):
    def __init__(self, mysql):
        self.mysql = mysql

    """-----Update DATA---------"""

    def update(self, fname, lname):
        # Create cursor
        cur = self.mysql.connection.cursor()
        # Execute query
        cur.execute("UPDATE STUDENTS SET CH = 1 WHERE fname=%s and lname=%s", (fname, lname))

        # Commit to DB
        self.mysql.connection.commit()
        # Close connection
        cur.close()

    """-----Insert DATA---------"""
    def insert(self, fname, lname, ch):
        # Create cursor
        cur = self.mysql.connection.cursor()
        # Execute query
        cur.execute("INSERT INTO STUDENTS(fname, lname, CH) VALUES(%s, %s, %s)",
                    (fname, lname, ch))

        # Commit to DB
        self.mysql.connection.commit()
        # Close connection
        cur.close()

    """-----GET DATA---------"""
    def get(self):
        # Create cursor
        cur = self.mysql.connection.cursor()
        # Execute query
        cur.execute("SELECT * FROM STUDENTS")
        data = cur.fetchall()
        cur.close()
        return data
        #return jsonify({'STUDENTS':data})


    """-----DEL DATA---------"""

    def Del(self, fname, lname):
        # Create cursor
        cur = self.mysql.connection.cursor()
        # Execute query
        cur.execute("DELETE FROM STUDENTS WHERE fname = %s and lname = %s", (fname, lname))
        # Commit to DB
        self.mysql.connection.commit()
        cur.close()


    """-----ADD ADMIN---------"""

    def addAdmin(self, username, password):
        # Create cursor
        cur = self.mysql.connection.cursor()
        # Execute query
        cur.execute("INSERT INTO admins(username, password) VALUES(%s, %s)", (username, password))
        # Commit to DB
        self.mysql.connection.commit()
        # Close connection
        cur.close()

    """-----Admin Login---------"""
    def login(self, username):
        # Create cursor
        cur = self.mysql.connection.cursor()
        # Execute query
        result = cur.execute("SELECT * FROM admins WHERE username = %s " %username)
        data = cur.fetone()
        cur.close()
        return result, data




# {% for item in data.items()  %} {% endfor %}
