import random
import smtplib

with open('.env') as f:
    lines = f.readlines()
    sender_email = lines[0].strip()
    sender_password = lines[1].strip()

def check_email(email):
    return True

def hash_password(password): 
    return password

def send_otp(email):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    otp = random.randint(100000,999999)
    s.starttls()
    s.login(sender_email, sender_password)
    message = f"Your OTP is {otp}"
    s.sendmail(sender_email,email, message)
    s.quit()
    return otp

def verify_student_details( email, current_study_year, hostel_no, password):
    if not check_email(email):
        raise Exception("Invalid Email ID")

    print(current_study_year, type(current_study_year))
    if int(current_study_year) not in [1, 2, 3, 4, 5]:
        raise Exception("Invalid Study Year")
    
    if int(hostel_no) not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
        raise Exception("Invalid Hostel Number")
    
    # if len(password) < 8:
    #     raise Exception("Password must be at least 8 characters long")
    
    # if not any(char.isdigit() for char in password):
    #     raise Exception("Password must contain at least one digit")
    
    # if not any(char.isupper() for char in password):
    #     raise Exception("Password must contain at least one uppercase letter")
    
    # if not any(char.islower() for char in password):
    #     raise Exception("Password must contain at least one lowercase letter")
    
    # if not any(char in "!@#$%^&*()-+ " for char in password):
    #     raise Exception("""
    #                Password must contain at least one special character from the set !@#$%^&*()-+
    #                """)
    
    # not_allowed_chars = "'\"\\/"
    # if any(char in not_allowed_chars for char in password):
    #     raise Exception(f"Password cannot contain any of the following characters: {not_allowed_chars}")

