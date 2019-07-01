import json

from flask import Flask, jsonify, request, abort


app = Flask(__name__)


@app.route('/users', methods=['GET'])
def get_users():
    with open('mock_database.json', 'r') as f:
        data = json.load(f)
        return jsonify({'users': data['users']})


@app.route('/users', methods=['POST'])
def create_user():
    if not request.json or not 'name' in request.json:
        abort(400)

    with open('mock_database.json', 'r') as f:
        data = json.load(f)
        users = data['users']

    with open('mock_database.json', 'w') as f:
        user = {
            'id': users[-1]['id'] + 1,
            'name': request.json['name'],
            'phone_number': request.json['phoneNumber'],
            'country_code': request.json['countryCode'],
            'email': request.json['email']
        }

        users.append(user)
        data['users'] = users
        json.dump(data, f)

    return jsonify({'user': user}), 201


@app.route('/users/<int:user_id>', methods=['DELETE'])
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


if __name__ == '__main__':
    app.run(debug=True, port=3000)