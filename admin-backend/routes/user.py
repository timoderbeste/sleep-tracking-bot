import json
import requests

from routes import database_api_base_url
from flask import request, jsonify, Blueprint, abort, current_app
from flask_cors import CORS

user = Blueprint('user', __name__,
                 template_folder='templates')
CORS(user)


@user.route('/', methods=['GET'])
def get_users():
    res = requests.get('%s/users' % database_api_base_url)
    return jsonify({'users': res.json()['users']})


@user.route('/', methods=['POST'])
def create_user():
    if not request.json or not 'userName' in request.json:
        abort(400)

    new_user = {
        'userName': request.json['userName'],
        'phone': request.json['phone'],
        'timezone': request.json['timezone'] if 'timezone' in request.json
        else '',
        'idealBedtime': request.json['idealBedtime'] if 'idealBedtime' in request.json
        else '',
        'currentBedtime': request.json['currentBedtime'] if 'currentBedtime' in request.json
        else '',
        'currentState': request.json['currentState'] if 'currentState' in request.json
        else '',
        'weeklyHit': request.json['weeklyHit'] if 'weeklyHit' in request.json and request.json['weeklyHit']
        else 0,
        'weeklyMiss': request.json['weeklyMiss'] if 'weeklyMiss' in request.json and request.json['weeklyMiss']
        else 0,
        'weeklyPlanId': request.json['weeklyPlanId'] if 'weeklyPlanId' in request.json and request.json['weeklyPlanId']
        else -1,
        'userChoiceA': request.json['userChoiceA'] if 'userChoiceA' in request.json
        else '-1',
        'userChoiceB': request.json['userChoiceB'] if 'userChoiceB' in request.json
        else '-1',
    }

    headers = {
        'Content-type': 'application/json'
    }

    res = requests.post('%s/user' % database_api_base_url, headers=headers, data=json.dumps(new_user))

    if res.status_code == 201:
        return jsonify({'user': new_user}), 201
    else:
        abort(400)


@user.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id: int):
    if not request.json:
        abort(400)

    users = requests.get('%s/users' % database_api_base_url).json()['users']

    for user in users:
        if user['id'] == user_id:
            print(user)
            updated_user = {
                'userName': request.json['userName']
                if 'userName' in request.json else user['userName'],
                'phone': request.json['phone']
                if 'phone' in request.json else user['phone'],
                'timezone': request.json['timezone']
                if 'timezone' in request.json else user['timezone'],
                'idealBedtime': request.json['idealBedtime']
                if 'idealBedtime' in request.json else user['idealBedtime'],
                'currentBedtime': request.json['currentBedtime']
                if 'currentBedtime' in request.json else user['currentBedtime'],
                'currentState': request.json['currentState']
                if 'currentState' in request.json else user['currentState'],
                'weeklyHit': request.json['weeklyHit']
                if 'weeklyHit' in request.json else user['weeklyHit'],
                'weeklyMiss': request.json['weeklyMiss']
                if 'weeklyMiss' in request.json else user['weeklyMiss'],
                'weeklyPlanId': request.json['weeklyPlanId']
                if 'weeklyPlanId' in request.json else user['weeklyPlanId'],
                'userChoiceA': request.json['userChoiceA']
                if 'userChoiceA' in request.json else user['userChoiceA'],
                'userChoiceB': request.json['userChoiceB']
                if 'userChoiceB' in request.json else user['userChoiceB'],
            }

            headers = {
                'Content-type': 'application/json'
            }
            requests.put('%s/user/%d' % (database_api_base_url, user_id), headers=headers, data=json.dumps(updated_user))

            return jsonify({'user': updated_user}), 201
    abort(404)


@user.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id: int):
    res = requests.delete('%s/user/%d' % (database_api_base_url, user_id))

    if res.status_code == 201:
        deleted_user = res.json()
        return jsonify({'user': deleted_user}), 201
    abort(404)


