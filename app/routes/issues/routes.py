from flask import render_template, request, redirect, jsonify, Blueprint

issues = Blueprint('issues', __name__)
@issues.route("/issues")
def IssuesPage():
    return render_template("issues.html")