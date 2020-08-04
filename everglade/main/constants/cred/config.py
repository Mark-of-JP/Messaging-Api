import os

config = {
    "apiKey": os.environ.get("CONFIG_API_KEY", None),
    "authDomain": os.environ.get("CONFIG_AUTH_DOMAN", None),
    "databaseURL": os.environ.get("CONFIG_DATABASE_URL", None),
    "projectId": os.environ.get("CONFIG_PROJECT_ID", None),
    "storageBucket": os.environ.get("CONFIG_STORAGE_BUCKET", None),
    "messagingSenderId": os.environ.get("CONFIG_MESSENGER_SENDER_ID", None),
    "appId": os.environ.get("CONFIG_APP_ID", None),
    "measurementId": os.environ.get("CONFIG_MEASUREMENT_ID", None)
}