# Author: Alex Ksikes 

import web
import config

from app.models import submissions

from config import view
from web import form

vemail = form.regexp(r'.+@.+', 'Please enter a valid email address')
vurl = form.regexp('(^\s*$)|(^http://.*$)', 
    'Please provide a valid website url (eg, http://www.example.com).')

application_form = form.Form(
    form.Textbox('first_name', 
        form.notnull,
        description='First Name *'),
    form.Textbox('last_name', 
        form.notnull,
        description='Last Name *'),
    form.Radio('gender', 
        ('Male', 'Female'),
        form.notnull,
        description='Gender *'),
    form.Textbox('nationality', 
        form.notnull,
        description='Nationality *'),
    form.Textbox('country', 
        form.notnull,
        description='Country of Current Affiliation *'),
    
    form.Textbox('email', 
        form.notnull, vemail,
        form.Validator('This email address is already taken (Have you already submitted an application?)', 
        lambda x: submissions.is_email_available(x)),
        description='Your Email *'),
    form.Textbox('email_again', 
        form.notnull, vemail,
        description='Your Email Again *'),
    
    form.Textbox('affiliation', 
        form.notnull,
        description='Affiliation *',
        pre='<label class="help">Your university or the company you work for.</label>'),
    form.Textbox('department', 
        form.notnull,
        description='Affiliation (Department) *'),
    form.Textbox('interests', 
        form.notnull,
        description='Interests *',
        pre='<label class="help">Please provide 3-10 keywords/keyphrases, separated by commas.</label>'),
    form.Textbox('website', 
        vurl,
        description='Personal Website (optional)',
        pre='<label class="help">If you have a personal website, please provide its url with http.</label>'),
     
    form.Dropdown('degree', 
        ('', 'Highschool', 'Bachelors', 'Masters', 'PhD', 'Other'),
        form.notnull,
        description='Highest Degree Attained *'),
    form.Dropdown('occupation', 
        ('', 'Undergraduate student', 'PhD student', 'Postdoc', 'Faculty', 'Industry Researcher', 'Other'),
        form.notnull,
        description='Current Occupation *'),
    form.File('resume', 
        form.notnull,
        description='Upload your resume in pdf. *'),
    
    form.Radio('pascal_member', 
        ('Yes', 'No'),
        description='Pascal Member (optional)',
        pre='<label class="help">Are you a member of the PASCAL European network?</label>'),
    form.Textbox('poster_title', 
        description='Poster Title (optional)',
        pre='<label class="help">We will probably have a poster session for students to present their work. Tentative title of your poster if you were able to present at the MLSS.</label>'),
    form.Textarea('abstract', 
        description='Abstract (optional)',
    pre='<label class="help">If you plan to present a poster, please include in this box the <strong>abstract of your poster</strong>.</label>'),
    form.Textarea('cover_letter', 
        description='Comments (optional)',
    pre='<label class="help">Additional comments in support of your application (max 200 words) -- You can use this box to highlight reasons why the MLSS is appropriate for you and any specific achievements you feel are relevant.</label>'),
    
    form.Textbox('referee_name', 
        form.notnull,
        description='Referee Name *',
        pre='<label class="help">Please ensure the referee is willing to submit a letter by <strong>June 11</strong>.</label>'),
    form.Textbox('referee_email', 
        form.notnull, vemail,
        description='Referee Email *'),
    form.Textbox('referee_email_again', 
        form.notnull, vemail, 
        description='Referee Email Again *'),
    form.Textbox('referee_affiliation', 
        form.notnull,
        description='Referee Affiliation *'),
    
    form.Checkbox('travel_support', 
        description='Travel Support (optional)',
        post='<span>I wish to apply for financial support.</span>'),
    
    form.Textbox('travel_support_budget',
        form.Validator('Please enter an integer for your financial support budget estimate.', 
        lambda x: not x or isinstance(int(x), int)),
        description='Enter budget estimate (in dollars)'),
    
    form.Button('submit', type='submit', value='Apply'),
    validators = [
        form.Validator('If you are applying for financial support, make sure you complete all the fields.', 
            lambda i: check_travel_support(i)),
        form.Validator('Your email addresses did not match!', 
            lambda i: i.email == i.email_again),
        form.Validator('Referee email addresses did not match!', 
            lambda i: i.referee_email == i.referee_email_again),
    ]
)

