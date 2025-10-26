from flask import Flask, jsonify, redirect, render_template, request
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

new_users_data = [["125102009@nitkkr.ac.in",999999]]


def get_all_users():
    cursor.execute("select * from users")
    users = cursor.fetchall()
    return users

def create_user_table():
    try:   
        cursor.execute("""
                   create table users(
                       roll_no int primary key,
                       name varchar(80) not null,
                       email varchar(80) not null unique,
                       hostel_no int,
                       clubs varchar(200),
                       current_study_year int,
                       password varchar(100) not null
                   );
                   """)
        conn.commit()
    except Exception as e:
        print("User table already exists")

def create_blog_table():
    try:
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
    except Exception as e:
        print("Blog table already exists")

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


def add_student(roll_no,name,email, current_study_year, hostel_no, clubs, password):
    verify_student_details(email, current_study_year,hostel_no, password)
    cursor.execute(f"insert into users(roll_no,name,email,current_study_year,hostel_no, clubs, password) values({roll_no},'{name}','{email}',{current_study_year},'{hostel_no}','{clubs}','{password}')")
    conn.commit()

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

@app.route("/devesh")
def AboutUsPage():
    return redirect("/")

@app.route("/blog/<string:slug>")
def BlogPost(slug):
    blog = get_blog_by_slug(slug)
    if blog is None:
        return "Blog not found"
    print(blog)
    blog_data = {
        "title": blog[1],
        "creator_email": blog[2],
        "created_at": blog[3],
        "slug": blog[4],
        "content": blog[5]
    }
    return render_template("blog-post.html", blog=blog_data)


@app.route("/login",methods=["GET", "POST"])
def LoginPage():
    if request.method == "POST":
        data = request.get_json();
        email = data.get("email")
        password = data.get("password")
        print(f"Received issue from {email}: {password}")
        
        if verify_student_details(email,password):
            return jsonify({"status":200})
        else:
            return jsonify({"status":500})
        
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
            
        # otp = send_otp(email)
        otp = 999999
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
        hostel_no = data.get("hostel_no")
        clubs = data.get("clubs")
        password = data.get("password")

        print(email,otp,username,current_study_year,hostel_no,clubs,password)

        if verify_student_details(email=email,current_study_year=current_study_year, hostel_no=hostel_no, password=password):
            return "Message: Some informations are wrong."
        print(new_users_data)
        for user in new_users_data:
            print(user,email,type(otp))
            if user[0] == email and user[1] == int(otp) and not search_student(roll_no):
                add_student(roll_no,username,email,current_study_year,hostel_no, clubs, password)
                new_users_data.remove(user)
                print("new user added successfully")
                return jsonify({"status": 200})
        print("Something went wrong. Please try again.")
        return jsonify({"status":500})
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