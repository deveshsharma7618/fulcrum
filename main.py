from flask import Flask, redirect, render_template, request, make_response
from flask_sqlalchemy import SQLAlchemy
from verify import check_email, send_otp



app = Flask(__name__,static_url_path="/static")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db = SQLAlchemy(app)

class User(db.Model):
    email = db.Column(db.String(120), unique=True, nullable=False, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    current_study_year = db.Column(db.Integer, unique=False, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    
    def __init__(self, username, email, current_study_year, password):
        super().__init__()
        self.username = username
        self.email = email
        self.current_study_year = current_study_year
        self.password = password



# user = User(username="admin", email="devesh1", current_study_year="4th Year", password="admin123")
# db.session.add(user)
# db.session.commit()

new_users_data = []


@app.route("/")
def HomePage():
    return render_template("index.html")


@app.route("/login",methods=["GET", "POST"])
def LoginPage():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        print(f"Received issue from {email}: {password}")
        
        return render_template("login.html", message="Thank you for reaching out! We will get back to you soon.")
    else:
        return render_template("login.html")


@app.route("/create-account", methods=["GET", "POST"])
def CreateAccount():
    if request.method == "POST":
        email = request.form.get("email")
        print(email)
        if check_email(email) == False:
            return "Invalid Email ID"
        
        for user in new_users_data:
            if user[0] == email:
                return render_template("verify-otp.html", message="OTP already sent to this email", otp_sent_to=email, otp = user[1])
            
        otp = send_otp(email)
        new_users_data.append([email,otp])
        print(f"Received issue from {email} : ({otp}")
        resp = make_response()
        resp.set_cookie("email", email,max_age=5*60)
        
        
        print(new_users_data)
        return render_template("verify-otp.html", otp_sent_to=email, otp = otp)
    else:
        return render_template("create-account.html")

@app.route("/verify-otp", methods=["GET", "POST"])
def VerifyOTP():
    if request.method == "POST":
        email = request.form.get("email")
        
        otp = request.form.get("otp")
        username = request.form.get("username")
        current_study_year = request.form.get("current_study_year")
        password = request.form.get("password")
        
        print(email,otp,username,current_study_year,password)
        for user in new_users_data:
            if user[0] == email and str(user[1]) == otp:
                new_user = User( username=username, email=email, current_study_year=current_study_year, password=password)
                db.session.add(new_user)
                db.session.commit()
                new_users_data.remove(user)
                return redirect("/",user_data = {
                    "username": username,
                    "email": email,
                    "current_study_year": current_study_year,
                    "password": password
                })
        return render_template("verify-otp.html", message="Incorrect OTP")
    else:
        return render_template("verify-otp.html")

@app.route("/blogs")
def BlogsPage():
    blogs = [
        {
            "title": "The Impact of Social Media on Mental Health",
            "description": "Exploring the correlation between social media usage and mental health issues among teenagers."
        },
        {
            "title": "The Impact of Social Media on Mental Health",
            "description": "Exploring the correlation between social media usage and mental health issues among teenagers."
        },
        {
            "title": "The Impact of Social Media on Mental Health",
            "description": "Exploring the correlation between social media usage and mental health issues among teenagers."
        },
        {
            "title": "The Impact of Social Media on Mental Health",
            "description": "Exploring the correlation between social media usage and mental health issues among teenagers."
        }
    ]
    blogs_from_db = Blog.query.all()
    for blog in blogs_from_db:
        blogs.append({
            "title": blog.title,
            "description": blog.content
        })
    
    return render_template("blogs.html", blogs=blogs)

@app.route("/contact-us")
def ContactUsPage():
    return render_template("contact-us.html")

if __name__ == "__main__":
    app.run(port = 5500,debug=True)