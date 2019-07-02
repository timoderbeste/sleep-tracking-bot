import json
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_migrate import upgrade as upgrade_database
from emile import app, prepare_app, db, parsers
from emile.models import Datum, User, Record
from emile.obs_design_pattern import Subject, Observer
from emile.concrete_observer import ConcreteObserver
from emile.survey_view import send_message, concrete_subject

prepare_app(environment='development')
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

USER_NUM = '+18728066767' # yun
#USER_NUM = "+12244200851" # zhihan

#subject = Subject()
concrete_observer = ConcreteObserver(USER_NUM)
concrete_observer.initiate_conversation()
#subject.attach(concrete_observer)
concrete_subject.attach(concrete_observer)
        
@manager.command
def test():
    """Run the unit tests."""
    import sys
    import unittest
    prepare_app(environment='test')
    upgrade_database()
    tests = unittest.TestLoader().discover('.', pattern="*_tests.py")
    test_result = unittest.TextTestRunner(verbosity=2).run(tests)

    if not test_result.wasSuccessful():
        sys.exit(1)
# 

@manager.command
def dbseed():
    with open('user.json') as user_file:
        user_json_string = user_file.read()
        db.save(parsers.user_from_json(user_json_string))


if __name__ == "__main__":
    
    manager.run()
    us1 = User(phone='11111', currentPLan='123456', personalInfo='wang')
    us2 = User(phone='22222', currentPLan='201512', personalInfo='zhang')
    us3 = User(phone='33333', currentPLan='987654', personalInfo='chen')
    us4 = User(phone='44444', currentPLan='456789', personalInfo='zhou')
    db.session.add_all([us1, us2, us3, us4])
    db.session.commit()
