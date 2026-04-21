from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()


class User(db.Model):
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password