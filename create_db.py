from api.models import Package
from api import db, create_app
with create_app().app_context():
    db.create_all()
    for i in range(1, 6):
        new_package = Package(
            locker_id=i,
            package_id="",
            name="",
            student_id="",
            email="",
            available=True
        )
        db.session.add(new_package)
        db.session.commit()

# To view the datebase:
# sqlite3 instance/database.db
# SELECT * from packages
