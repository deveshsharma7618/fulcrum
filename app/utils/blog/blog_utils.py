
def create_blog_table(cursor, conn):
    try:
        cursor.execute("""
                   create table blogs(
                       id int primary key auto_increment,
                       title varchar(200) not null,
                       creator_email varchar(100) not null,
                       created_at timestamp default current_timestamp,
                       slug varchar(200) not null unique,
                       content text not null
                   );
                   """)
        conn.commit()
    except Exception as e:
        print("Blog table already exists")

def add_blog(cursor, conn, title, creator_email, slug, content):
    cursor.execute(f"insert into blogs(title,creator_email,slug,content) values('{title}','{creator_email}','{slug}','{content}')")
    conn.commit()


def get_n_blogs(cursor, n):
    cursor.execute("select * from blogs")
    blogs = cursor.fetchall()[:n]
    return blogs

def get_all_blogs(cursor):
    cursor.execute("select * from blogs")
    blogs = cursor.fetchall()
    return blogs

def get_blog_by_slug(cursor, slug):
    cursor.execute(f"select * from blogs where slug='{slug}'")
    blog = cursor.fetchone()
    return blog
