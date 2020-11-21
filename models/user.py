from db import db


class UserModel(db.Model):
    __tablename__ = 'users'


    # These are the three columns the db are going to have
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))  # 80 is the character limit for the string
    password = db.Column(db.String(80))
    # ithe class variables e.g. self.etc must have same name as the columns to be stored in db

    def __init__(self, username, password):  # use _id as id is a python keyword
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
