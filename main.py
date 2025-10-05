from flask import Flask, render_template, request,g
from flaskext.mysql import MySQL


app = Flask(__name__,static_url_path="/static")
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'team'
app.config['MYSQL_DATABASE_PASSWORD'] = 'falcruds@#420'
app.config['MYSQL_DATABASE_DB'] = 'falcrum'

mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()


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
        current_study_year = request.form.get("current_study_year")
        password = request.form.get("password")
        print(f"Received issue from {email} ({current_study_year}): {password}")
        return render_template("create-account.html", message="Thank you for reaching out! We will get back to you soon.")
    else:
        return render_template("create-account.html")

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
    return render_template("blogs.html", blogs=blogs)

@app.route("/contact-us")
def ContactUsPage():
    return render_template("contact-us.html")

if __name__ == "__main__":
    app.run(port = 5500,debug=True)