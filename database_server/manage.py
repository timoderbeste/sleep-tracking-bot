#!/usr/bin/env python
import json
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_migrate import upgrade as upgrade_database
from botDB import app, prepare_app, db, parsers
from botDB.models import Datum, User, Record

prepare_app(environment='development')
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

        
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


# @manager.command
# def dbseed():
#     with open('user.json') as user_file:
#         user_json_string = user_file.read()
#         db.save(parsers.user_from_json(user_json_string))


if __name__ == "__main__":
    manager.run()
