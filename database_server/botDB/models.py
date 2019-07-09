from botDB import db


class Table(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)

    def to_dict(self):
        dicttem = dict(self.__dict__)
        dicttem.pop('_sa_instance_state', None)
        if self.id != None:
            dicttem['id'] = self.id
        dicttem['time'] = str(self.time)
        return dicttem


class Plan(Table):
    __tablename__ = 'plans'

    id = db.Column(db.Integer, primary_key=True)
    weeklyBedtime = db.Column(db.String(64))
    weeklyFrequency = db.Column(db.String(4))
    __mapper_args__ = {'concrete': True}

    def __repr__(self):
        return '<Plan %r>' % (self.weeklyBedtime + self.weeklyFrequency)


class Datum(Table):
    __tablename__ = 'data'

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
    isUser = db.Column(db.Boolean, nullable=False)
    content = db.Column(db.String(256))
    time = db.Column(db.DateTime)
    __mapper_args__ = {'concrete': True}
   
    def __repr__(self):
        return '<Datum %r>' % self.id
    

class User(Table):
    __tablename__ = 'users'


    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(64))
    phone = db.Column(db.String(64), unique=True, index=True)
    timezone = db.Column(db.String(32))
    idealBedtime = db.Column(db.String(64))
    currentBedtime = db.Column(db.String(64))
    currentState = db.Column(db.String(64))
    weeklyPlanId = db.Column(db.Integer, db.ForeignKey('plans.id'))
    weeklyhit = db.Column(db.Integer)
    weeklymiss = db.Column(db.Integer)
    __mapper_args__ = {'concrete': True}

    def __repr__(self):
        return '<User %r>' % self.userName

class Record(Table):
    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
    weeklyPlanId = db.Column(db.Integer, db.ForeignKey('plans.id'))
    date = db.Column(db.Date, nullable=False)
    isSlept = db.Column(db.Boolean, nullable=False)
    reason = db.Column(db.String)
    __mapper_args__ = {'concrete': True}
    	
    def __repr__(self):
        return '<Record %r>' % self.id

class Admin(Table):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    adminName = db.Column(db.String(64))
    password = db.Column(db.String(64))
    __mapper_args__ = {'concrete': True}