from flask import Blueprint, jsonify, request
from . import db
from .models import Package
from datetime import datetime
import locker

main = Blueprint('main', __name__)


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
    locker.unlock(int(data['locker_id']))

    return 'Done', 200
