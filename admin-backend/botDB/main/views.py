from flask import session, redirect, url_for, current_app
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
        udict = u.to_dict
        udict['id'] = u.id
        data.append(u.dict)
        return jsonify({'users': data})


@main.route('/users', methods=['POST'])
def create_user():
    if not request.json or not 'name' in request.json:
        abort(400)

    with open('mock_database.json', 'r') as f:
        data = json.load(f)
        users = data['users']

    newUser = User(userName = request.json['userName'], phone = request.json['phone'], currentPlan=request.json['currentPlan'], 
        personalInfo = request.json['personalInfo'])

    db.session.add(newUser)
    db.session.commit()
    newUserDict = newUser.to_dict
    newUserDict['id'] = newUser.id
    return jsonify({'user': newUserDict}), 201


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
 


@main.route('/users/<int:user_id>', methods=['DELETE'])
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