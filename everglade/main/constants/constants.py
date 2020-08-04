import os

if os.environ.get('IS_HEROKU', False):
    from everglade.main.constants.cred.config import config
else:
    from everglade.main.constants.ignore.config import config