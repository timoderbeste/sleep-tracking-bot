import requests
from twilio.rest import Client

from flask import Flask, request, jsonify


app = Flask(__name__)
message_handling_service_url = 'http://127.0.0.1:5001'

# Edited by jingya
account_sid = 'AC96667ba222e43cae8b9857372b6b6709'
auth_token = 'cf369e037a592bbcf0497e113bae68eb'
client = Client(account_sid, auth_token)
host_phone_num = '+16197623257' # twilio number
outgoing_phone_num = '+16192281477' # jingya
###

# This service will include an api for receiving a message as well as an api
# for outputting a message.

@app.route('/incoming/<id>', methods=['POST'])
def handle_incoming(id: str):
    incoming_message = request.json['message']
    print('Received input message for user %s: %s' % (id, incoming_message))
    requests.post('%s/incoming/%s' % (message_handling_service_url, id), json={'message': incoming_message})
    return jsonify()


@app.route('/outgoing/<id>', methods=['POST'])
def handle_outgoing(id: str):
    outgoing_message = request.json['message']
    # TODO use twilo etc to send the message to the correct user.
    # Edited by jingya
    message = client.messages \
                .create(
                     body=outgoing_messagne,
                     from_=,
                     to=outgoing_phone_num
                 )
    ###
    print('Received output message for user %s: %s' % (id, outgoing_message))
    return jsonify()


if __name__ == '__main__':
    app.run(debug=True, port=5000)
