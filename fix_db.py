import sqlite3
import datetime

# File and Database Path
TOKEN_FILE = 'manager/usertokens.txt'
DATABASE_FILE = 'tokens.db'

# Function to Initialize the Database
def init_db():
    with sqlite3.connect(DATABASE_FILE) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS tokens
                        (token TEXT PRIMARY KEY, expiration_date DATE)''')

# Function to Read Tokens from File and Extend Expiration Dates
def read_and_extend_tokens(token_file):
    with open(token_file, 'r') as file:
        for line in file:
            token, expiration_str = line.strip().split(',')
            expiration_date = datetime.datetime.strptime(expiration_str, '%Y-%m-%d').date()
            new_expiration_date = expiration_date + datetime.timedelta(days=30)
            yield (token, new_expiration_date.isoformat())

# Function to Insert Tokens into the Database
def insert_tokens_into_db(tokens):
    with sqlite3.connect(DATABASE_FILE) as conn:
        conn.executemany("INSERT OR REPLACE INTO tokens (token, expiration_date) VALUES (?, ?)", tokens)

# Main Function
def main():
    init_db()
    tokens = read_and_extend_tokens(TOKEN_FILE)
    insert_tokens_into_db(tokens)
    print("Tokens have been successfully migrated to the database.")

if __name__ == '__main__':
    main()
