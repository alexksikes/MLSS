# Author: Alex Ksikes 

import web
from config import db

def create_account(email, password, nickname):
    db.insert('users', email=email, password=password, nickname=nickname)
    
def get_user_by_email(email):
    return web.listget(
        db.select('users', vars=dict(email=email), 
            where='email = $email'), 0, {})

def is_email_available(email):
    return not db.select(
        'users', 
        vars = dict(email=email),
        what = 'count(id) as c', 
        where = 'email = $email')[0].c

def is_valid_password(password):
    return len(password) >= 5

def is_correct_password(email, password):
    user = get_user_by_email(email)
    return user.get('password', False) == password

def update(id, **kw):
    db.update('users', vars=dict(id=id), where='id = $id', **kw)

def get_user_by_id(id):
    return web.listget(
        db.select('users', vars=dict(id=id), 
            where='id = $id'), 0, {})
