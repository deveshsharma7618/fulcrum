from .verify_user import verify_student_details
from ..sql.sql_verify import verify_sql_safe

def get_all_users(cursor):
    cursor.execute("select * from users")
    users = cursor.fetchall()
    return users

def create_user_table(cursor, conn):
    try:   
        cursor.execute("""
                   create table users(
                       roll_no int primary key,
                       name varchar(80) not null,
                       email varchar(80) not null unique,
                       hostel_no int,
                       clubs varchar(200),
                       current_study_year int,
                       password varchar(100) not null
                   );
                   """)
        conn.commit()
    except Exception as e:
        print("User table already exists")



def add_student(cursor, conn, roll_no,name,email, current_study_year, hostel_no, clubs, password):
    if not verify_sql_safe(email) or not verify_sql_safe(name) or not verify_sql_safe(clubs) or not verify_sql_safe(password) or not verify_sql_safe(str(current_study_year)) or not verify_sql_safe(str(hostel_no)):
        print("SQL Injection detected")
        return False
    cursor.execute(f"insert into users(roll_no,name,email,current_study_year,hostel_no, clubs, password) values({roll_no},'{name}','{email}',{current_study_year},'{hostel_no}','{clubs}','{password}')")
    conn.commit()
    return True

def search_student(cursor,roll_no, password):
    if not verify_sql_safe(str(roll_no)):
        return False
    
    cursor.execute(f"select * from users where roll_no={roll_no} and password='{password}'")
    user = cursor.fetchone()
    print(user)
    if user is None:
        return False
    else:
        return True


