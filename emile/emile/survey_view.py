from . import app
from flask import url_for, session, request
from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse
from .obs_design_pattern import Subject, Observer
from twilio.rest import Client
import datetime
import json

class ConcreteSubject(Subject):
    _state: int = 0
    _observers = []

    def attach(self, observer: Observer) -> None:
        print("Subject: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, msg, state) -> None:
        print("notifying observers")
        print(len(self._observers))
        for observer in self._observers:
            observer.update(msg, state)

# The session object makes use of a secret key.
SECRET_KEY = 'a secret key'

# Try adding your own number to this list!
callers = {
    "+19172148443": "Timo",
    "+16192281477": "Jingya",
}

account_sid = 'AC96667ba222e43cae8b9857372b6b6709'
auth_token = 'cf369e037a592bbcf0497e113bae68eb'
client = Client(account_sid, auth_token)
TWILIO_NUM = '+12565703455'
OUTPUT_FILE = 'smsbot_log.json'
state_counter = 0

concrete_subject = ConcreteSubject()

def send_message(message, user_number):
    message = client.messages \
                    .create(
                         body=message,
                         from_=TWILIO_NUM,
                         to=user_number # jingya
                     )
                     
@app.route("/sms", methods=['GET', 'POST'])
def get_message():
    global concrete_subject
    global msg_bank
    global state_counter

    from_number = request.values.get('From')
    print("current state is: {}".format(concrete_subject._state))

    # process received message
    incoming_msg = request.values.get('Body')
    with open(OUTPUT_FILE, 'a') as f:
        f.write("\"source\":\"user\",\"time\":\""+str(datetime.datetime.now())+"\",\"body\":\""+incoming_msg+"\"}\n")
        print("incoming message body: {}".format(incoming_msg))
    concrete_subject.notify(incoming_msg, concrete_subject._state)

    resp = MessagingResponse()
    return str(resp)
