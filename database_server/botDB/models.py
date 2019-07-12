from botDB import db


class Table(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)

    def to_dict(self):
        dicttem = dict(self.__dict__)
        dicttem.pop('_sa_instance_state', None)
        if self.id != None:
            dicttem['id'] = self.id
        return dicttem


class Plan(Table):
    __tablename__ = 'plans'

    id = db.Column(db.Integer, primary_key=True)
    weeklyBedtime = db.Column(db.String(16))
    weeklyFrequency = db.Column(db.String(4))
    users = db.relationship('User', backref = 'plan')
    __mapper_args__ = {'concrete': True}

    def __repr__(self):
        return '<Plan %r>' % (self.weeklyBedtime + self.weeklyFrequency)


class Datum(Table):
    __tablename__ = 'data'

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
    isUser = db.Column(db.Boolean, nullable=False)
    content = db.Column(db.String(256))
    time = db.Column(db.String(32)) # example: '2018-02-03 15:37:12'
    __mapper_args__ = {'concrete': True}
   
    def __repr__(self):
        return '<Datum %r>' % self.id
    

class User(Table):
    __tablename__ = 'users'


    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(64))
    phone = db.Column(db.String(32), unique=True, index=True)
    timezone = db.Column(db.String(16))
    idealBedtime = db.Column(db.String(32))
    currentBedtime = db.Column(db.String(32))
    currentState = db.Column(db.String(32))
    weeklyPlanId = db.Column(db.Integer, db.ForeignKey('plans.id'))
    weeklyHit = db.Column(db.Integer)
    weeklyMiss = db.Column(db.Integer)
    userChoiceA = db.Column(db.String(32))
    userChoiceB = db.Column(db.String(32))
    records = db.relationship('Record', backref='user')
    data = db.relationship('Datum', backref='user')
    __mapper_args__ = {'concrete': True}

    def __repr__(self):
        return '<User %r>' % self.userName

class Record(Table):
    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
    weeklyPlanId = db.Column(db.Integer, db.ForeignKey('plans.id'))
    date = db.Column(db.String(16), nullable=False) # example: '2018-02-03'
    isSlept = db.Column(db.Boolean, nullable=False)
    reason = db.Column(db.String(128))
    __mapper_args__ = {'concrete': True}
    	
    def __repr__(self):
        return '<Record %r>' % self.id

class Admin(Table):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    adminName = db.Column(db.String(32))
    password = db.Column(db.String(32))
    __mapper_args__ = {'concrete': True}