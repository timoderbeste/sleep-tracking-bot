import json

from flask import Flask, request, jsonify, Blueprint, abort
from flask_cors import CORS

user = Blueprint('user', __name__,
                 template_folder='templates')
CORS(user)


@user.route('/', methods=['GET'])
def get_users():
    with open('mock_database.json', 'r') as f:
        data = json.load(f)
        return jsonify({'users': data['users']})


@user.route('/', methods=['POST'])
def create_user():
    if not request.json or not 'name' in request.json:
        abort(400)

    with open('mock_database.json', 'r') as f:
        data = json.load(f)
        users = data['users']

    user = {
        'id': users[-1]['id'] + 1 if len(users) != 0 else 1,
        'name': request.json['name'],
        'phone_number': request.json['phoneNumber'],
        'country_code': request.json['countryCode'],
        'email': request.json['email']
    }
    users.append(user)

    with open('mock_database.json', 'w') as f:
        data['users'] = users
        json.dump(data, f)

    return jsonify({'user': user}), 201


@user.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id: int):
    if not request.json:
        abort(400)

    with open('mock_database.json', 'r') as f:
        data = json.load(f)
        users = data['users']

    for user in users:
        if user['id'] == user_id:
            if request.json['name']:
                user['name'] = request.json['name']
            if request.json['phoneNumber']:
                user['phone_number'] = request.json['phoneNumber']
            if request.json['countryCode']:
                user['country_code'] = request.json['countryCode']
            if request.json['email']:
                user['email'] = request.json['email']

            with open('mock_database.json', 'w') as f:
                data['users'] = users
                json.dump(data, f)

            return jsonify({'user': user}), 201
    abort(404)


@user.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id: int):
    with open('mock_database.json', 'r') as f:
        data = json.load(f)
        users = data['users']

    user = [user for user in users if user['id'] == user_id]
    if len(user) == 0:
        abort(404)

    users.remove(user[0])
    with open('mock_database.json', 'w') as f:
        data['users'] = users
        json.dump(data, f)

    return jsonify({'user': user[0]}), 201
