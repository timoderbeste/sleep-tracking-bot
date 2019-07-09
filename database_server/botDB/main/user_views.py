from flask import request, session, redirect, url_for, current_app, jsonify
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
    	weeklPlanId = int(request.json['weeklPlanId']), idealBedtime = request.json['idealBedtime'], currentBedtime = request.json['currentBedtime'], 
    	currentState = request.json['currentState'], weeklyHit = int(request.json['weeklyHit']), weeklyMiss = int(request.json['weeklyMiss']))

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
    targetUser.weeklPlanId = int(request.json['weeklPlanId'])
    db.session.add(targetUser)
    db.session.commit()
    return jsonify({'user': targetUser.to_dict()}), 201

@main.route('/user/<int:user_id>', methods=['PUT'])
def update_user_state(user_id: int):
    if not request.json:
        abort(400)

    targetUser = User.query.get_or_404(user_id)
    targetUser.currentState = request.json['currentState']
    db.session.add(targetUser)
    db.session.commit()
    return jsonify({'user': targetUser.to_dict()}), 201

@main.route('/user/<int:user_id>/hit++', methods=['PUT'])
def update_hit_plus(user_id: int):

    targetUser = User.query.get_or_404(user_id)
    targetUser.weeklyHit += 1
    db.session.add(targetUser)
    db.session.commit()
    return jsonify({'user': targetUser.to_dict()}), 201

@main.route('/user/<int:user_id>/hit--', methods=['PUT'])
def update_hit_minus(user_id: int):

    targetUser = User.query.get_or_404(user_id)
    targetUser.weeklyHit -= 1
    db.session.add(targetUser)
    db.session.commit()
    return jsonify({'user': targetUser.to_dict()}), 201

@main.route('/user/<int:user_id>/miss++', methods=['PUT'])
def update_miss_plus(user_id: int):
   
    targetUser = User.query.get_or_404(user_id)
    targetUser.weeklyMiss += 1
    db.session.add(targetUser)
    db.session.commit()
    return jsonify({'user': targetUser.to_dict()}), 201

@main.route('/user/<int:user_id>/miss--', methods=['PUT'])
def update_miss_minus(user_id: int):
    
    targetUser = User.query.get_or_404(user_id)
    targetUser.weeklyMiss -= 1
    db.session.add(targetUser)
    db.session.commit()
    return jsonify({'user': targetUser.to_dict()}), 201

@main.route('/user/<int:user_id>/missreset', methods=['PUT'])
def update_hit_reset(user_id: int):
    
    targetUser = User.query.get_or_404(user_id)
    targetUser.weeklyMiss = 0
    db.session.add(targetUser)
    db.session.commit()
    return jsonify({'user': targetUser.to_dict()}), 201

@main.route('/user/<int:user_id>/hitreset', methods=['PUT'])
def update_miss_reset(user_id: int):
    
    targetUser = User.query.get_or_404(user_id)
    targetUser.weeklyHit = 0
    db.session.add(targetUser)
    db.session.commit()
    return jsonify({'user': targetUser.to_dict()}), 201

@main.route('/user/<int:user_id>/changeplan', methods=['PUT'])
def update_miss_reset(user_id: int):
    if not request.json:
        abort(400)

    updateWeeklyBedtime = request.json['weeklyBedtime']
    updateWeeklyFrequency = request.json['weeklyFrequency']
    updatePlan = Plan(weeklyFrequency = updateWeeklyFrequency, weeklyBedtime = updateWeeklyBedtime)
    db.session.add(updatePlan)
    db.session.commit()
    
    targetUser = Plan.query.get_or_404(user_id)
    targetUser.weeklPlanId = updatePlan.id
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