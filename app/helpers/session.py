# Author: Alex Ksikes

# TODO:
# - webpy session module is ineficient and makes 5 db calls per urls!
# - because sessions are attached to an app, every user has sessions whether they atually need it or not.
# - login required decorator should save intended user action before asking to login.

import web
from config import db

from app.models import users
from app.models import applicants

def add_sessions_to_app(app):
    if web.config.get('_session') is None:
        store = web.session.DBStore(db, 'sessions')
        session = web.session.Session(app, store, 
            initializer={'is_logged' : False})
        web.config._session = session
    else:
        session = web.config._session

def get_session():
    return web.config._session

def is_logged():
    return get_session().is_logged

def login(email):
    s = get_session()
    for k, v in users.get_user_by_email(email).items():
        s[k] = v
    s.is_logged = True
    
def logout():
    get_session().kill()
    
def reset():
    user = users.get_user_by_id(get_user_id())
    login(user.email)
    
def get_user_id():
    return get_session().id    

def get_last_visited_url():
    redirect_url = web.cookies(redirect_url='/').redirect_url
    web.setcookie('redirect_url', '', expires='')
    return redirect_url

def set_last_visited_url():
    url = web.ctx.get('path')
    if url:
        web.setcookie('redirect_url', url)

def login_required(meth):
    def new(*args):
        if not is_logged():
            return web.redirect('/account')
        return meth(*args)
    return new

def login_required_for_reviews(meth):
    def new(*l):
        context = l[1] or web.input(context='').context
        if not is_logged() and context == 'reviewed':
            return web.redirect('/account')
        return meth(*l)
    return new
