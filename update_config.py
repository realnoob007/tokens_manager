import yaml

def read_tokens(file_path):
    tokens = []
    with open(file_path, 'r') as file:
        for line in file:
            token, _ = line.strip().split(',')
            # Directly include the token without additional quotes
            tokens.append(token)
    return tokens

def update_config_file(config_file_path, token_file_path):
    # Read the new tokens from usertokens.txt
    new_tokens = read_tokens(token_file_path)

    # Load the config.yaml file
    with open(config_file_path, 'r') as file:
        config_data = yaml.safe_load(file)

    # Replace the USERTOKENS section with new tokens
    config_data['USERTOKENS'] = new_tokens

    # Save the modified config.yaml file
    with open(config_file_path, 'w') as file:
        # Use a custom dumper to prevent adding additional quotes
        yaml.dump(config_data, file, default_flow_style=False, Dumper=yaml.Dumper)

# File paths
config_file_path = 'manager/cock1/config.yaml'
token_file_path = 'manager/usertokens.txt'

# Updating the config file
update_config_file(config_file_path, token_file_path)