# This form is only used for applicant who are affiliated to the university.
# For those applicants the application is simple (no letter of reference and financial support).
application_form_simple = form.Form(
    form.Radio('affiliated', 
        ('University of Cambridge', 'Microsoft Research Cambridge', 'Other (explain below)'),
        form.notnull,
        description='Affiliation with Cambridge *'),
    
    form.Textbox('first_name', 
        form.notnull,
        description='First Name *'),
    form.Textbox('last_name', 
        form.notnull,
        description='Last Name *'),
    form.Radio('gender', 
        ('Male', 'Female'),
        form.notnull,
        description='Gender *'),
    form.Textbox('nationality', 
        form.notnull,
        description='Nationality *'),
    form.Textbox('country', 
        form.notnull,
        description='Country of Current Affiliation *'),
    
    form.Textbox('email', 
        form.notnull, vemail,
        form.Validator('This email address is already taken (Have you already submitted an application?)', 
        lambda x: submissions.is_email_available(x)),
        description='Your Email *'),
    form.Textbox('email_again', 
        form.notnull, vemail,
        description='Your Email Again *'),
    
    form.Textbox('affiliation', 
        form.notnull,
        description='Affiliation *',
        pre='<label class="help">Your university or the company you work for.</label>'),
    form.Textbox('department', 
        form.notnull,
        description='Affiliation (Department) *'),
    form.Textbox('interests', 
        form.notnull,
        description='Interests *',
        pre='<label class="help">Please provide 3-10 keywords/keyphrases, separated by commas.</label>'),
    form.Textbox('website', 
        vurl,
        description='Personal Website (optional)',
        pre='<label class="help">If you have a personal website, please provide its url with http.</label>'),
     
    form.Dropdown('degree', 
        ('', 'Highschool', 'Bachelors', 'Masters', 'PhD', 'Other'),
        form.notnull,
        description='Highest Degree Attained *'),
    form.Dropdown('occupation', 
        ('', 'Undergraduate student', 'PhD student', 'Postdoc', 'Faculty', 'Industry Researcher', 'Other'),
        form.notnull,
        description='Current Occupation *'),
    form.File('resume', 
        form.notnull,
        description='Upload your resume in pdf. *'),
        
    form.Radio('pascal_member', 
        ('Yes', 'No'),
        description='Pascal Member (optional)',
        pre='<label class="help">Are you a member of the PASCAL European network?</label>'),
    form.Textbox('poster_title', 
        description='Poster Title (optional)',
        pre='<label class="help">We will probably have a poster session for students to present their work. Tentative title of your poster if you were able to present at the MLSS.</label>'),
    form.Textarea('abstract', 
        description='Abstract (optional)',
    pre='<label class="help">If you plan to present a poster, please include in this box the <strong>abstract of your poster</strong>.</label>'),
    form.Textarea('cover_letter', 
        description='Comments (optional)',
    pre='<label class="help">Additional comments in support of your application (max 200 words) -- You can use this box to highlight reasons why the MLSS is appropriate for you and any specific achievements you feel are relevant.</label>'),
        
    form.Button('submit', type='submit', value='Apply'),
    validators = [
        form.Validator('Your email addresses did not match!', 
            lambda i: i.email == i.email_again),
    ]
)
   
class apply:
    def GET(self):
        success = web.input(success='').success
        return view.application_form(self.form(), success)
        
    def POST(self):
        f = self.form()
        
        # due a bug in webpy we have to do web.input(_unicode=False) 
        # when having a File input element in a form
        if not f.validates(web.input(_unicode=False)):
            return view.application_form(f)
        else:
            success = handle_post(f)
            raise web.seeother('/submit_application?success=%s' % success)
    
    def form(self):
        return application_form()

# This is for applicants who are affiliated within cambridge.
# They do not need a reference and financial support (have their own housing, etc...)
class apply_simple:
    def GET(self):
        success = web.input(success='').success
        return view.application_form_simple(self.form(), success)
    
    def POST(self):
        f = self.form()
        
        # due a bug in webpy we have to do web.input(_unicode=False) 
        # when having a File input element in a form
        if not f.validates(web.input(_unicode=False)):
            return view.application_form_simple(f)
        else:
            success = handle_post(f, simple=True)
            raise web.seeother('/affiliated/submit_application?success=%s' % success)
    
    def form(self):
        return application_form_simple()

def handle_post(f, simple=False):
    resume = web.input(resume={}).resume
    success = True
    try:
        submissions.submit_application(resume, f.d, simple)
    except:
        raise
        success = False
    return success
    
# In a browser, if a checkbox is not checked, it isn't sent in the request
# (see http://www.w3.org/TR/html401/interact/forms.html#h-17.2.1) 
def check_travel_support(i):
    # note that i.travel_support leads to an error! 
    i.travel_support = i.get('travel_support', False)
    return (not i.travel_support and not i.travel_support_budget) or (i.travel_support and i.travel_support_budget)
