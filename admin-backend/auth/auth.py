import requests
from flask import request, jsonify, Blueprint
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from flask_cors import CORS
from config import database_url
import base64

auth = Blueprint('auth', __name__,
                 template_folder='templates')
CORS(auth)


@auth.route('/login', methods=['GET'])
def get_public_key():
    """
        Get RSA public key from server

        Returns:
            jsonified public key in format like:
            {
                'public_key': public_key
            }
    """
    ret_json = {}
    with open('./rsa_keys/rsa_1024_pub.pem') as pub:
        ret_json['public_key'] = pub.read()
    return jsonify(ret_json)


@auth.route('/login', methods=['POST'])
def login():
    """
        Login Authentication Interface

        Parameters:
            account: from request.json['account']
            password: from request.json['password']

        Returns:
            if login succeed
    """
    # SHA initialization
    sha = SHA.new()
    # get username and password(encrypted) from request
    account = request.json['account']
    password = request.json['password']
    decrypted_password = decrypt_password(password)
    sha.update(decrypted_password)
    sha_encrypted_password = sha.hexdigest()

    # TODO: Check database and validate the username and password
    api_url = database_url + 'admin/get'
    response = requests.get(url=api_url)
    if response.status_code == 200:
        admins = response.json()
        if admins['admin']['adminName'] == account and admins['admin']['password'] == sha_encrypted_password:
            return login_response('success')
    return login_response('fail')


def decrypt_password(password):
    """
        Decrypt the password which encrypted by public key

        Parameters:
            password (str): encrypted password (using public key)

        Returns:
            decrypted password or sentinel(default value: -1)
    """
    data = base64.b64decode(password)
    # load private key
    private_key = RSA.import_key(open('./rsa_keys/rsa_1024_priv.pem').read())

    # create cipher rsa using PKCS_v1_5
    cipher_rsa = PKCS1_v1_5.new(private_key)

    # if decrypt failed, sentinel will be returned
    sentinel = -1
    ret = cipher_rsa.decrypt(data, sentinel)
    return ret


def login_response(status):
    """
        Generate a login response in json format

        Parameters:
            status (str): login status(success or fail)

        Returns:
            jsonified login response
    """
    if status == 'success':
        return jsonify({
            'login_status': status,
            'message': 'Login succeed, redirecting...',
            'redirect': '/',
        })
    else:
        return jsonify({
            'login_status': status,
            'errors': 'Invalid account or password',
        })


def create_default_user():
    """
        Create default user
    """
    api_url = database_url + 'admin/update'
    sha = SHA.new()
    sha.update(b'magics')
    encryptedPassword = sha.hexdigest()
    data = {
        "adminName": "admin",
        "password": encryptedPassword,
    }
    requests.put(url=api_url, json=data)


# For test only
if __name__ == '__main__':
    create_default_user()
