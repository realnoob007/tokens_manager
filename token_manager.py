import datetime
import sys
import os

TOKEN_FILE = 'usertokens.txt'

def add_token(token, token_file=TOKEN_FILE):  # Default to TOKEN_FILE if not provided
    tokens = read_tokens(token_file)
    tokens[token] = datetime.date.today().isoformat()
    write_tokens(tokens, token_file)

def read_tokens(token_file):
    if not os.path.exists(token_file):
        return {}
    with open(token_file, 'r') as file:
        return dict(line.strip().split(',') for line in file if line)

def write_tokens(tokens, token_file):
    with open(token_file, 'w') as file:
        for token, date in tokens.items():
            file.write(f'{token},{date}\n')

def cleanup_tokens(token_file):
    tokens = read_tokens(token_file)
    today = datetime.date.today()
    tokens = {token: date for token, date in tokens.items() if (today - datetime.date.fromisoformat(date)).days <= 30}
    write_tokens(tokens, token_file)

def get_tokens_details(token_file):
    tokens = read_tokens(token_file)
    today = datetime.date.today()
    return {token: {"created_at": date, "expires_in": 30 - (today - datetime.date.fromisoformat(date)).days} for token, date in tokens.items()}

def delete_token(token, token_file=TOKEN_FILE):  # Default to TOKEN_FILE if not provided
    tokens = read_tokens(token_file)
    if token in tokens:
        del tokens[token]
        write_tokens(tokens, token_file)