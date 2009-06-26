# Author: Alex Ksikes

# This is a sample config file. Complete it and rename the file config.py.

import web, os

from app.helpers import misc
from app.helpers import utils

# connect to database
db = web.database(dbn='mysql', db='mlss', user='your username', passwd='your password')

# in development debug error messages and reloader
web.config.debug = True

# in develpment template caching is set to false
cache = False

# global used template functions
globals = utils.get_all_functions(misc)

# the domain where to get the forms from
site_domain = 'your website domain'

# email settings
mail_sender = 'MLSS 2009 <noreply@example.com>'

# set global base template
view = web.template.render('app/views', cache=cache,  globals=globals)

# used as a salt
encryption_key = 'a random string'

# in production the internal errors are emailed to us
web.config.email_errors = ''
