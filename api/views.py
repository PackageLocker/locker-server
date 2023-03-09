from flask import Blueprint, jsonify, request, make_response, current_app
from . import db
from .models import Package, User
import datetime as dt
from datetime import datetime
from .notification import notification
import locker
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps
import gspread

main = Blueprint('main', __name__)

# updates google sheet with action message
def update_sheet(package_data, message):
    wks = gspread.service_account().open("Knight Pickup Global Database").sheet1
    wks.insert_row(values=None, index=2)
    wks.update('A2', [[datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), package_data["locker_id"], message, package_data['student_id'], 
                       package_data["package_id"], package_data['name'], package_data['email']]])

def token_required(f):
    @wraps(f)
    def decorated(*arg, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return 'Token is missing', 401

        try:
            data = jwt.decode(
                token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return 'Token is invalid', 401

        return f(*arg, **kwargs)

    return decorated


@main.route('/user', methods=['GET'])
@token_required
def get_users():
    users = User.query.all()
    users_list = []
    for user in users:
        users_list.append({
            'id': user.id,
            'username': user.username,
            'password': user.password
        })
    return jsonify(users_list), 200


@main.route('/user', methods=['POST'])
@token_required
def create_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(username=data['username'], password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return 'New user created', 201


@main.route('/user/<id>', methods=['DELETE'])
@token_required
def delete_user(id):
    user = User.query.filter_by(id=id).first()

    if not user:
        return 'No user found!'

    db.session.delete(user)
    db.session.commit()

    return 'User deleted', 200


@main.route('/auth', methods=['POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return 'Missing username or password', 401

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return 'Could not verify username or password', 401

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({
            'exp': dt.datetime.utcnow() + dt.timedelta(minutes=30)},
            current_app.config['SECRET_KEY']
        )

        return jsonify({'token': token})

    return 'Could not verify', 401


@main.route('/new', methods=['POST'])
@token_required
def add_package():
    package_data = request.get_json()
    package = db.get_or_404(Package, package_data["locker_id"])
    package.package_id = package_data['package_id']
    package.name = package_data['name']
    package.student_id = package_data['student_id']
    package.email = package_data['email']
    package.available = False
    package.timestamp = package_data['timestamp']
    db.session.commit()

    update_sheet(package_data=package_data, message="DELIVERED") # Send delivery log message

    notification(package_data['email'])  # Send email to student

    locker.unlock(int(package_data['locker_id']))
    return 'Done', 201


@main.route('/packages', methods=['GET'])
@token_required
def packages():
    package_list = Package.query.all()
    packages = []

    for package in package_list:
        packages.append({
            'locker_id': package.locker_id,
            'package_id': package.package_id,
            'name': package.name,
            'student_id': package.student_id,
            'email': package.email,
            'available': package.available,
            'timestamp': package.timestamp
        })

    return jsonify(packages), 200


@main.route('/delete', methods=["DELETE"])
@token_required
def update_package():
    package_data = request.get_json()
    package = db.get_or_404(Package, package_data["locker_id"])
    update_sheet(package_data=package_data, message="REMOVED") # send log message to google sheet
    package.package_id = ""
    package.name = ""
    package.student_id = ""
    package.email = ""
    package.available = True
    package.timestamp = 0
    db.session.commit()

    return 'Done', 200


@main.route('/unlock', methods=['POST'])
@token_required
def unlock_locker():
    data = request.get_json()

    # Send log message to google sheet with empty fields
    wks = gspread.service_account().open("Knight Pickup Global Database").sheet1
    wks.insert_row(values=None, index=2)
    wks.update('A2', [[datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), data["locker_id"], "",
                       "", "", "", "UNLOCKED"]])
    
    locker.unlock(int(data['locker_id']))

    return 'Done', 200
