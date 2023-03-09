from api.models import Package, User
from api import db, create_app
from werkzeug.security import generate_password_hash, check_password_hash

LOCKER_NUM = 7

with create_app().app_context():
    db.create_all()
    for i in range(1, LOCKER_NUM+1):
        new_package = Package(
            locker_id=i,
            package_id="",
            name="",
            student_id="",
            email="",
            available=True,
            timestamp=0
        )
        db.session.add(new_package)
        db.session.commit()

    hashed_password = generate_password_hash('4admin', method='sha256')
    root_user = User(username='admin', password=hashed_password)
    db.session.add(root_user)
    db.session.commit()