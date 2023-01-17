from . import db


class Package(db.Model):
    __tablename__ = "packages"

    id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.String(50))
    name = db.Column(db.String(50))
    student_id = db.Column(db.String(20))
    email = db.Column(db.String(50))
