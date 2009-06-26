# Author: Alex Ksikes

# TODO:
# - this should be moved to a DB.

import web
import config

_from = config.mail_sender
bcc = 'alex.ksikes@gmail.com'

msg_to_applicant = \
'''$def with (applicant)
Dear $applicant.first_name $applicant.last_name,

Your application for the Machine Learning Summer School in 
Cambridge has been received. We will contact $applicant.referee_name 
and ask for a letter of reference. Both you and the referee 
will receive notification once the letter has been received. 
Decisions on applications will be emailed by the end of June.

Thank you very much for applying.

With regards 

The Organisers
Machine Learning Summer School 2009, University of Cambridge
'''

msg_to_applicant_simple = \
'''$def with (applicant)
Dear $applicant.first_name $applicant.last_name,

Your application for the Machine Learning Summer School in 
Cambridge has been received. Decisions on applications will be 
emailed by the end of June.

Thank you very much for applying.

With regards 

The Organisers
Machine Learning Summer School 2009, University of Cambridge
'''

msg_to_referee = \
'''$def with (applicant)
Dear $applicant.referee_name,

$applicant.first_name $applicant.last_name has applied for the Machine Learning Summer School 
2009 in Cambridge and named you as referee.

We expect to receive more applications for the summer school than 
there are places available, and will select participants based on 
their academic background. We would ask you to submit a letter of 
reference that helps us evaluate the applicant's qualification. 
Your letter should address the applicant's background and potential 
in Machine Learning, academic standing compared to other students, 
and how the student would benefit from attending MLSS 2009. 

If the applicant wishes to apply for financial support (we will be 
able to provide support to a limited number of participants), 
please include a paragraph explaining why such support is required. 
Otherwise, we will not consider the applicant for financial support.

Your letter can be entered as plain text under the following URL:

http://%s/submit_reference/$applicant.secret_md5

For more information about the summer school, please refer to

http://mlg.eng.cam.ac.uk/mlss09/

Thank you very much.

With regards

The Organisers
Machine Learning Summer School 2009, University of Cambridge
''' % config.site_domain

msg_notify_applicant = \
'''$def with (applicant)
Dear $applicant.first_name $applicant.last_name,

This is to inform you that your letter of reference for the
Machine Learning Summer School 2009 has been received. You should
receive a decision on your application by the end of June, 2009.

With regards

The Organisers
Machine Learning Summer School 2009, University of Cambridge
'''

msg_notify_referee = \
'''$def with (applicant)
Dear $applicant.referee_name

Your letter of reference for $applicant.first_name, $applicant.last_name has been received.
Thank you very much for your assistance.

With regards

The Organisers
Machine Learning Summer School 2009, University of Cambridge
'''

msg_resend_password = \
'''$def with (user)
Hello $user.nickname, 

Here are the login information you have requested:

login: $user.email
password: $user.password

Thank you,

The Machine Learning Summer School admin at Cambridge.
'''

def to_applicant(applicant):
    subject = 'MLSS 2009: Thank You for Your Application'
    msg = web.template.Template(msg_to_applicant)(applicant)
    web.sendmail(_from, applicant.email, subject, msg, bcc=bcc)

def to_applicant_simple(applicant):
    subject = 'MLSS 2009: Thank You for Your Application'
    msg = web.template.Template(msg_to_applicant_simple)(applicant)
    web.sendmail(_from, applicant.email, subject, msg, bcc=bcc)

def to_referee(applicant):
    subject = 'Request for Reference Letter for MLSS 2009 - Deadline: June 11'
    msg = web.template.Template(msg_to_referee)(applicant)
    web.sendmail(_from, applicant.referee_email, subject, msg, bcc=bcc)
    
def notify_applicant(applicant):
    subject = 'MLSS 2009: Reference Letter'
    msg = web.template.Template(msg_notify_applicant)(applicant)
    web.sendmail(_from, applicant.email, subject, msg, bcc=bcc)

def notify_referee(applicant):
    subject = 'MLSS 2009: Reference Letter Received'
    msg = web.template.Template(msg_notify_referee)(applicant)
    web.sendmail(_from, applicant.referee_email, subject, msg, bcc=bcc)

def resend_password(user):
    subject = 'MLSS - Password request'
    msg = web.template.Template(msg_resend_password)(user)
    web.sendmail(_from, user.email, subject, msg, bcc=bcc)
