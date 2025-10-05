from flask import Flask, render_template

app = Flask(__name__,static_url_path="/static")


@app.route("/")
def HomePage():
    return render_template("index.html")

@app.route("/login")
def LoginPage():
    return render_template("login.html")

@app.route("/create-account")
def CreateAccount():
    return render_template("create-account.html")

@app.route("/blogs")
def BlogsPage():
    return render_template("blogs.html")

@app.route("/contact-us")
def ContactUsPage():    
    return render_template("contact-us.html")

if __name__ == "__main__":
    app.run(port = 5500)