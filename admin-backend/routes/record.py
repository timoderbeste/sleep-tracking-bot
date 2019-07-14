import json
import requests

from routes import database_api_base_url
from flask import request, jsonify, Blueprint, abort, current_app
from flask_cors import CORS

record = Blueprint('record', __name__,
                 template_folder='templates')
CORS(record)


@record.route('/', methods=['GET'])
def get_records():
    res = requests.get('%s/records' % database_api_base_url)
    return jsonify({'records': res.json()['records']})


@record.route('/', methods=['POST'])
def create_record():
    if not request.json:
        abort(400)

    new_record = {
        'userId': request.json['userId'],
        'reason': request.json['reason'],
        'isSlept': request.json['isSlept'],
        'date': request.json['date'],
        'weeklyPlanId': request.json['weeklyPlanId'],
    }

    headers = {
        'Content-type': 'application/json'
    }

    res = requests.post('%s/record' % database_api_base_url, headers=headers, data=json.dumps(new_record))

    if res.status_code == 201:
        return jsonify({'record': new_record}), 201
    else:
        abort(400)


@record.route('/<int:record_id>', methods=['PUT'])
def update_record(record_id: int):
    if not request.json:
        abort(400)

    records = requests.get('%s/records' % database_api_base_url).json()['records']

    for record in records:
        if record['id'] == record_id:
            print(record)
            updated_record = record
            if 'reason' in request.json:
                updated_record['reason'] = request.json['reason']
            if 'isSlept' in  request.json:
                updated_record['isSlept'] = request.json['isSlept']
            if 'date' in  request.json:
                updated_record['date'] = request.json['date']
            if 'weeklyPlanId' in  request.json:
                updated_record['weeklyPlanId'] = request.json['weeklyPlanId']

            headers = {
                'Content-type': 'application/json'
            }
            requests.put('%s/record/%d' % (database_api_base_url, record_id),
                         headers=headers, data=json.dumps(updated_record))

            return jsonify({'record': updated_record}), 201
    abort(404)


@record.route('/<int:record_id>', methods=['DELETE'])
def delete_record(record_id: int):
    res = requests.delete('%s/record/%d' % (database_api_base_url, record_id))

    if res.status_code == 201:
        deleted_record = res.json()
        return jsonify({'record': deleted_record}), 201
    abort(404)


