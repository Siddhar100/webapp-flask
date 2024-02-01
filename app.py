from flask_sqlalchemy import SQLAlchemy
from flask import Flask,render_template,request
from markupsafe import escape
import json
import pymysql
pymysql.install_as_MySQLdb()


app = Flask(__name__,template_folder='templetes')


with open('config.json', 'r') as c:
    params = json.load(c)["Param"]

app.config['SQLALCHEMY_DATABASE_URI'] = params['server']

db = SQLAlchemy(app)


class posts(db.Model):
    si_no = db.Column(db.Integer,primary_key=True)
    image_url = db.Column(db.String(80),nullable=False)
    content = db.Column(db.String(80),nullable=False)
    post_time = db.Column(db.String(80),nullable=False)

     

@app.route('/')
def index():
    post = posts.query.filter_by().all()
    return render_template('index.html',post=post,params=params)

@app.route('/twitter')
def twitter():
    return render_template('index.html',params=params)



if __name__ == "__main__":
    app.run(debug=True)