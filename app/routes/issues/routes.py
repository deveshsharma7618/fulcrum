from flask import render_template, request, redirect, jsonify, Blueprint

issues = Blueprint('issues', __name__)
@issues.route("/contact-us", methods=["GET", "POST"])
def IssuesPage():
    if request.method == "POST":
        data = request.get_json()
        message = data.get("message")
        if len(message) > 1000:
            return jsonify({"status": 400, "message": "Message is too long. Please limit it to 1000 characters.", "code": 400})
        
        if len(message) < 10:
            return jsonify({"status": 400, "message": "Message is too short. Please provide more details.", "code": 400})
        email = data.get("email")
        access_token = data.get("access_token")
        
        from app import cursor
        cursor.execute("SELECT * FROM users WHERE password = %s AND email = %s", (access_token, email))
        user = cursor.fetchone()
        if not user:
            return jsonify({"status": 401, "message": "Invalid access token or email.", "code": 401})
        # Here you can add code to save the message to a database or send an email
        print(f"Received message: {message}")
        
        cursor.execute("CREATE TABLE IF NOT EXISTS messages (message_id INT AUTO_INCREMENT PRIMARY KEY, message TEXT)")
        cursor.execute("SELECT * FROM messages WHERE message = %s", (message,))
        existing_message = cursor.fetchone()
        if existing_message:
            return jsonify({"status": 400, "message": "This message has already been submitted.", "code": 400})
        
        cursor.execute("INSERT INTO messages (message) VALUES (%s)", (message,))
        cursor.connection.commit()
        return jsonify({"status": 200, "message": "Issue raised successfully!"})
    
    return render_template("contact-us.html")

@issues.route("/raise-issue", methods=["POST", "GET"])
def raise_issue():
    if request.method == "POST":
        data = request.get_json()
        issue = data.get("issue")
        print(issue)
        email = data.get("email")
        access_token = data.get("access_token")
        if len(issue) > 1000:
            return jsonify({"status": 400, "message": "Issue is too long. Please limit it to 1000 characters.", "code": 400})
        
        if len(issue) < 10:
            return jsonify({"status": 400, "message": "Issue is too short. Please provide more details.", "code": 400})
        email = data.get("email")
        access_token = data.get("access_token")
        
        from app import cursor
        cursor.execute("SELECT * FROM users WHERE password = %s AND email = %s", (access_token, email))
        user = cursor.fetchone()
        if not user:
            return jsonify({"status": 401, "message": "Invalid access token or email.", "code": 401})
        # Here you can add code to save the message to a database or send an email
        print(f"Received issue: {issue}")
        
        cursor.execute("CREATE TABLE IF NOT EXISTS issues (message_id INT AUTO_INCREMENT PRIMARY KEY, message TEXT)")
        cursor.execute("SELECT * FROM issues WHERE message = %s", (issue,))
        existing_message = cursor.fetchone()
        if existing_message:
            return jsonify({"status": 400, "message": "This issue has already been submitted.", "code": 400})
        
        cursor.execute("INSERT INTO issues (message) VALUES (%s)", (issue,))
        cursor.connection.commit()
        return jsonify({"status": 200, "message": "Issue raised successfully!"})
    
    return render_template("index.html")