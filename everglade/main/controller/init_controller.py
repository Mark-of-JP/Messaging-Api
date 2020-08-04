from everglade.main.controller.login import initialize_login
from everglade.main.controller.database_test import initialize_database_test
from everglade.main.controller.user_controller import initialize_user_routes
from everglade.main.controller.chat_controller import initialize_chat_routes

#List of initialization functions from controllers
controllers = [
    initialize_login,
    initialize_user_routes,
    initialize_chat_routes,

    
    initialize_database_test
]

def initialize_all_controllers(api):
    """Adds all routes to the api
    """
    for i in range(len(controllers)):
        controllers[i](api)