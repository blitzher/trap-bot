import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()

def user_to_dict(user):
    return {'user_id':user[0], 'score':user[1]}

def create_user_table():
    try: 
        c.execute(""" CREATE TABLE users (
                user_id text,
                score integer
                )""")
    except Exception:
        pass

def add_user(user_id):
    if query(user_id):
        print("User already exists!")
        return

    with conn:
        print("Added user: {} to the database.".format(user_id))
        user_id = user_id.replace('#', '')
        c.execute(" INSERT INTO users VALUES (:id, 0)", {'id':user_id})

def update_score(user_id, current, change):
    score = query(user_id)['score']
    if change == 0: 
        return

    with conn:
        c.execute("""
            UPDATE users SET score = :scr WHERE user_id = :id """,
            {'scr':score + change, 'id':user_id} )

def query(user_id):
    user_id = user_id.replace('#', '')
    c.execute(" SELECT * FROM users WHERE user_id=:id", {'id':user_id})
    fetch = c.fetchone()
    if fetch:
        return user_to_dict(fetch)
    else: 
        return False


def query_all(user_id):
    user_id = user_id.replace('#', '')
    c.execute(" SELECT * FROM users WHERE user_id=:id", {'id':user_id})
    return user_to_dict(c.fetchall())

def load_all():
    ret_list = []
    for user in c.execute('SELECT * FROM users'):
        ret_list.append(user_to_dict(user))
    return ret_list

try: 
    create_user_table()
except: 
    pass
