import json
import datetime
from flask_script import Manager
from register import app



WTF_CSRF_ENABLED=False
app.permanent_session_lifetime = datetime.timedelta(seconds=8)
manager = Manager(app)


if __name__ == "__main__":
    manager.run()
