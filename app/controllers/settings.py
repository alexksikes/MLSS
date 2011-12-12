# Author: Alex Ksikes 

import web
import config

from web import form

from app.models import applicants
from app.models import users

from app.helpers import session
from config import view
    
password_form = form.Form(
    form.Password('password', 
        form.notnull,
        form.Validator('Your password must at least 5 characters long.', 
        lambda x: users.is_valid_password(x)),
        description='Your new password:'),
    form.Button('submit', type='submit', value='Change password')
)

nickname_form = form.Form(
    form.Textbox('nickname', 
        form.notnull,
        description='Your new nickname:'),
    form.Button('submit', type='submit', value='Change your nickname')
)

vemail = form.regexp(r'.+@.+', 'Please enter a valid email address')
email_form = form.Form(
    form.Textbox('email', 
        form.notnull, vemail,
        form.Validator('This email address is already taken.', 
        lambda x: users.is_email_available(x)),
        description='Your new email:'),
    form.Button('submit', type='submit', value='Change your email')
)

def render_settings(nickname_form=nickname_form(), email_form=email_form(), password_form=password_form(), on_success_message=''):
    counts = applicants.get_counts()
    user = session.get_session()
    
    return view.base(
        view.settings(user, nickname_form, email_form, password_form, on_success_message)
    )
	
class index:
    @session.login_required
    def GET(self):
        return render_settings()

class change_nickname:
    @session.login_required
    def POST(self):
        f = self.form()
        if not f.validates(web.input(_unicode=False)):
            return render_settings(nickname_form=f)
        else:
            users.update(session.get_user_id(), nickname=f.d.nickname)
            session.reset()
            raise web.seeother('/settings')

    def form(self):
        return nickname_form()

class change_email:
    @session.login_required
    def POST(self):
        f = self.form()
        if not f.validates(web.input(_unicode=False)):
            return render_settings(email_form=f)
        else:
            users.update(session.get_user_id(), email=f.d.email)
            session.reset()
            raise web.seeother('/settings')

    def form(self):
        return email_form()

class change_password:
    @session.login_required
    def POST(self):
        f = self.form()
        if not f.validates(web.input(_unicode=False)):
            return render_settings(password_form=f)
        else:
            users.update(session.get_user_id(), password=f.d.password)
            session.reset()
            return render_settings(on_success_message='Your password has been successfuly changed.')

    def form(self):
        return password_form()

