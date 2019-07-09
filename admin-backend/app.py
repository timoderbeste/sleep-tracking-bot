from flask import Flask
from flask_cors import CORS

from auth import auth

app = Flask(__name__)
app.register_blueprint(auth.auth, url_prefix='/auth')
CORS(app)

if __name__ == '__main__':
    app.run()
