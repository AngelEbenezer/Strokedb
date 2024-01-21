from flask import Flask, redirect, render_template, flash, url_for
from flask import request, session
from flask_session import Session
import mysql.connector as mysql

app = Flask(__name__)
app.secret_key = "super secret key"

@app.route('/')
def MyhomeRoot():
    return render_template('MyLogin.html')

@app.route("/My_Login_Process", methods=['POST'])
def My_Login_Process():
    uid = request.form["username"]
    pwd = request.form["password"]
    try:
        db_connect = mysql.connect(
            host="localhost", database="mydatabase", user="root", passwd="admin", use_pure=True)
        sql = "Select username, password From mypassword where username = " + "'" + uid + "'"
        mycursor = db_connect.cursor()
        mycursor.execute(sql)
        cno = mycursor.fetchall()
        res = [tuple(str(item) for item in t) for t in cno]
        #print(res)
    except Exception as err:
        print(err)
        return render_template('MyError.html')
    if len(res) == 0:
        status = 0
        return render_template('MyError.html')
    else:
        usrid  = res[0][0]
        passwd = res[0][1]
        if (usrid == uid and pwd == passwd):
            return render_template('MyHome1.html', usrid=usrid)
        else:
            """status = 0"""
            return render_template('MyError.html')

@app.route("/ViewPatient")
def ViewPatient():
    try:
        db_connect = mysql.connect(
            host="localhost", database="mydatabase", user="root", passwd="admin", use_pure=True)
        sql = "Select Name, Age, Gender, Diagnosis From patient"
        mycursor = db_connect.cursor()
        mycursor.execute(sql)
        cdata = mycursor.fetchall()
        return render_template("ViewPatient.html", cdata=cdata)
    except Exception as err:
        print(err)
        return render_template('MyError.html')

@app.route("/AddPatient", methods=['POST'])
def AddPatient():
    try:
        name   = request.form["name"]
        age  = request.form["age"]
        gender = request.form["gender"]
        db_connect = mysql.connect(
            host="localhost", database="mydatabase", user="root", passwd="admin", use_pure=True)
        sql = "INSERT INTO Patient(Name,Age,Gender) VALUES (" + "'" + name + "'" + "," + "'" + age +"'" + "," + "'"+gender+"'" + ")" 
        mycursor = db_connect.cursor()
        mycursor.execute(sql)
        db_connect.commit()
        return render_template("MyHome.html")
    except Exception as err:
        print(err)
        return render_template('MyError.html')


@app.route("/EnterSymptoms")
def EnterSymptoms():
    try:
        db_connect = mysql.connect(
            host="localhost", database="mydatabase", user="root", passwd="admin", use_pure=True)
        sql_std = "Select Name, Age, Gender, Diagnosis From patient"
        mycursor = db_connect.cursor()
        mycursor.execute(sql_std)
        cdata = mycursor.fetchall()
        return render_template("EnterSymptoms.html", cdata=cdata)
    except Exception as err:
        print(err)
        return render_template('Error.html')

@app.route("/MyHome")
def MyHome():
    return render_template("MyHome.html")

@app.route("/MyError")
def MyError():
    return render_template("MyError.html")

@app.route("/AddPatient")
def InsertStudent():
    return render_template("AddPatient.html")

if __name__ == '__main__':
    app.run()
