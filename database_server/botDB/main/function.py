from flask import request, session, redirect, url_for, current_app, jsonify, abort
from .. import db
from ..models import Datum, User, Record, Plan
from . import main



@main.route('/user/id/<int:user_id>/reason', methods=['GET'])
def get_reason(user_id: int):
    targetUser = User.query.get_or_404(user_id)
    records = targetUser.records
    reasonDict = dict()
    for r in records:
        if r.reason not in reasonDict:
            reasonDict[r.reason] = 1
        else: reasonDict[r.reason] += 1
    reasonDict = dict(sorted(reasonDict.items(), key=lambda d: d[1], reverse = True)[:3])

    return jsonify({'reason': reasonDict})