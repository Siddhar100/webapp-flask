from flask_sqlalchemy import SQLAlchemy
from flask import Flask,render_template,request,session,Response,redirect
from flask_session import Session
from markupsafe import escape
import json
import stripe
import pymysql
pymysql.install_as_MySQLdb()


app = Flask(__name__,template_folder='templetes')
stripe.api_key =  "sk_test_51OgOmZSIkioDkBuALAyB5xM4dwoE9G51Z2Wj8z1yzLR4Vyjyv5GXLwQRKxDVDm13KrxvAOf7UJOa8oVddHia318l00RtLWqVZJ"

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

class course(db.Model):
    si_no = db.Column(db.Integer,primary_key=True)
    email_id = db.Column(db.String(80),nullable=False)
    course_name = db.Column(db.String(80),nullable=False)
    course_time = db.Column(db.String(80),nullable=False)
    course_id = db.Column(db.Integer,primary_key=False)


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
    #we can directly redirect to the particular url
    return render_template('index.html',params=params)

@app.route('/signup')
def signup():
    return render_template('signUp.html',params=params)

@app.route('/formSubmit',methods=['GET','POST'])
def formSubmit():
    #user sign up function.
    #all the data is stored in mysql database.
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email_id = request.form.get('email_id')
        country = request.form.get('country')
        state = request.form.get('state')
        zip_code = request.form.get('zip_code')
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        errors = []
        if not first_name:
            errors.append("Enter First Name!")
        if not last_name:
            errors.append("Enter Last Name!")
        if not email_id:
            errors.append("Enter Email!")
        if not country:
            errors.append("Enter Country!")
        if not state:
            errors.append("Enter State!")
        if not zip_code:
            errors.append("Enter Zip Code!")
        if not user_name:
            errors.append("Enter User Name!")
        if not password:
            errors.append("Enter password!")
        if len(password) < 8:
            errors.append("Password should be minimum 8 charecter!")
        if user.query.filter_by(email_id=email_id).count()!= 0:
            errors.append("Email Id is already registered with another user!")
        if errors:
            return render_template('signUp.html',errors=errors,params=params)
        else:
            entry = user(first_name=first_name, last_name=last_name , email_id=email_id,country=country , state=state,zip_code=zip_code,user_name=user_name,password=password)
            db.session.add(entry)
            db.session.commit()
            post = posts.query.filter_by().all()
            return render_template('index.html',params=params,post=post)

@app.route('/login')
def login():
    #user login page
    return render_template('login.html',params=params)

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():

    if request.method == 'POST':
        #data submission in login page will always use post method for security
        email = request.form.get('email_id')
        password = request.form.get('password')
        errors = []
        if not email:
            errors.append("Enter Email Id!")
        if not password:
            errors.append("Enter password!")
        if user.query.filter_by(email_id=email).count() == 0:
            errors.append("Invalid User Name and Password!")
        if errors:
            return render_template('login.html',errors=errors,params=params)
        else:
            user_password =  user.query.filter_by(email_id=email).first()
            #print(user_password)
            if password == user_password.password:
                session["username"] = email
                session["user_name"] = user_password.user_name
                session["first_name"]= user_password.first_name
                session["last_name"] = user_password.last_name
                session["email"] = user_password.email_id
                session["country"] = user_password.country
                courses = course.query.filter_by(email_id=email).all()
                not_included = []
                for items in courses:
                    not_included.append(items.course_id)
                post = posts.query.filter(~(posts.si_no.in_(not_included)))
                return render_template('dashboard.html',post=post,params=params,user_password=user_password,errors=errors)
            else:
                errors.append("Password mismatch!")
                return render_template('login.html',errors=errors,params=params)
            
    else:
        #Get method will be used to redirect from bucket to dashboard
        email = session.get('email')
        user_password =  user.query.filter_by(email_id=email).first()
        courses = course.query.filter_by(email_id=email).all()
        not_included = []
        for items in courses:
            not_included.append(items.course_id)
        post = posts.query.filter(~(posts.si_no.in_(not_included)))
        return render_template('dashboard.html',user_password=user_password,post=post,params=params)
        
        

@app.route('/logout',methods = ['POST','GET'])
def logout():
    #In logout method session will be invalidate
    if request.method == 'GET':
       session["name"] = None
       post = posts.query.filter_by().all()
       """response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"""
       return render_template('index.html',post=post,params=params)
    

@app.route('/new_courses')
def new_courses():
    post = posts.query.filter_by().all()
    return render_template('courses.html',post=post)

