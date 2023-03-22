from flask import Flask, render_template, redirect, request, flash,url_for,session
from flask_mysqldb import MySQL,MySQLdb 
import MySQLdb.cursors
from werkzeug.utils import secure_filename
import os
#import magic
import urllib.request
from datetime import datetime
##############   ai code ######################
# import cv2
# import argparse
# from utils import *
# import mediapipe as mp
# from body_part_angle import BodyPartAngle
# from types_of_exercise import TypeOfExercise






 
app = Flask(__name__)
       
app.secret_key = "caircocoders-ednalan-2020"
       
app.config['MYSQL_HOST'] = 'p3nlmysql85plsk.secureserver.net'
app.config['MYSQL_USER'] = 'gymdbuid'
app.config['MYSQL_PASSWORD'] = '!Bsg15a8'
app.config['MYSQL_DB'] = 'gymdb'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
 
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
  
ALLOWED_EXTENSIONS = set(['WMV','AVI','3G2','mp4'])
  
def allowed_file(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@app.route('/')
def home():
	return render_template("index.html")



@app.route('/about')
def about():
	return render_template("about.html")
	
@app.route('/contact')
def contact():
	return render_template("contact.html")



##########  Admin Login ###################
	

@app.route('/login_admin',methods=['GET','POST'])
def adminlogin():
    msg = ''
    if request.method == 'POST': 
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (username, password, ))
        nonfaclog = cursor.fetchone()
        if nonfaclog:
            # session['loggedin'] = True
            # session['id'] = nonfaclog['id']
            # session['username'] = nonfaclog['username']
            msg = 'Logged in successfully !'
            return render_template('UI/admin/admin_index.html', msg = msg)
        else:
            msg = 'Wrong Credential !'
            return render_template('login_admin.html', msg = msg)
    else:
        return render_template("login_admin.html")



###########    Admin Dashboard  #######################

@app.route('/abc')
def admin():
    return render_template("UI/admin/admin_index.html")

##########   Coach Dashboard ###############


@app.route('/coachdashboard')
def coachdashboard():
    return render_template("UI/coach/coach_index.html")

 



############   Coach_ Entry #############

