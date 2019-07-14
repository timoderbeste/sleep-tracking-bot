import json
import requests

from routes import database_api_base_url
from flask import request, jsonify, Blueprint, abort, current_app
from flask_cors import CORS

plan = Blueprint('plan', __name__,
                 template_folder='templates')
CORS(plan)


@plan.route('/', methods=['GET'])
def get_plans():
    res = requests.get('%s/plans' % database_api_base_url)
    return jsonify({'plans': res.json()['plans']})


@plan.route('/', methods=['POST'])
def create_plan():
    if not request.json:
        abort(400)

    new_plan = {
        'weeklyBedtime': request.json['weeklyBedtime'],
        'weeklyFrequency': request.json['weeklyFrequency'],
    }

    headers = {
        'Content-type': 'application/json'
    }

    res = requests.post('%s/plan' % database_api_base_url, headers=headers, data=json.dumps(new_plan))

    if res.status_code == 201:
        return jsonify({'plan': new_plan}), 201
    else:
        abort(400)


@plan.route('/<int:plan_id>', methods=['PUT'])
def update_plan(plan_id: int):
    if not request.json:
        abort(400)

    plans = requests.get('%s/plans' % database_api_base_url).json()['plans']

    for plan in plans:
        if plan['id'] == plan_id:
            print(plan)
            updated_plan = plan
            if 'weeklyBedtime' in request.json:
                updated_plan['weeklyBedtime'] = request.json['weeklyBedtime']
            if 'weeklyFrequency' in request.json:
                updated_plan['weeklyFrequency'] = request.json['weeklyFrequency']

            headers = {
                'Content-type': 'application/json'
            }
            requests.put('%s/plan/%d' % (database_api_base_url, plan_id),
                         headers=headers, data=json.dumps(updated_plan))

            return jsonify({'plan': updated_plan}), 201
    abort(404)


@plan.route('/<int:plan_id>', methods=['DELETE'])
def delete_plan(plan_id: int):
    res = requests.delete('%s/plan/%d' % (database_api_base_url, plan_id))

    if res.status_code == 201:
        deleted_plan = res.json()
        return jsonify({'plan': deleted_plan}), 201
    abort(404)


