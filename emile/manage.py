import json
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_migrate import upgrade as upgrade_database
from emile import app, prepare_app
from emile.obs_design_pattern import Subject, Observer
from emile.concrete_observer import ConcreteObserver
from emile.survey_view import send_message, concrete_subject

#prepare_app(environment='development')
#migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

USER_NUM = '+16192281477' # jingya
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


@manager.command
def dbseed():
    with open('survey.json') as survey_file:
        survey_json_string = survey_file.read()
        db.save(parsers.survey_from_json(survey_json_string))


if __name__ == "__main__":
    manager.run()
