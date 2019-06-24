import requests

from flask import Flask, request, jsonify


app = Flask(__name__)
message_handling_service_url = 'http://127.0.0.1:5001'

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
    print('Received output message for user %s: %s' % (id, outgoing_message))
    return jsonify()
    

if __name__ == '__main__':
    app.run(debug=True, port=5000)