from datetime import datetime
from flask import request, session, redirect, url_for, current_app, jsonify, abort
from .. import db
from ..models import Datum, User, Record
from . import main



@main.route('/data', methods=['GET'])
def get_data():
    allData = Datum.query.all()
    data = list()
    for d in allData:
        data.append(d.to_dict())
    return jsonify({'data': data})


@main.route('/datum/id/<int:data_id>', methods=['GET'])
def get_datum(data_id: int):
    targetData = Datum.query.get_or_404(data_id)
    return jsonify({'datum': targetData.to_dict()}), 201


@main.route('/datum', methods=['POST'])
def create_datum():
    if not request.json:
        abort(400)

    newDatum = Datum(userId = int(request.json['userId']), isUser = bool(request.json['isUser']), content = request.json['content'], 
        time = request.json['time']) 

    db.session.add(newDatum)
    db.session.commit()
    return jsonify({'datum': newDatum.to_dict()}), 201


@main.route('/datum/<int:data_id>', methods=['PUT'])
def update_datum(data_id: int):
    if not request.json:
        abort(400)

    targetDatum = Datum.query.get_or_404(data_id)
    targetDatum.userId = int(request.json['userId'])
    targetDatum.isUser = bool(request.json['isUser'])
    targetDatum.content = request.json['content']
    targetDatum.time = datetime.strptime(request.json['time'] , '%Y-%m-%d %H:%M:%S')
    db.session.add(targetDatum)
    db.session.commit()
    return jsonify({'user': targetDatum.to_dict()}), 201
 


@main.route('/datum/<int:data_id>', methods=['DELETE'])
def delete_datum(data_id: int):
    targetDatum = Datum.query.get_or_404(data_id)
    targetDict = targetDatum.to_dict()
    db.session.delete(targetDatum)
    db.session.commit()

    return jsonify({'datum': targetDict}), 201