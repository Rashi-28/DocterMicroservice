from flask import Flask,render_template,request,redirect,session,url_for,jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import yaml
import re




app = Flask(__name__)

app.secret_key = "super secret key"

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'Poddar$123'
# app.config['MYSQL_DB'] = 'flask_project'
#  configure db
db= yaml.load(open('db.yaml'),Loader=yaml.Loader)
# db = pyyaml.load('db.yaml', Loader=pyyaml.Loader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
 
mysql = MySQL(app)

@app.route('/')
def hello():
    return 'Welcome to Doctor Service'

@app.route('/reg',methods=['POST','Get'])
def reg():
    if request.method=='POST':
        Name = request.form["Name"]
        Email = request.form["Email"]
        Password = request.form["Password"]
        Speciality = request.form["Speciality"]
        cur = mysql.connection.cursor()
        cur.execute("Select * from patient_details where Email = %s",(Email, ))
        account = cur.fetchone()
        if account:
           return jsonify("Account already exists!")
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',Email):
           return jsonify("Invalid email address! ")
        elif not Name or not Password or not Email:
           return jsonify("Please fill out the form!")
        cur.execute("INSERT INTO patient_details(Name,Email,Password,Speciality) VALUES(%s,%s,%s,%s)",(Name,Email,Password,Speciality))
        mysql.connection.commit()
        cur.close()
        return jsonify("Successfully Registered")
    return jsonify("Failed")

@app.route('/login', methods = ['POST','GET'])
def login():
    # msg=''
    if request.method == 'GET':
        name1 = request.form['Name']
        password1 = request.form['Password']
        cursor = mysql.connection.cursor()
        # cursor.execute("Select Name , Password from patient_details where Name = {un} and Password = {pw}".format(un=name1,pw=password1))
        cursor.execute("Select * from patient_details where Name = %s and Password=%s",(name1,password1))
        record = cursor.fetchone()
        if record:
            session['loggedin']= True
            session['Name']=record[1]
            return jsonify('Logged In Successfully !')
            # return render_template('home.html', msg=msg)
            
        else:
            return jsonify("Incorrect name/password.Try Again!")
    return jsonify("Back to Register Page")
    # return render_template('login.html', msg=msg)
    
# @app.route("/logout")
# def logout():
#     session.pop('loggedin',None)
#     session.pop('Name',None)
#     return redirect(url_for('login'))

@app.route("/users")
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("select * from patient_details")
    if resultValue>0:
        userDetails= cur.fetchall()
        return render_template('users.html',userDetails=userDetails)
    return jsonify("No Doctor is Registered")

@app.route('/delete/<int:id>', methods=['GET','POST'])
def delete(id):
     
    cursor = mysql.connection.cursor()
    response_object = {'status' : 'success'}
   
    # cursor.execute("Delete from patient_details where id ={}",[id])
    cursor.execute("Delete from patient_details where Id ={}" .format(id))
    mysql.connection.commit()
    cursor.close()
    response_object['message'] = 'Successfully Deleted'
    return jsonify(response_object)

if __name__ == '__main__':
    #  app.run(host='0.0.0.0', port=8000)
    app.run(debug=True) 