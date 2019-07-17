import requests
from Crypto.Hash import SHA

from config import database_url


def create_default_user():
    """
        Create default user
    """
    api_url = database_url + 'admin/create'
    sha = SHA.new()
    sha.update(b'magics')
    encryptedPassword = sha.hexdigest()
    data = {
        "adminName": "admin",
        "password": encryptedPassword,
    }
    requests.post(url=api_url, json=data)


# For test only
if __name__ == '__main__':
    create_default_user()