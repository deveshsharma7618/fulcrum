from flask import Flask, jsonify, redirect, render_template, request
from flaskext.mysql import MySQL
from app.utils.user.verify_user import check_email, send_otp, verify_student_details
from dotenv import load_dotenv
from os import environ as env
from flask_bcrypt import Bcrypt


mysql = MySQL()
load_dotenv()

app = Flask(__name__,static_url_path="/static")
bcrypt = Bcrypt(app)
app.config['MYSQL_DATABASE_HOST'] = env.get('MYSQL_DATABASE_HOST')
app.config['MYSQL_DATABASE_USER'] = env.get('MYSQL_DATABASE_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = env.get('MYSQL_DATABASE_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = env.get('MYSQL_DATABASE_DB')
app.config['SECRET_KEY'] = env.get('SECRET_KEY')
app.config['MYSQL_DATABASE_PORT'] = int(env.get('MYSQL_DATABASE_PORT') or 3306)

from app.routes.blogs import blog
from app.routes.user import user
from app.routes.issues import issues

app.register_blueprint(blog)
app.register_blueprint(user)
app.register_blueprint(issues)

mysql.init_app(app) # Initialize Flask-MySQL with your app
conn = mysql.connect()
cursor = conn.cursor()


@app.route("/")
def HomePage():
    return render_template("index.html")

@app.route("/devesh")
def AboutUsPage():
    return redirect("/")

@app.route("/contact-us")
def ContactUsPage():
    return render_template("contact-us.html")
