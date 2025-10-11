import random
import smtplib

with open('.creditionals.txt') as f:
    lines = f.readlines()
    sender_email = lines[0].strip()
    sender_password = lines[1].strip()

def check_email(email):
    if "@nitkkr.ac.in" not in email:
        return False
    
    roll_number = email.split("@")[0]
    for char in roll_number:
        if char not in "0123456789":
            return False
        
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

def verify_student_details(roll_no, name, email, current_study_year, password):
    if not check_email(email):
        raise Exception("Invalid Email ID")
    
    if str(roll_no) != email.split('@')[0]:
        raise Exception("Roll number and Email ID do not match")
    
    if len(str(roll_no)) != 9:
        raise Exception("Invalid Roll Number")

    if current_study_year not in [1, 2, 3, 4, 5]:
        raise Exception("Invalid Study Year")

    if len(password) < 8:
        raise Exception("Password must be at least 8 characters long")
    
    if not any(char.isdigit() for char in password):
        raise Exception("Password must contain at least one digit")
    
    if not any(char.isupper() for char in password):
        raise Exception("Password must contain at least one uppercase letter")
    
    if not any(char.islower() for char in password):
        raise Exception("Password must contain at least one lowercase letter")
    
    if not any(char in "!@#$%^&*()-+ " for char in password):
        raise Exception("""
                   Password must contain at least one special character from the set !@#$%^&*()-+
                   """)
    
    not_allowed_chars = "'\"\\/"
    if any(char in not_allowed_chars for char in password):
        raise Exception(f"Password cannot contain any of the following characters: {not_allowed_chars}")

