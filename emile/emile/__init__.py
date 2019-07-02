from emile.config import config_env_files
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
admin = Admin(app, name='emile admin', template_mode='bootstrap3')


def prepare_app(environment='development', p_db=db):
    p_db.init_app(app)
    app.config.from_object(config_env_files[environment])
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin.add_view(ModelView(User, p_db.session))
    # load views by importing them
    # from . import views
    return app

def save_and_commit(item):
    db.session.add(item)
    db.session.commit()
db.save = save_and_commit
