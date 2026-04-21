from flask import Blueprint, render_template, request, redirect, jsonify
from ...utils.user.user_utils import  add_student, search_student
from ...utils.user.verify_user import check_email, verify_student_details, send_otp
import time
from ...utils.sql.sql_verify import verify_sql_safe
import bcrypt

user = Blueprint('user', __name__)

new_users_data = [{
    "email": "125102009@nitkkr.ac.in",
    "otp": "999999",
    "expired_time": 2776770918.351186
    }] # Temporary storage for new users' email and OTP

@user.route("/login",methods=["GET", "POST"])
def LoginPage():
    if request.method == "POST":
        data = request.get_json() or {}
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            return jsonify({"status": 400, "message": "Email and password are required."})
        
        if check_email(email) and verify_sql_safe(email) and verify_sql_safe(password):
            from app import cursor
            cursor.execute("select * from users where email=%s", (email,))
            student = cursor.fetchone()
            if student is None:
                return jsonify({"status": 401, "message": "Invalid credentials."})
            
            access_token = student[6]
            if not bcrypt.checkpw(password.encode('utf-8'), access_token.encode('utf-8')):
                return jsonify({"status": 401, "message": "Invalid credentials."})

            return jsonify({"status":200, "access_token": access_token,"roll_no" : student[0], "username" : student[1],   "email" : student[2], "current_study_year" : student[5],
                            "clubs" : student[4], "hostel_no" : student[3]})
        
        else:
            return jsonify({"status":400, "message": "Invalid login payload."})
        
    else:
        return render_template("login.html")


@user.route("/create-account", methods=["GET", "POST"])
def CreateAccount():
    if request.method == "POST":
        email = request.get_json().get("email")
        if check_email(email) == False:
            return jsonify({"status": 500, "message": "Invalid Email ID"})
        
        for user in new_users_data:
            if user.get("email") == email and user.get("expired_time") < time.time():
                return render_template("verify-otp.html", message="OTP already sent to this email", otp_sent_to=email, otp = user.get("otp"))
            elif user.get("email") == email and user.get("expired_time") > time.time():
                new_users_data.remove(user)
                break
            
        # otp = send_otp(email)
        otp = 999999
        new_users_data.append({"email": email, "otp": otp, "expired_time": time.time() + 300})  # OTP expires in 5 minutes

        return render_template("verify-otp.html", otp_sent_to=email, otp = otp)
    else:
        return render_template("create-account.html")

@user.route("/verify-otp", methods=["GET", "POST"])
def VerifyOTP():
    if request.method == "POST":
        data = request.get_json() or {}
        email = data.get("email")
        if not email:
            return jsonify({"status": 400, "message": "Email is required."})

        roll_no = email.split('@')[0]
        
        
        otp = data.get("otp")
        username = data.get("username")
        current_study_year = data.get("current_study_year")
        hostel_no = data.get("hostel_no")
        clubs = data.get("clubs")
        password = data.get("password")

        try:
            verify_student_details(email=email, current_study_year=current_study_year, hostel_no=hostel_no, password=password)
        except Exception as e:
            return jsonify({"status": 400, "message": str(e)})

        try:
            otp_value = int(otp)
        except (TypeError, ValueError):
            return jsonify({"status": 400, "message": "Invalid OTP format."})
        
        from app import cursor, conn
        access_token = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        for user in new_users_data:
            if user.get("email") == email and user.get("otp") == otp_value and user.get("expired_time") > time.time() and not search_student(cursor, roll_no, access_token):
                if add_student(cursor, conn, roll_no,username,email,current_study_year,hostel_no, clubs, access_token): 
                    new_users_data.remove(user)
                    return jsonify({"status": 200, "message": "User created successfully", "email": email, "username": username, "current_study_year": current_study_year, "hostel_no": hostel_no, "clubs": clubs, "access_token": access_token})

        return jsonify({"status":500, "message": "Message: OTP is wrong or expired, or user already exists."})
    else:
        return render_template("verify-otp.html")

