from botDB import db


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
    
    def __repr__(self):
        return '<Datum %r>' % self.id
    
    def to_dict(self):
        dicttem = dict(self.__dict__)
        dicttem.pop('_sa_instance_state', None)
        if self.id != None:
            dicttem['id'] = self.id
        dicttem['time'] = str(self.time)
        return dicttem

class User(db.Model):
    __tablename__ = 'users'


    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(64))
    phone = db.Column(db.String(64), unique=True, index=True)
    currentPlan = db.Column(db.String(64))
    personalInfo = db.Column(db.String(128))


    def __init__(self, userName, phone, currentPlan, personalInfo):
        self.userName = userName
        self.phone = phone
        self.currentPlan = currentPlan
        self.personalInfo = personalInfo
    
    def __repr__(self):
        return '<User %r>' % self.userName
    
    def to_dict(self):
        dicttem = dict(self.__dict__)
        dicttem.pop('_sa_instance_state', None)
        if self.id != None:
            dicttem['id'] = self.id
        return dicttem

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
    
    def __repr__(self):
        return '<Record %r>' % self.id
    
    def to_dict(self):
        dicttem = dict(self.__dict__)
        dicttem.pop('_sa_instance_state', None)
        if self.id != None:
            dicttem['id'] = self.id
        dicttem['date'] = str(self.date)
        return dicttem