from flask import Blueprint, jsonify, request
from . import db
from .models import Package, User
from datetime import datetime
from .notification import Notification
# import locker
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)

@main.route('/user', methods=['GET'])
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
def create_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(username=data['username'], password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return 'New user created', 201


@main.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.filter_by(id=id).first()

    if not user:
        return 'User not found!'

    db.session.delete(user)
    db.session.commit()

    return 'User deleted', 200


@main.route('/new', methods=['POST'])
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

    Notification(package_data['email']) # Send email to student

    # locker.unlock(int(package_data['locker_id']))
    return 'Done', 201


@main.route('/packages', methods=['GET'])
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
def update_package():
    package_data = request.get_json()
    package = db.get_or_404(Package, package_data["locker_id"])
    package.package_id = ""
    package.name = ""
    package.student_id = ""
    package.email = ""
    package.available = True
    package.timestamp = 0
    db.session.commit()

    return 'Done', 200


@main.route('/unlock', methods=['POST'])
def unlock_locker():
    data = request.get_json()
    # locker.unlock(int(data['locker_id']))

    return 'Done', 200
