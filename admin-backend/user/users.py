import json
import requests

from flask import request, jsonify, Blueprint, abort, current_app
from flask_cors import CORS

user = Blueprint('user', __name__,
                 template_folder='templates')
CORS(user)

database_api_base_url = 'http://127.0.0.1:5000'


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
        'timezone': '',
        'idealBedtime': '',
        'currentBedtime': '',
        'currentState': '',
        'weeklyHit': '0',
        'weeklyMiss': '0',
        'weeklyPlanId': '-1',
        'userChoiceA': '',
        'userChoiceB': '',
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
                'timezone': '',
                'idealBedtime': '',
                'currentBedtime': '',
                'currentState': '',
                'weeklyHit': '0',
                'weeklyMiss': '0',
                'weeklyPlanId': '-1',
                'userChoiceA': '',
                'userChoiceB': '',
                'userName': user['userName'],
                'phone': user['phone'],
            }
            if request.json['userName']:
                updated_user['userName'] = request.json['userName']
            if request.json['phone']:
                updated_user['phone'] = request.json['phone']

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


