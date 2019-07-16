from flask import request, session, redirect, url_for, current_app, jsonify, abort
from .. import db
from ..models import Datum, User, Record, Plan
from . import main



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




@main.route('/user', methods=['POST'])
def create_user():
    if not request.json:
        abort(400)

    newUser = User(userName = request.json['userName'], phone = request.json['phone'], timezone = request.json['timezone'], 
    	weeklyPlanId = int(request.json['weeklyPlanId']), idealBedtime = request.json['idealBedtime'], currentBedtime = request.json['currentBedtime'], 
    	currentState = request.json['currentState'], weeklyHit = int(request.json['weeklyHit']), weeklyMiss = int(request.json['weeklyMiss']),
    	userChoiceA = request.json['userChoiceA'], userChoiceB = request.json['userChoiceB'])

    db.session.add(newUser)
    db.session.commit()
    return jsonify({'user': newUser.to_dict()}), 201

@main.route('/user/create', methods=['POST'])
def create_newuser():
    if not request.json:
        abort(400)

    newUser = User(userName = request.json['userName'], phone = request.json['phone'], weeklyMiss = 0, weeklyHit = 0, weeklyPlanId = 0)

    db.session.add(newUser)
    db.session.commit()
    return jsonify({'user': newUser.to_dict()}), 201




@main.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id: int):
    if not request.json:
        abort(400)

    targetUser = User.query.get_or_404(user_id)
    targetUser.userName = request.json['userName'] 
    targetUser.phone = request.json['phone']
    targetUser.timezone = request.json['timezone']
    targetUser.idealBedtime = request.json['idealBedtime']
    targetUser.currentBedtime = request.json['currentBedtime']
    targetUser.currentState = request.json['currentState']
    targetUser.weeklyHit = int(request.json['weeklyHit'])
    targetUser.weeklyMiss = int(request.json['weeklyMiss'])
    targetUser.weeklyPlanId = int(request.json['weeklyPlanId'])
    db.session.add(targetUser)
    db.session.commit()
    
    return jsonify({'user': targetUser.to_dict()}), 201


@main.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id: int):
    targetUser = User.query.get_or_404(user_id)
    targetDict = targetUser.to_dict()
    db.session.delete(targetUser)
    db.session.commit()

    return jsonify({'user': targetDict}), 201


