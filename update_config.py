import yaml
import os
import logging
from filelock import FileLock

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def update_token_in_all_configs(config_dir, token, action):
    config_dir=config_dir
    try:
        for dirpath, _, filenames in os.walk(config_dir):
            for filename in filenames:
                if filename.endswith('.yaml'):  # Assuming config files are YAML
                    config_file_path = os.path.join(dirpath, filename)
                    if action == 'add':
                        add_token_to_config(config_file_path, token)
                    elif action == 'delete':
                        delete_token_from_config(config_file_path, token)
    except Exception as e:
        logging.error(f"Error updating tokens in configs: {e}")
        
def read_config(config_file_path):
    with FileLock(config_file_path + ".lock"):
        with open(config_file_path, 'r') as file:
            return yaml.safe_load(file)

def write_config(config_file_path, config_data):
    with FileLock(config_file_path + ".lock"):
        with open(config_file_path, 'w') as file:
            yaml.dump(config_data, file, default_flow_style=False, Dumper=yaml.Dumper)

def add_token_to_config(config_file_path, token):
    logging.debug(f"Adding token {token} to {config_file_path}")
    try:
        config_data = read_config(config_file_path)
        if 'USERTOKENS' not in config_data:
            config_data['USERTOKENS'] = []

        if token not in config_data['USERTOKENS']:
            config_data['USERTOKENS'].append(token)
            write_config(config_file_path, config_data)
            logging.info(f"Token {token} added to {config_file_path}")
        else:
            logging.info(f"Token {token} already exists in {config_file_path}")
    except Exception as e:
        logging.error(f"Error adding token to config: {e}")

def delete_token_from_config(config_file_path, token):
    logging.debug(f"Deleting token {token} from {config_file_path}")
    try:
        config_data = read_config(config_file_path)
        if 'USERTOKENS' in config_data and token in config_data['USERTOKENS']:
            config_data['USERTOKENS'].remove(token)
            write_config(config_file_path, config_data)
            logging.info(f"Token {token} deleted from {config_file_path}")
        else:
            logging.info(f"Token {token} not found in {config_file_path}")
    except Exception as e:
        logging.error(f"Error deleting token from config: {e}")
