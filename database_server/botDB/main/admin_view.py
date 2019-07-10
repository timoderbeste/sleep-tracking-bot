from flask import request, session, redirect, url_for, current_app, jsonify, abort
from .. import db
from ..models import Admin
from . import main



@main.route('/admin/get', methods=['GET'])
def get_admin():
    admin = Admin.query.first()
    return jsonify({'admin': admin.to_dict()})



@main.route('/admin/create', methods=['POST'])
def create_admin():

    admin = Admin(adminName = request.json['adminName'], password = request.json['password'])

    db.session.add(admin)
    db.session.commit()
    return jsonify({'admin': admin.to_dict()}), 201


@main.route('/admin/update', methods=['PUT'])
def update_admin():
    if not request.json:
        abort(400)

    targetadmin = Admin.query.first()
    updateDict = dict(request.json)
    if 'adminName' in updateDict:
        targetadmin.adminName = updateDict['adminName']
    if  'password'in updateDict:
        targetadmin.password = updateDict['password']
    db.session.add(targetadmin)
    db.session.commit()
    return jsonify({'user': targetadmin.to_dict()}), 201