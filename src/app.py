from flask import Flask,render_template,request,redirect,session,url_for
from flask_mysqldb import MySQL
import yaml
import re




app = Flask(__name__)

app.secret_key = "super secret key"

#  configure db
db= yaml.load(open('db.yaml'),Loader=yaml.Loader)
# db = pyyaml.load('db.yaml', Loader=pyyaml.Loader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
 
mysql = MySQL(app)

# @app.route('/')
# def index():
#     return render_template("login.html")

# @app.route("/home")
# def home():
#      return render_template("home.html",username=session['Name'])
#     return render_template('home.html')
     
@app.route('/')
@app.route('/login', methods = ['POST','GET'])
def login():
    msg=''
    if request.method == 'POST' and 'Name' in request.form and 'Password' in request.form:
        name1 = request.form['Name']
        password1 = request.form['Password']
        cursor = mysql.connection.cursor()
        # cursor.execute("Select Name , Password from patient_details where Name = {un} and Password = {pw}".format(un=name1,pw=password1))
        cursor.execute("Select * from patient_details where Name = %s and Password=%s",(name1,password1))
        record = cursor.fetchone()
        if record:
            session['loggedin']= True
            session['Name']=record[1]
            msg = 'Logged In Successfully !'
            return render_template('home.html', msg=msg)
            
        else:
            msg= "Incorrect name/password.Try Again!"
    return render_template('login.html', msg=msg)
    
@app.route("/logout")
def logout():
    session.pop('loggedin',None)
    session.pop('Name',None)
    return redirect(url_for('login'))
    # return render_template("login.html")


@app.route('/register',methods = ['POST', 'GET'])
def register():
    msg =''
    
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form:

        
        Name = request.form['name']
        Email = request.form['email']
        Password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute("Select * from patient_details where Email = %s",(Email, ))
        account = cursor.fetchone()
        if account:
            msg = "Account already exists!"
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',Email):
            msg = "Invalid email address! "
        elif not Name or not Password or not Email:
            msg = "Please fill out the form!"
        else:
           cursor.execute("INSERT INTO patient_details(Name,Email,Password) VALUES(%s,%s,%s)",(Name,Email,Password)) 
           mysql.connection.commit()
           msg = "You Successfully Registered!"
           return render_template('login.html', msg=msg)
    elif request.method == 'POST':
        msg= "Please fill out the form"    
    return render_template('signup.html',msg=msg)  


        
    
    


# @app.route("/",methods = ['POST','GET'])
# def login():
    
#     name1 = request.form.get('Name')
#     password1 = request.form.get('Password')
#     sqlConnection = sqlite3.Connection(currentlocation + "\flask_project.db")
#     cursor = sqlconnection.cursor()
#     query1 = "Select Name , Password from patient_details where Name = {un} and Password = {pw}".format(un=name1,pw=password1)
#     rows = cursor.execute(query1)
#     rows = rows.fetchall()
#     if len(rows)==1:
#         return render_template("login.html")
#     else:
#         return redirect("/register")


    

# @app.route("/register",methods = ['POST', 'GET'])
# def sign_up():
    
#     if request.method == 'POST':
#         userDetails = request.form
#         Name = userDetails['name']
#         Email = userDetails['email']
#         Password = userDetails['password']
        

#         cur = mysql.connection.cursor()
#         cur.execute("INSERT INTO patient_details(Name,Email,Password) VALUES(%s,%s,%s)",(Name,Email,Password))
#         mysql.connection.commit()
#         cur.close()
#         # return redirect('/users')
#         return redirect(url_for('login'))
        
#     return render_template('signup.html')


    

@app.route("/users")
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("select * from patient_details")
    if resultValue>0:
        userDetails= cur.fetchall()
        return render_template('users.html',userDetails=userDetails)


if __name__ == '__main__':
    #   app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)

@app.route('/delete/<int:id>', methods=['GET','POST'])
def delete(id):
     
    cursor = mysql.connection.cursor()
    response_object = {'status' : 'success'}
   
    # cursor.execute("Delete from patient_details where id ={}",[id])
    cursor.execute("Delete from patient_details where id ={}" .format(id))
    mysql.connection.commit()
    cursor.close()
    response_object['message'] = 'Successfully Deleted'
    return jsonify(response_object)