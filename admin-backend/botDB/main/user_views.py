from flask import request, session, redirect, url_for, current_app, jsonify
from .. import db
from ..models import Datum, User, Record
from . import main


@main.route('/test')
def test():
    allUser = User.query.all()
    us1 = User.query.get(1)
    udict = us1.to_dict()
    db.session.delete(us1)
    db.session.commit()
    return str(udict)


@main.route('/users', methods=['GET'])
def get_users():
    allUser = User.query.all()
    data = list()
    for u in allUser:
        data.append(u.to_dict())
    return jsonify({'users': data})


@main.route('/user/id/<int:user_id>', methods=['GET'])
def get_user_byID(user_id: int):
    targetUser = User.query.get_or_404(user_id)
    return jsonify({'user': targetUser.to_dict()}), 201

@main.route('/user/phone/<user_phone>', methods=['GET'])
def get_user_byPhone(user_phone):
    targetUser = User.query.filter_by(phone = user_phone).first_or_404()
    return jsonify({'user': targetUser.to_dict()}), 201

@main.route('/users', methods=['POST'])
def create_user():
    if not request.json:
        abort(400)

    newUser = User(userName = request.json['userName'], phone = request.json['phone'], currentPlan=request.json['currentPlan'], 
        personalInfo = request.json['personalInfo'])

    db.session.add(newUser)
    db.session.commit()
    return jsonify({'user': newUser.to_dict()}), 201


@main.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id: int):
    if not request.json:
        abort(400)

    targetUser = User.query.get_or_404(user_id)
    targetUser.userName = request.json['userName'] 
    targetUser.phone = request.json['phone']
    targetUser.currentPlan = request.json['currentPlan'] 
    targetUser.personalInfo = request.json['personalInfo']
    db.session.add(targetUser)
    db.session.commit()
    return jsonify({'user': targetUser.to_dict()}), 201
 


@main.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id: int):
    targetUser = User.query.get_or_404(user_id)
    targetDict = targetUser.to_dict()
    db.session.delete(targetUser)
    db.session.commit()

    return jsonify({'user': targetDict}), 201