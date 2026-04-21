from flask import Blueprint, render_template, request, redirect, jsonify
from ...utils.user.user_utils import new_users_data, add_student, search_student
from ...utils.user.verify_user import check_email, verify_student_details

user = Blueprint('user', __name__)

@user.route("/login",methods=["GET", "POST"])
def LoginPage():
    if request.method == "POST":
        data = request.get_json();
        email = data.get("email")
        password = data.get("password")
        print(f"Received issue from {email}: {password}")
        
        if check_email(email):
            return jsonify({"status":200})
        else:
            return jsonify({"status":500})
        
    else:
        return render_template("login.html")


@user.route("/create-account", methods=["GET", "POST"])
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

@user.route("/verify-otp", methods=["GET", "POST"])
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
        from app import cursor, conn

        for user in new_users_data:
            print(user,email,type(otp))
            if user[0] == email and user[1] == int(otp) and not search_student(cursor, roll_no):
                add_student(cursor, conn, roll_no,username,email,current_study_year,hostel_no, clubs, password)
                new_users_data.remove(user)
                print("new user added successfully")
                return jsonify({"status": 200})
        print("Something went wrong. Please try again.")
        return jsonify({"status":500})
    else:
        return render_template("verify-otp.html")

