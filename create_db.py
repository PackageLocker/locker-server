from api.models import Package
from api import db, create_app
with create_app().app_context():
    db.create_all()

# To view the datebase:
# sqlite3 instance/database.db
# SELECT * from packages
