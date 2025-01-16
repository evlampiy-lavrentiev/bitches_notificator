import json
import logging
import dotenv
import os

logging = logging.getLogger('bitches')

cred = None

def get_cred(credentials_path = 'config.json'):
    global cred
    if cred is None:
        cred = json.load(open(credentials_path, 'r'))
    return cred

def get_variable(variable_name):
    credentials = get_cred()

    env_variable_name = variable_name.upper()
    dangerous_variables = ['api_id', 'api_hash', 'bot_token']
    if variable_name in credentials and credentials[variable_name] != "":
        if variable_name in dangerous_variables:
            logging.warning(f"{variable_name=} is set directly in session_info. "
                            f"It's recommended to define '{env_variable_name}' in the .env file or bash instead.")
        return credentials[variable_name]

    dotenv.load_dotenv()
    res = os.getenv(env_variable_name)
    if res is None:
        msg = f"{env_variable_name} must be set in the .env file."
        logging.error(msg)
        raise ValueError(msg)
    return res