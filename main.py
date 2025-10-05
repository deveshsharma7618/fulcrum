from flask import Flask, render_template

app = Flask(__name__,static_url_path="/static")


@app.route("/")
def HomePage():
    return render_template("index.html")

@app.route("/login")
def LoginPage():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(port = 5000)