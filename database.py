import os
import json

DATABASE_FILE = 'urls_db.json'

def load_urls():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_urls(urls):
    with open(DATABASE_FILE, 'w') as file:
        json.dump(urls, file)

def clear_urls():
    if os.path.exists(DATABASE_FILE):
        os.remove(DATABASE_FILE)
        print("URLs database cleared.")