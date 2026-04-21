
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




new_users_data = [["125102009@nitkkr.ac.in",999999]]




def add_student(cursor, conn, roll_no,name,email, current_study_year, hostel_no, clubs, password):
    verify_student_details(email, current_study_year,hostel_no, password)
    cursor.execute(f"insert into users(roll_no,name,email,current_study_year,hostel_no, clubs, password) values({roll_no},'{name}','{email}',{current_study_year},'{hostel_no}','{clubs}','{password}')")
    conn.commit()

def search_student(cursor,roll_no):
    cursor.execute(f"select * from users where roll_no={roll_no}")
    user = cursor.fetchone()
    print(user)
    if user is None:
        return False
    else:
        return True


