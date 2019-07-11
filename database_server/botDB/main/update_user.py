from flask import request, session, redirect, url_for, current_app, jsonify, abort
from .. import db
from ..models import Datum, User, Record, Plan
from . import main




@main.route('/user/<int:user_id>/update', methods=['PUT'])
def update_user_info(user_id: int):
    if not request.json:
        abort(400)

    targetUser = User.query.get_or_404(user_id)
    updateDict = dict(request.json)
    if 'currentState' in updateDict:
        targetUser.currentState = updateDict['currentState']
    if  'idealBedtime'in updateDict:
        targetUser.idealBedtime = updateDict['idealBedtime']
    if  'currentBedtime'in updateDict:
        targetUser.currentBedtime = updateDict['currentBedtime']
    if  'timezone'in updateDict:
        targetUser.timezone = updateDict['timezone']
    if  'userChoiceA'in updateDict:
        targetUser.userChoiceA = updateDict['userChoiceA']
    if  'userChoiceB'in updateDict:
        targetUser.userChoiceB = updateDict['userChoiceB']
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
def update_changeplan(user_id: int):
    if not request.json:
        abort(400)

    updateWeeklyBedtime = request.json['weeklyBedtime']
    updateWeeklyFrequency = request.json['weeklyFrequency']
    updatePlan = Plan(weeklyFrequency = updateWeeklyFrequency, weeklyBedtime = updateWeeklyBedtime)
    db.session.add(updatePlan)
    db.session.commit()
    
    targetUser = User.query.get_or_404(user_id)
    targetUser.weeklyPlanId = updatePlan.id
    db.session.add(targetUser)
    db.session.commit()
    return jsonify({'user': targetUser.to_dict()}), 201
