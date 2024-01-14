import yaml
import os

def read_tokens(file_path):
    tokens = []
    with open(file_path, 'r') as file:
        for line in file:
            token, _ = line.strip().split(',')
            tokens.append(token)
    return tokens

def update_config_file(config_file_path, token_file_path):
    new_tokens = read_tokens(token_file_path)
    with open(config_file_path, 'r') as file:
        config_data = yaml.safe_load(file)
    config_data['USERTOKENS'] = new_tokens
    with open(config_file_path, 'w') as file:
        yaml.dump(config_data, file, default_flow_style=False, Dumper=yaml.Dumper)

def update_all_configs(root_directory, token_file_path):
    for dirpath, dirnames, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename == 'config.yaml':
                config_file_path = os.path.join(dirpath, filename)
                print(f"Updating: {config_file_path}")  # Print the path of the file being updated
                update_config_file(config_file_path, token_file_path)

# Root directory to search for config.yaml files
root_directory = 'path/to/your/directory'  # Replace with the path to your root directory
token_file_path = 'path/to/manager/usertokens.txt'  # Replace with the path to your usertokens.txt

# Update all config files
update_all_configs(root_directory, token_file_path)
