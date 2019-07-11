from flask import Flask
from flask_cors import CORS

from auth import auth
from user import users

app = Flask(__name__)
app.register_blueprint(auth.auth, url_prefix='/api/auth')
app.register_blueprint(users.user, url_prefix='/api/users')

CORS(app)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
