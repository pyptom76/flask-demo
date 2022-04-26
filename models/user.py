from db import db
# import json as jjson


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    u_name = db.Column(db.String(80))
    u_pass = db.Column(db.String(80))

    def __init__(self, username, password):
        self.u_name = username
        self.u_pass = password

    def json(self):
        return {'id': self.id, 'username': self.u_name, 'password': self.u_pass}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(u_name=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        users = cls.query.all()
        return users
