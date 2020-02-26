import database
import json


all_users = database.load_all()

sorted_users = sorted(all_users, key=lambda x: x['user_id'].lower())


with open('user.json', 'w') as f:
    json.dump({'users': sorted_users}, f, indent = 2)