@app.route("/UI/admin/coach_entry",methods=['GET','POST'])
def coach_entry():
    if request.method=='POST':
        name=request.form['name']
        mobileno=request.form['mobileno']
        email=request.form['emailid']
        state=request.form['state']
        district=request.form['district']
        experience=request.form['experience']
        username=request.form['username']
        password=request.form['password']
        cursor=mysql.connection.cursor()
        
        cursor.execute("INSERT INTO coach_entry (name,mobileno,emailid,state,district,experience,username,password) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(name,mobileno,email,state,district,experience,username,password))
        mysql.connection.commit()
        msg="Data Inserted Successfully"
        
        return render_template("UI/admin/coach_Entry.html",msg=msg)
    else:
        cursor=mysql.connection.cursor()
        cursor.execute("SELECT * FROM coach_entry")
        coach_entry=cursor.fetchall()
        return render_template("UI/admin/coach_Entry.html",coach_entry=coach_entry)



            
    

###########   Coach Login ############



@app.route('/login_coach',methods=['GET','POST'])
def coachlogin():
    msg = ''
    if request.method == 'POST': 
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM coach_entry WHERE username = %s AND password = %s', (username, password, ))
        coach_login = cursor.fetchone()
        if coach_login:
            session['loggedin'] = True
            session['id'] = coach_login['id']
            session['username'] = coach_login['username']
            msg = 'Logged in successfully !'
            return render_template('UI/coach/coach_index.html', msg = msg)
        else:
            msg = 'Wrong Credential !'
            return render_template('login_coach.html', msg = msg)
    else:
        return render_template("login_coach.html")


###########   Student Registration Form ##############


@app.route('/UI/coach/student_registration',methods=['GET','POST'])
def student_registration():
    if request.method=='POST':
        first_name=request.form['first_name']
        last_name=request.form['last_name']
        gender=request.form['gender']
        age=request.form['age']
        height=request.form['height']
        weight=request.form['weight']
        bmi=request.form['bmi']
        #capture=request.form['capture']
        cursor=mysql.connection.cursor()
        cursor.execute("INSERT INTO student_registration (first_name,last_name,gender,age,height,weight,bmi) VALUES (%s,%s,%s,%s,%s,%s,%s)",(first_name,last_name,gender,age,height,weight,bmi))
        mysql.connection.commit()
        msg="Data Inserted Successfully"
        
        return render_template("UI/coach/student_Registration.html",msg=msg)
    else:
        cursor=mysql.connection.cursor()
        cursor.execute("SELECT * FROM student_registration")
        student_registration=cursor.fetchall()
        return render_template("UI/coach/student_Registration.html",student_registration=student_registration)


##########################     Exercise Add ##################


@app.route('/UI/admin/workout',methods=['GET','POST'])
def workout():
    if request.method=='POST':
        workout=request.form['workout']
        
        cursor=mysql.connection.cursor()
        cursor.execute("INSERT INTO exersize_name (workout) VALUES (%s)",[workout])
        cursor=mysql.connection.cursor()
        cursor.execute("SELECT * FROM exersize_name")
        exersize_name=cursor.fetchall()
        mysql.connection.commit()
        msg="Data Inserted Successfully"
        
        return render_template("UI/admin/add_workout.html",msg=msg,exersize_name=exersize_name)
    else:
        cursor=mysql.connection.cursor()
        cursor.execute("SELECT * FROM exersize_name")
        exersize_name=cursor.fetchall()
        return render_template("UI/admin/add_workout.html",exersize_name=exersize_name)
    


################### Capture Video #############################

@app.route('/UI/coach/capture_form',methods=['GET','POST'])
def capture():
   
        if 'loggedin' in session:
            if request.method=='GET':
                
                cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            
                cur.execute("SELECT id FROM coach_entry WHERE username=%s",(session['username'],))
                ghi=cur.fetchone()
                cur.execute("SELECT * FROM exersize_name")
                abc=cur.fetchall()
                cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("SELECT id FROM student_registration ")
                student_registration=cur.fetchone()
                # args = request.args
                # args.get('id',default="",type=str)

                return render_template("UI/coach/capture.html",exersize_name=abc,coach_entry=ghi,student_registration=student_registration)
            else:
                cur = mysql.connection.cursor()
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                now = datetime.now()
                if request.method == 'POST':
                    id=request.form['id']
                    coach_id=request.form['coach_id']
                    workout=request.form['workout']
                    files = request.files.getlist('files[]')
                    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            
                    cur.execute("SELECT id FROM coach_entry WHERE username=%s",(session['username'],))
                    ghi=cur.fetchone()
                    #print(files)
                    for file in files:
                        if file and allowed_file(file.filename):
                            filename = secure_filename(file.filename)
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                            cur.execute("INSERT INTO capture_form (student_id,coach_id,workout,file_name, uploaded_on) VALUES (%s, %s,%s,%s,%s)",[id,coach_id,workout,filename, now])
                            mysql.connection.commit()
                        print(file)
                    cur.close()   
                    flash('File(s) successfully uploaded')    
                return render_template("UI/coach/capture.html",coach_entry=ghi)





#################  coach profile  #############

@app.route('/UI/coach/coach_profile',methods=['GET','POST'])
def coach_profile():
    if 'loggedin' in session:
        if request.method=='GET':
            cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT name,mobileno,emailid,state,district,experience, username FROM coach_entry WHERE id = % s", (session['id'], ))
            coach_entry=cur.fetchone()
            return render_template("UI/coach/coach_profile.html",coach_entry=coach_entry)
        else:
            name=request.form['name']
            mobileno=request.form['mobileno']
            email=request.form['emailid']
            state=request.form['state']
            district=request.form['district']
            experience=request.form['experience']
            username=request.form['username']
            password=request.form['password']
            cursor=mysql.connection.cursor()
            
            cursor.execute("INSERT INTO coach_entry (name,mobileno,emailid,state,district,experience,username,password) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(name,mobileno,email,state,district,experience,username,password))
            mysql.connection.commit()
            msg="Data Inserted Successfully"
            
            return render_template("UI/admin/coach_Entry.html",msg=msg)
        
#################   Capture Report ################
@app.route("/UI/coach/analyse_form",methods=['GET','POST'])
def analyse_form():
     cur=mysql.connection.cursor()
     cur.execute("SELECT id,student_id,workout,file_name FROM capture_form")
     capture_form=cur.fetchall()
     return render_template("UI/coach/capture_report.html",capture_form=capture_form)

##############################   Analyse Form ##########################3       
@app.route("/UI/coach/analyse",methods=['GET','POST'])
def analyse():
    if 'loggedin' in session:
        
            cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute('SELECT file_name FROM capture_form WHERE id = %s',(session['id'],))
            capture_form=cur.fetchone()
            return render_template("UI/coach/analyse.html",capture_form=capture_form)

     


        





    








             

if __name__ == "__main__":
    app.run(debug=True)