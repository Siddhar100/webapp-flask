from flask_sqlalchemy import SQLAlchemy
from flask import Flask,render_template,request,session,Response
from flask_session import Session
from markupsafe import escape
import json
import pymysql
pymysql.install_as_MySQLdb()


app = Flask(__name__,template_folder='templetes')


with open('config.json', 'r') as c:
    params = json.load(c)["Param"]

app.config['SQLALCHEMY_DATABASE_URI'] = params['server']

db = SQLAlchemy(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

class posts(db.Model):
    si_no = db.Column(db.Integer,primary_key=True)
    image_url = db.Column(db.String(80),nullable=False)
    content = db.Column(db.String(80),nullable=False)
    post_time = db.Column(db.String(80),nullable=False)

     
class user(db.Model):
    si_no = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(80),nullable=False)
    last_name = db.Column(db.String(80),nullable=False)
    email_id = db.Column(db.String(80),nullable=False)
    country = db.Column(db.String(80),nullable=False)
    state = db.Column(db.String(80),nullable=False)
    zip_code = db.Column(db.String(80),nullable=False)
    user_name = db.Column(db.String(80),nullable=False)
    password = db.Column(db.String(80),nullable=False)


@app.route('/')
def index():
    if  session.get("name") is not None:
        # if not there in the session then redirect to the login page
        return redirect("/dashboard")
    else:
        post = posts.query.filter_by().all()
        return render_template('index.html',post=post,params=params)

@app.route('/twitter')
def twitter():
    return render_template('index.html',params=params)

@app.route('/signup')
def signup():
    return render_template('signUp.html',params=params)

@app.route('/formSubmit',methods=['GET','POST'])
def formSubmit():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email_id = request.form.get('email_id')
        country = request.form.get('country')
        state = request.form.get('state')
        zip_code = request.form.get('zip_code')
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        entry = user(first_name=first_name, last_name=last_name , email_id=email_id,country=country , state=state,zip_code=zip_code,user_name=user_name,password=password)
        db.session.add(entry)
        db.session.commit()
    post = posts.query.filter_by().all()
    return render_template('index.html',params=params,post=post)

@app.route('/login')
def login():
    return render_template('login.html',params=params)

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():

    if request.method == 'POST':
        email = request.form.get('email_id')
        password = request.form.get('password')
        user_password =  user.query.filter_by(email_id=email).first()
        print(user_password)
        if password == user_password.password:
            session["username"] = email
            post = posts.query.filter_by().all()
            return render_template('dashboard.html',post=post,params=params,user_password=user_password)
        else:
            post = posts.query.filter_by().all()
            return render_template('loginerror.html',post=post,params=params)
    else:
        return "!sorry"

@app.route('/logout',methods = ['POST','GET'])
def logout():
    if request.method == 'GET':
       session["name"] = None
       post = posts.query.filter_by().all()
       """response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"""
       return render_template('index.html',post=post,params=params)
    

@app.route('/new_courses')
def new_courses():
    post = posts.query.filter_by().all()
    return render_template('courses.html',post=post)

if __name__ == "__main__":
    app.run(debug=True)