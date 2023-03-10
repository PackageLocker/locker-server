from . import db


class Package(db.Model):
    __tablename__ = "packages"

    locker_id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.String(50))
    name = db.Column(db.String(50))
    student_id = db.Column(db.String(20))
    email = db.Column(db.String(50))
    available = db.Column(db.Boolean())
    timestamp = db.Column(db.Integer)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(80))
