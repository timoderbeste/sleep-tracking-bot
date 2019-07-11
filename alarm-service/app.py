import argparse
import requests
import json
from datetime import datetime

import flask
from flask import request, jsonify, abort
from apscheduler.schedulers.background import BackgroundScheduler


app = flask.Flask('alarm-service')
scheduler = BackgroundScheduler()
data_storage = {}


def print_datetime():
    print('The time is: %s' % datetime.now())


def alert(callback_address: str, job_id: str):
    with app.app_context():
        data = data_storage[job_id]
        try:
            headers = {'Content-type': 'application/json'}
            requests.post(callback_address, data=json.dumps(data), headers=headers)
        except requests.exceptions.InvalidSchema:
            print('No connection available to %s' % callback_address)
            print('Data is %s' % json.dumps(data))
        except requests.exceptions.ConnectionError:
            print('No connection available to %s' % callback_address)
            print('Data is %s' % json.dumps(data))


@app.route('/', methods=['GET'])
def index():
    return 'This is the alarm service. Please refer to the documentation for more details.'


@app.route('/alert', methods=['POST'])
def alerted():
    print('Alerted')


@app.route('/register', methods=['POST'])
def register_alarm():
    if not request.json:
        abort(400)
    data = request.json
    if 'task_id' not in data or 'event_name' not in data or 'timer_opts' not in data or 'data' not in data:
        abort(400)

    if 'trigger' not in data['timer_opts']:
        abort(400)

    if 'interval' not in data['timer_opts']['trigger'] and 'date' not in data['timer_opts']['trigger']:
        abort(400)

    job_id = '%s-%s' % (data['task_id'], data['event_name'])
    if scheduler.get_job(job_id):
        abort(400)
    data['timer_opts']['id'] = job_id

    try:
        scheduler.add_job(alert, args=[data['callback_address'], job_id], **data['timer_opts'])
        data_storage[job_id] = data['data']
    except TypeError:
        abort(400)
    return jsonify({'job_id': job_id}), 203


@app.route('/deregister', methods=['POST'])
def deregister_alarm():
    if not request.json:
        abort(400)

    data = request.json
    if not data['task_id'] or not data['event_name']:
        abort(400)

    job_id = '%s-%s' % (data['task_id'], data['event_name'])
    if not scheduler.get_job(job_id):
        abort(404)
    scheduler.remove_job(job_id)
    del data_storage[job_id]
    return 'Deregistered', 203


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--port', type=int, required=False)
    args = arg_parser.parse_args()

    scheduler.start()

    app.config['DEBUG'] = True
    app.run(port=(None if not args.port else args.port))


if __name__ == '__main__':
    main()
