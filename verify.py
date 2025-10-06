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
