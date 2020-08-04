import os
import json

if os.environ.get('IS_HEROKU', False):
    from everglade.main.constants.cred.config import config
    
    with open('everglade/main/constants/cred/credentials.json', 'w') as outfile:
        cred = {
        "type": os.environ.get('CREDENTIALS_TYPE', None),
        "project_id": os.environ.get('CREDENTIALS_PROJECT_ID', None),
        "private_key_id": os.environ.get('CREDENTIALS_PRIVATE_KEY_ID', None),
        "private_key": os.environ.get('CREDENTIALS_PRIVATE_KEY', None),
        "client_email": os.environ.get('CREDENTIALS_CLIENT_EMAIL', None),
        "client_id": os.environ.get('CREDENTIALS_CLIENT_ID', None),
        "auth_uri": os.environ.get('CREDENTIALS_AUTH_URI', None),
        "token_uri": os.environ.get('CREDENTIALS_TOKEN_URI', None),
        "auth_provider_x509_cert_url": os.environ.get('CREDENTIALS_AUTH_PROVIDER_X509_CERT_URL', None),
        "client_x509_cert_url": os.environ.get('CREDENTIALS_CLIENT_X509_CERT_URL', None)}

        print('POOGERINO')
        print(cred)
        json.dump(cred, outfile)

    credentials_path = 'everglade/main/constants/cred/credentials.json'
else:
    from everglade.main.constants.ignore.config import config
    credentials_path = 'everglade/main/constants/ignore/credentials.json'