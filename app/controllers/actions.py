# Author: Alex Ksikes 

import web
import config

from app.helpers import paging
from app.helpers import session

from app.models import applicants
from app.models import comments
from app.models import votes

from config import view

class admit:
    @session.login_required
    def POST(self):
        i = web.input(context='', id=[])
        
        if i.id:
            applicants.admit(i.id, session.get_user_id())
        raise web.seeother(web.ctx.environ['HTTP_REFERER'])
        
class reject:
    @session.login_required
    def POST(self):
        i = web.input(context='', id=[])
        
        if i.id:
            applicants.reject(i.id, session.get_user_id())
        raise web.seeother(web.ctx.environ['HTTP_REFERER'])

class undecide:
    @session.login_required
    def POST(self):
        i = web.input(context='', id=[])
        
        if i.id:
            applicants.undecide(i.id, session.get_user_id())
        raise web.seeother(web.ctx.environ['HTTP_REFERER'])

class rate:
    @session.login_required
    def POST(self):
        i = web.input(context='', id=[], score=[])
        score = web.intget(i.score[0] or i.score[1], '')
        
        if i.id and score:
#            applicants.rate(i.id, score, session.get_user_id())
            votes.add(i.id, score, session.get_user_id())
        raise web.seeother(web.ctx.environ['HTTP_REFERER'])

class comment:
    @session.login_required
    def POST(self, id):
        i = web.input(comment='')
        
        if i.id and i.comment:
            comments.add_comment(session.get_user_id(), id, i.comment)
        
        raise web.seeother(web.ctx.environ['HTTP_REFERER'])

class delete_comment:
    @session.login_required
    def GET(self, comment_id):
        comments.delete_comment(session.get_user_id(), comment_id)
        
        raise web.seeother(web.ctx.environ['HTTP_REFERER'])

class grant:
    @session.login_required
    def POST(self, id):
        i = web.input(amount='')

        if i.id and i.amount:
            applicants.grant(session.get_user_id(), id, i.amount)
        
        raise web.seeother(web.ctx.environ['HTTP_REFERER'])