@app.route('/bucket')
def bucket():
    user_name = session.get("username")
    courses = course.query.filter_by(email_id=user_name).all()
    course_ids = []
    for ids in courses:
        course_ids.append(ids.course_id)
    post = posts.query.filter(posts.si_no.in_(course_ids))
    return render_template('bucket.html',params=params,post=post)

@app.route('/sucess_1')
def sucess_1():
    user_email = session.get('username')
    course_name = "C"
    course_time = "2 hrs"
    course_id = 1
    entry = course(email_id=user_email,course_name=course_name,course_time=course_time,course_id=course_id)
    db.session.add(entry)
    db.session.commit()
    email = session.get('email')
    user_password =  user.query.filter_by(email_id=email).first()
    courses = course.query.filter_by(email_id=email).all()
    not_included = []
    for items in courses:
        not_included.append(items.course_id)
    post = posts.query.filter(~(posts.si_no.in_(not_included)))
    return render_template('dashboard.html',user_password=user_password,post=post,params=params)

@app.route('/sucess_2')
def sucess_2():
    user_email = session.get('username')
    course_name = "Java"
    course_time = "3 hrs"
    course_id = 2
    entry = course(email_id=user_email,course_name=course_name,course_time=course_time,course_id=course_id)
    db.session.add(entry)
    db.session.commit()
    email = session.get('email')
    user_password =  user.query.filter_by(email_id=email).first()
    courses = course.query.filter_by(email_id=email).all()
    not_included = []
    for items in courses:
        not_included.append(items.course_id)
    post = posts.query.filter(~(posts.si_no.in_(not_included)))
    return render_template('dashboard.html',user_password=user_password,post=post,params=params)


@app.route('/sucess_3')
def sucess_3():
    user_email = session.get('username')
    course_name = "Python"
    course_time = "3 hrs"
    course_id = 3
    entry = course(email_id=user_email,course_name=course_name,course_time=course_time,course_id=course_id)
    db.session.add(entry)
    db.session.commit()
    email = session.get('email')
    user_password =  user.query.filter_by(email_id=email).first()
    courses = course.query.filter_by(email_id=email).all()
    not_included = []
    for items in courses:
        not_included.append(items.course_id)
    post = posts.query.filter(~(posts.si_no.in_(not_included)))
    return render_template('dashboard.html',user_password=user_password,post=post,params=params)


@app.route('/cancel')
def cancel():
    email = session.get('email')
    user_password =  user.query.filter_by(email_id=email).first()
    courses = course.query.filter_by(email_id=email).all()
    not_included = []
    for items in courses:
        not_included.append(items.course_id)
    post = posts.query.filter(~(posts.si_no.in_(not_included)))
    return render_template('dashboard.html',user_password=user_password,post=post,params=params)

@app.route('/1')
def add_course_1():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items = [
                {
                    'price':'price_1OgTw2SIkioDkBuA4JCmpoI1',
                    'quantity':1

                }
            ],
            mode="subscription",
            success_url = "http://127.0.0.1:5000/sucess_1",
            cancel_url = "http://127.0.0.1:5000/cancel"

        )
    except Exception as e:
        return str(e)
    return redirect(checkout_session.url)  
    

@app.route('/2')
def add_course_2():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items = [
                {
                    'price':'price_1OgVbcSIkioDkBuARv71Co95',
                    'quantity':1

                }
            ],
            mode="subscription",
            success_url = "http://127.0.0.1:5000/sucess_2",
            cancel_url = "http://127.0.0.1:5000/cancel"

        )
    except Exception as e:
        return str(e)
    return redirect(checkout_session.url)  

@app.route('/3')
def add_course_3():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items = [
                {
                    'price':'price_1OgVd0SIkioDkBuAKfURdk0O',
                    'quantity':1

                }
            ],
            mode="subscription",
            success_url = "http://127.0.0.1:5000/sucess_3",
            cancel_url = "http://127.0.0.1:5000/cancel"

        )
    except Exception as e:
        return str(e)
    return redirect(checkout_session.url)  

@app.route('/course_no_1')
def course_no_1():
    return redirect("https://www.cs.fsu.edu/~cop3014p/lectures/")

@app.route('/course_no_2')
def course_no_2():
    return redirect("https://ww2.cs.fsu.edu/~thrasher/cop3252/")

@app.route('/course_no_3')
def course_no_3():
    return redirect("https://www.tutorialspoint.com/python/index.htm")

if __name__ == "__main__":
    app.run(debug=True)