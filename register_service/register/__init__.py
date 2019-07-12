from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)

DB_URL = 'http://127.0.0.1:5000/'
SMS_URL = 'http://69f52c2b.ngrok.io/'

class RegisterForm(FlaskForm):
    userName = StringField('Please enter your username', validators=[DataRequired()])
    phone = StringField('Please enter your phone number', validators=[DataRequired()])
    submit = SubmitField('Submit')


def add_user(userName, phone):
   URL = DB_URL + 'user/create'
   data = dict()
   data["userName"] = userName
   data["phone"] = phone
   requests.post(url = URL, json = data)

def notify_sms(phone):
   URL = SMS_URL + 'newuser'
   data = dict()
   data["phone"] = phone
   requests.post(url = URL, json = data)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = RegisterForm()
    if form.validate_on_submit():
        session['userName'] = form.userName.data
        session['phone'] = form.phone.data
        add_user(form.userName.data, form.phone.data)
        notify_sms(form.phone.data)
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('userName'))
