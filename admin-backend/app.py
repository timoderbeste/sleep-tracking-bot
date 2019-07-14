#!/usr/bin/env python
from flask import Flask
from flask_cors import CORS

from routes import auth
from routes import user
from routes import record
from routes import plan


app = Flask(__name__)
app.register_blueprint(auth.auth, url_prefix='/api/auth')
app.register_blueprint(user.user, url_prefix='/api/users')
app.register_blueprint(record.record, url_prefix='/api/records')
app.register_blueprint(plan.plan, url_prefix='/api/plans')

CORS(app)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
