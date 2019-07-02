from emile import db


class Datum(db.Model):
    __tablename__ = 'data'

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
    isUser = db.Column(db.Boolean, nullable=False)
    content = db.Column(db.String(256))
    time = db.Column(db.DateTime)


    def __init__(self, userId, isUser, content, time):
        self.userId = userId
        self.isUser = isUser
        self.content = content
        self.time = time



class User(db.Model):
    __tablename__ = 'users'


    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(64), unique=True, index=True)
    currentPlan = db.Column(db.String(64))
    personalInfo = db.Column(db.String(128))


    def __init__(self, phone, currentPlan, personalInfo):
        self.phone = phone
        self.currentPlan = currentPlan
        self.personalInfo = personalInfo



class Record(db.Model):
    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.Date, nullable=False)
    isSlept = db.Column(db.Boolean, nullable=False)
    reason = db.Column(db.String)


    def __init__(self, userId, date, isSlept, reason):
        self.userId = userId
        self.date = date
        self.isSlept = isSlept
        self.reason = reason
