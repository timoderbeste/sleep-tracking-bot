from flask import Flask, request, jsonify, Blueprint
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from flask_cors import CORS
import base64

auth = Blueprint('auth', __name__,
                 template_folder='templates')
CORS(auth)


"""
    Login Authentication Interface
    'GET': get public key
    'POST': send encrypted password(using public key) to backend and check the validation
"""


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if 'GET' == request.method:
        # pass public key to frontend
        ret_json = {}
        with open('./rsa_keys/rsa_1024_pub.pem') as pub:
            ret_json['public_key'] = pub.read()
        return jsonify(ret_json)
    elif 'POST' == request.method:
        # get username and password(encrypted) from request
        username = request.json['account']
        password = request.json['password']
        decrypted_password = decrypt_password(password)

        # TODO: Check database and validate the username and password

        # make return json
        res_json = {}
        if decrypt_password is not None:
            res_json['login_status'] = 'failed'
        else:
            res_json['login_status'] = 'succeed'

        return jsonify(res_json)


"""
    Decrypt the password which encrypted by public key
    password: encrypted password (using public key)
"""


def decrypt_password(password):
    data = base64.b64decode(password)
    # load private key
    private_key = RSA.import_key(open('./rsa_keys/rsa_1024_priv.pem').read())

    # create cipher rsa using PKCS_v1_5
    cipher_rsa = PKCS1_v1_5.new(private_key)

    # if decrypt failed, sentinel will be returned
    sentinel = -1
    ret = cipher_rsa.decrypt(data, sentinel)
    return ret

