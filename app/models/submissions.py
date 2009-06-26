# Author: Alex Ksikes

import web
from config import db

from app.helpers import utils
from app.helpers import email_templates

from cStringIO import StringIO
from datetime import date

resume_dir = 'public/resumes/'

def submit_application(resume, d, simple=False):
    # clean up some fields
    clean_up_data(d)
    # handle the file upload
    d.resume_fn = save_resume(resume, d.first_name, d.last_name)
    # in simple mode, no reference is required
    if simple:
        # save the data in the db
        add_applicant(d)
        # email user and referee
        email_templates.to_applicant_simple(d)
    else:
        # make secret md5
        d.secret_md5 = utils.make_unique_md5()
        # save the data in the db
        add_applicant(d)
        # email user and referee
        email_templates.to_applicant(d)
        email_templates.to_referee(d)

def clean_up_data(d):
    utils.dict_remove(d, 'resume', 'submit', 'referee_email_again', 'email_again')
    d.gender = d.gender.lower() 
    d.pascal_member = d.pascal_member == 'Yes';
    d.travel_support = d.get('travel_support', None) and True or None;
    d.affiliated = d.get('affiliated', False) != False;

def is_email_available(email):
    return not db.select(
        'applicants', 
        vars = dict(email=email),
        what = 'count(id) as c', 
        where = 'email = $email')[0].c

def save_resume(resume, first_name, last_name):
    ext = resume.filename.split('.')[-1]
    fname = '%s.%s.%s.resume.%s' % (first_name, last_name, date.today(), ext)
    fname = fname.replace(' ', '-')
    open(resume_dir + fname, 'wb').write(resume.value)
    return fname

def add_applicant(d):
    db.insert('applicants', **d)

def submit_reference(applicant, d):
    # clean up some fields
    utils.dict_remove(d, 'submit')
    # add the provided reference
    add_reference(applicant.secret_md5, d)
    # notify user and referee by email
    email_templates.notify_applicant(applicant)
    email_templates.notify_referee(applicant)

def get_by_secret_md5(secret_md5):
    return web.listget(db.select(
        'applicants', 
        vars = dict(md5=secret_md5),
        where = 'secret_md5 = $md5'), 0, False)

# TODO: set update_ts as well
def add_reference(secret_md5, d):
    db.update(
        'applicants', 
        vars = dict(md5=secret_md5),
        where = 'secret_md5=$md5', 
        **d)
