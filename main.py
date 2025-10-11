from flask import Flask, redirect, render_template, request
from flaskext.mysql import MySQL
from verify import check_email, send_otp, verify_student_details


mysql = MySQL()

app = Flask(__name__,static_url_path="/static")
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'devesHSharma7618'
app.config['MYSQL_DATABASE_DB'] = 'fulcrum'
app.config['MYSQL_DATABASE_PORT'] = 3306 # Default MySQL port

mysql.init_app(app) # Initialize Flask-MySQL with your app
conn = mysql.connect()
cursor = conn.cursor()

new_users_data = []

def get_all_users():
    cursor.execute("select * from users")
    users = cursor.fetchall()
    return users

def create_user_table():
    cursor.execute("""
                   create table users(
                       roll_no int primary key,
                       name varchar(80) not null,
                       email varchar(80) not null unique,
                       password varchar(100) not null,
                       current_study_year int
                   );
                   """)
    conn.commit()

def create_blog_table():
    cursor.execute("""
                   create table blogs(
                       id int primary key auto_increment,
                       title varchar(200) not null,
                       creator_email varchar(100) not null,
                       created_at timestamp default current_timestamp,
                       slug varchar(200) not null unique,
                       content text not null
                   );
                   """)
    conn.commit()

def add_blog(title, creator_email, slug, content):
    cursor.execute(f"insert into blogs(title,creator_email,slug,content) values('{title}','{creator_email}','{slug}','{content}')")
    conn.commit()


def get_n_blogs(n):
    cursor.execute("select * from blogs")
    blogs = cursor.fetchall()[:n]
    return blogs

def get_all_blogs():
    cursor.execute("select * from blogs")
    blogs = cursor.fetchall()
    return blogs

def get_blog_by_slug(slug):
    cursor.execute(f"select * from blogs where slug='{slug}'")
    blog = cursor.fetchone()
    return blog


def add_student(roll_no,name,email, current_study_year, password):
    verify_student_details(roll_no,name,email, current_study_year, password)
    cursor.execute(f"insert into users(roll_no,name,email,current_study_year,password) values({roll_no},'{name}','{email}',{current_study_year},'{password}')")
    cursor.commit()

def search_student(roll_no):
    cursor.execute(f"select * from users where roll_no={roll_no}")
    user = cursor.fetchone()
    print(user)
    if user is None:
        return False
    else:
        return True


@app.route("/")
def HomePage():
    return render_template("index.html")


@app.route("/login",methods=["GET", "POST"])
def LoginPage():
    if request.method == "POST":
        data = request.get_json();
        email = data.get("email")
        password = data.get("password")
        print(f"Received issue from {email}: {password}")
        
        if verify_student_details(email,password):
            return redirect("/",user_data = {
                "email": email,
                "password": password
            })
        else:
            return "Message: Invalid Credentials. Please try again."
        
    else:
        return render_template("login.html")


@app.route("/create-account", methods=["GET", "POST"])
def CreateAccount():
    if request.method == "POST":
        email = request.get_json().get("email")
        print(email)
        if check_email(email) == False:
            return "Invalid Email ID"
        
        for user in new_users_data:
            if user[0] == email:
                return render_template("verify-otp.html", message="OTP already sent to this email", otp_sent_to=email, otp = user[1])
            
        otp = send_otp(email)
        new_users_data.append([email,otp])
        print(f"Received issue from {email} : ({otp}")
        
        
        print(new_users_data)
        return render_template("verify-otp.html", otp_sent_to=email, otp = otp)
    else:
        return render_template("create-account.html")

@app.route("/verify-otp", methods=["GET", "POST"])
def VerifyOTP():
    if request.method == "POST":
        data = request.get_json()
        email = data.get("email")
        roll_no = email.split('@')[0]
        otp = data.get("otp")
        username = data.get("username")
        current_study_year = data.get("current_study_year")
        password = data.get("password")
              
        print(email,otp,username,current_study_year,password)
        for user in new_users_data:
            if user[0] == email and str(user[1]) == otp and not search_student(roll_no):
                new_users_data.remove(user)
                return redirect("/",user_data = {
                    "username": username,
                    "email": email,
                    "current_study_year": current_study_year,
                    "password": password
                })
        return "Message: Something went wrong. Please try again."
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
    blogs_from_db = get_all_blogs()
    print(blogs_from_db)
    for blog in blogs_from_db:
        blogs.append({
            "title": blog[1],
            "description": blog[5]
        })
    
    return render_template("blogs.html", blogs=blogs)

@app.route("/contact-us")
def ContactUsPage():
    return render_template("contact-us.html")


if __name__ == "__main__":
    app.run(port = 5500,debug=True)