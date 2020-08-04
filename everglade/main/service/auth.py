from __future__ import annotations
from typing import Dict, Tuple

import os
import json
from requests.exceptions import HTTPError

import pyrebase
import firebase_admin
from firebase_admin import auth, credentials

from everglade.main.constants.constants import config

print(os.environ.get('IS_HEROKU', 'UNPOG'))
print(config)
fb = pyrebase.initialize_app(config)
pyre_auth = fb.auth()

with open('everglade/main/service/cred/credentials.json', 'w') as outfile:
    json.dump({
    "type": "service_account",
    "project_id": "f-messaging",
    "private_key_id": "f",
    "private_key": "f",
    "client_email": "f",
    "client_id": "f",
    "auth_uri": "f",
    "token_uri": "f",
    "auth_provider_x509_cert_url": "f",
    "client_x509_cert_url": "f"}, outfile)

#cred = credentials.Certificate('everglade/main/service/cred/credentials.json') # Run this for production server
#cred = credentials.Certificate('everglade/main/service/ignore/credentials.json') # Run this for local server
firebase = firebase_admin.initialize_app()

def authLogin(email: str, password: str) -> Tuple[Dict, int]:
    """ Logs in the user using the email and password
    
    Returns the response and the status code
    """
    try:
        user = pyre_auth.sign_in_with_email_and_password(email, password)

        return { "token": user["idToken"] }, 200
    except:
        return { "message": "Login Error" }, 400
        # response_error = error.args[0].response #If this errors then ignore it. Not sure why it says this is an error in the ide. It does not error when you run it.

        # results = {}
        # results["message"] = response_error.json()['error']['message']

        # response_code = response_error.status_code

        # if results['message'] == "INVALID_PASSWORD":
        #     response_code = 401

        # return results, response_code

def authSighUp(email: str, password: str) -> Tuple[Dict, int]:
    """ Signs up the user using the email and password
    
    Returns the response and the status
    """
    try:
        user = pyre_auth.create_user_with_email_and_password(email, password)

        return {"token": user["idToken"], "uid": user['localId']}, 200
    except:
        return { "message": "Login Error" }, 400
        

        # if isinstance(err.args[0], dict):
        #     response_error = err.args[0]

        #     results = {}
        #     results["message"] = response_error['message']

        #     response_code = response_error['status_code']
        # else:
        #     response_error = err.args[0].response #If this errors then ignore it. Not sure why it says this is an error in the ide. It does not error when you run it.

        #     results = {}
        #     results["message"] = response_error.json()['error']['message']

        #     response_code = response_error.status_code

        # return results, response_code

def get_info_from_token(token: str) -> Dict:
    """ Takes a token and returns information about the user
    """
    token_info = pyre_auth.get_account_info(token)['users'][0]
    token_info['user_id'] = token_info['localId']
    return token_info
    