import json
from botDB.config import config_env_files
from flask import Flask, jsonify
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
app = Flask(__name__)



def prepare_app(environment='development', p_db=db):
    p_db.init_app(app)
    app.config.from_object(config_env_files[environment])
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app

def save_and_commit(item):
    db.session.add(item)
    db.session.commit()
db.save = save_and_commit
