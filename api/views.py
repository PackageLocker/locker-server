from flask import Blueprint, jsonify, request
from . import db
from .models import Package

main = Blueprint('main', __name__)


@main.route('/new', methods=['POST'])
def add_package():
    package_data = request.get_json()
    new_package = Package(
        locker_id=package_data['locker_id'],
        package_id=package_data['package_id'],
        name=package_data['name'],
        student_id=package_data['student_id'],
        email=package_data['email']
    )
    db.session.add(new_package)
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
            'email': package.email
        })

    return jsonify({'packages': packages}), 200


@main.route('/delete', methods=["DELETE"])
def update_package():
    package_data = request.get_json()
    package = db.get_or_404(Package, package_data["locker_id"])
    db.session.delete(package)
    db.session.commit()

    return 'Done', 201