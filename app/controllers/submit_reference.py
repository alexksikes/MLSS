# Author: Alex Ksikes 

import web
import config

from app.models import submissions
from app.models import applicants

from config import view
from web import form

class refer:
    def GET(self, secret_md5):
        applicant = applicants.get_by_secret_md5(secret_md5)
        
        if not applicant and secret_md5 == '0' * 32:
            applicant = applicants.get_dummy_record()
        
        return view.reference_form(self.form(), applicant, web.input(success='').success)
    
    def POST(self, secret_md5):
        applicant = applicants.get_by_secret_md5(secret_md5)
        
        f = self.form()
        if not f.validates(web.input(_unicode=False)):
            return view.reference_form(f, applicant)
        else:
            success = True
            try:
                submissions.submit_reference(applicant, f.d)
            except:
                raise
                success = False
            raise web.seeother('/submit_reference/%s?success=%s' % (secret_md5, success))
    
    def form(self):
        return form.Form(
            form.Dropdown('referee_rating', 
                 ('',
                 ('1', '* - Not recommended'), 
                 ('2', '** - Has reserve'), 
                 ('3', '*** - Average'),
                 ('4', '**** - Strong applicant'),
                 ('5', '***** - Outstanding')),
                form.notnull,
                description='How would you score this applicant?'),
            form.Textarea('reference', 
                form.notnull,
                description='Please describe in less than 500 words why you recommmend this applicant.'),
            form.Button('submit', type='submit', value='Submit reference'),
        )
