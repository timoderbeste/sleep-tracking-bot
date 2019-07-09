from flask import request, session, redirect, url_for, current_app, jsonify
from .. import db
from ..models import Datum, User, Record
from . import main



@main.route('/records', methods=['GET'])
def get_records():
    allRecord = Record.query.all()
    data = list()
    for r in allRecord:
        data.append(r.to_dict())
    return jsonify({'records': data})


@main.route('/record/id/<int:record_id>', methods=['GET'])
def get_record_byID(record_id: int):
    targetRecord = Record.query.get_or_404(record_id)
    return jsonify({'record': targetRecord.to_dict()}), 201


@main.route('/record', methods=['POST'])
def create_record():
    if not request.json:
        abort(400)

    newRecord = Record(weeklPlanId = int(request.json['weeklPlanId']), userId = int(request.json['userId']), reason = request.json['reason'],
     isSlept = bool(request.json['isSlept']), date = request.json['date']) # example: '2018-02-03'

    db.session.add(newRecord)
    db.session.commit()
    return jsonify({'record': newRecord.to_dict()}), 201


@main.route('/record/<int:record_id>', methods=['PUT'])
def update_record(record_id: int):
    if not request.json:
        abort(400)

    targetRecord = Record.query.get_or_404(record_id)
    targetRecord.weeklPlanId = int(request.json['weeklPlanId'])
    targetRecord.userId = int(request.json['userId'])
    targetRecord.reason = request.json['reason']
    targetRecord.isSlept = bool(request.json['isSlept'])
    targetRecord.date = request.json['date']
    db.session.add(targetRecord)
    db.session.commit()
    return jsonify({'record': targetRecord.to_dict()}), 201
 


@main.route('/record/<int:record_id>', methods=['DELETE'])
def delete_record(record_id: int):
    targetRecord = Record.query.get_or_404(record_id)
    targetDict = targetRecord.to_dict()
    db.session.delete(targetRecord)
    db.session.commit()

    return jsonify({'record': targetDict}), 201