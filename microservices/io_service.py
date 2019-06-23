from flask import Flask, request, jsonify


app = Flask(__name__)

# This service will include an api for receiving a message as well as an api
# for outputting a message.

@app.route('/incoming/<id>', methods=['POST'])
def handle_incoming(id: str):
    incoming_message = request.json['message']
    # Add this message to a queue or further forward it to message handling service later
    print('Received input message for user %s: %s' % (id, incoming_message))
    return jsonify()
    

@app.route('/outgoing/<id>', methods=['POST'])
def handle_outgoing(id: str):
    outgoing_message = request.json['message']
    print('Received output message for user %s: %s' % (id, outgoing_message))
    return jsonify()
    

if __name__ == '__main__':
    app.run(debug=True)