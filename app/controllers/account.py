# Author: Alex Ksikes 

import web
from web import form

from app.models import users
from app.helpers import session
from app.helpers import email_templates

from config import view

vemail = form.regexp(r'.+@.+', 'Please enter a valid email address')
login_form = form.Form(
    form.Textbox('email', 
        form.notnull, vemail,
        description='Your email:'),
    form.Password('password', 
        form.notnull,
        description='Your password:'),
                
    form.Button('submit', type='submit', value='Login'),
    validators = [
        form.Validator('Incorrect email / password combination.', 
            lambda i: users.is_correct_password(i.email, i.password))
    ]
)

register_form = form.Form(
    form.Textbox('email', 
        form.notnull, vemail,
        form.Validator('This email address is already taken.', 
        lambda x: users.is_email_available(x)),
        description='Your email:'),
    form.Password('password', 
        form.notnull,
        form.Validator('Your password must at least 5 characters long.', 
        lambda x: users.is_valid_password(x)),
        description='Choose a password:'),
    form.Textbox('nickname', 
        form.notnull,
        description='Choose a nickname:'),
                
    form.Button('submit', type='submit', value='Register'),
)

forgot_password_form = form.Form(
    form.Textbox('email', 
        form.notnull, vemail,
        form.Validator('There is no record of this email in our database.', 
        lambda x: not users.is_email_available(x)),
        description='Your email:'),
                
    form.Button('submit', type='submit', value='Register'),
)

def render_account(show='all', 
    login_form=login_form(), register_form=register_form(), forgot_password_form=forgot_password_form(), 
    on_success_message=''):
    
    return view.base(
        view.account(show, login_form, register_form, forgot_password_form, on_success_message))

class index:
    def GET(self):
        return render_account(show='all')

class login:
    def GET(self):
        return render_account(show='login_only')
    
    def POST(self):
        f = self.form()
        if not f.validates(web.input(_unicode=False)):
            show = web.input(show='all').show
            return render_account(show, login_form=f)
        else:
            session.login(f.d.email)
            raise web.seeother('/')
            #raise web.seeother(session.get_last_visited_url())
    
    def form(self):
        return login_form()
    
class register:
    def GET(self):
        return render_account(show='register_only')
    
    def POST(self):
        f = self.form()
        if not f.validates(web.input(_unicode=False)):
            show = web.input(show='all').show
            return render_account(show, register_form=f)
        else:
            users.create_account(f.d.email, f.d.password, f.d.nickname)
            session.login(f.d.email)
            raise web.seeother('/')
    
    def form(self):
        return register_form()

class resend_password:
    def GET(self):
        return render_account(show='forgot_password_only')
    
    def POST(self):
        f = self.form()
        show = web.input(show='all').show
        if not f.validates(web.input(_unicode=False)):
            return render_account(show, forgot_password_form=f)
        else:
            user = users.get_user_by_email(f.d.email)
            email_templates.resend_password(user)
            return render_account(show, 
                on_success_message='Login information succesfully emailed.')
    
    def form(self):
        return forgot_password_form()

class logout:
    def GET(self):
        session.logout()
        raise web.seeother(web.ctx.environ['HTTP_REFERER'])
    
class help:
    def GET(self):
        return view.base(view.help())
