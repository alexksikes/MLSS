# Author: Alex Ksikes 

# TODO:
# - see for a better paging module
# - no need to have two separate login_required_for_reviews and login_required

import web
import config

from app.helpers import paging
from app.helpers import session

from app.models import applicants
from app.models import comments
from app.models import votes

from config import view

results_per_page = 50
default_order = 'id'

class list:
    @session.login_required_for_reviews
    def GET(self, context):
        i = web.input(start=0, order=default_order, desc='desc', query='')
        start = int(i.start)
        context = context or 'all'
        user_id = session.is_logged() and session.get_user_id()
        
        results, num_results = applicants.query(query=i.query, context=context, 
            offset=start, limit=results_per_page, order=i.order + ' ' + i.desc, 
            user_id=user_id)
        
        pager = web.storage(paging.get_paging(start, num_results, 
            results_per_page=results_per_page, window_size=1))
        
        counts = applicants.get_counts()
        
        user = session.get_session()
        
        stats = applicants.get_stats()
        
        return view.layout(
            view.applicants(results, context, pager, i), 
            user, context, counts, i.query, stats)

class show:
    @session.login_required_for_reviews
    def GET(self, id):
        i = web.input(context='all', start=0, order=default_order, desc='desc', query='')
        start = int(i.start)
        user_id = session.is_logged() and session.get_user_id()
        
        results, num_results = applicants.query(query=i.query, context=i.context, 
            offset=start and start - 1, limit=results_per_page+2, order=i.order + ' ' + i.desc, 
            user_id=user_id)
        
        pager = web.storage(paging.get_paging_results(start, num_results, 
            int(id), results, results_per_page))
        
        counts = applicants.get_counts()
        
        user = session.get_session()
        
        applicant = applicants.get_by_id(id)
        
        _comments = comments.get_comments(applicant.id)
        
        _votes = votes.get_votes(applicant.id)
        
        stats = applicants.get_stats()
        
        return view.layout(
            view.applicant(applicant, _comments, _votes, user, pager, i), 
            user, i.context, counts, i.query, stats)
