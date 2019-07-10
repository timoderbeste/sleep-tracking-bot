from flask import request, session, redirect, url_for, current_app, jsonify, abort
from .. import db
from ..models import Datum, User, Plan, Plan
from . import main



@main.route('/plans', methods=['GET'])
def get_plans():
    allPlan = Plan.query.all()
    data = list()
    for p in allPlan:
        data.append(p.to_dict())
    return jsonify({'plans': data})


@main.route('/plan/id/<int:plan_id>', methods=['GET'])
def get_plan_byID(plan_id: int):
    targetPlan = Plan.query.get_or_404(plan_id)
    return jsonify({'plan': targetPlan.to_dict()}), 201


@main.route('/plan', methods=['POST'])
def create_plan():
    if not request.json:
        abort(400)

    newPlan = Plan(weeklyBedtime = request.json['weeklyBedtime'], weeklyFrequency = request.json['weeklyFrequency'])

    db.session.add(newPlan)
    db.session.commit()
    return jsonify({'plan': newPlan.to_dict()}), 201


@main.route('/plan/<int:plan_id>', methods=['PUT'])
def update_plan(plan_id: int):
    if not request.json:
        abort(400)

    targetPlan = Plan.query.get_or_404(plan_id)
    targetPlan.weeklyBedtime = request.json['weeklyBedtime']
    targetPlan.weeklyFrequency = request.json['weeklyFrequency']
    db.session.add(targetPlan)
    db.session.commit()
    return jsonify({'plan': targetPlan.to_dict()}), 201
 


@main.route('/plan/<int:plan_id>', methods=['DELETE'])
def delete_plan(plan_id: int):
    targetPlan = Plan.query.get_or_404(plan_id)
    targetDict = targetPlan.to_dict()
    db.session.delete(targetPlan)
    db.session.commit()

    return jsonify({'plan': targetDict}), 201