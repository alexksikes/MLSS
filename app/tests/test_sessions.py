# Author: Alex Ksikes 

import web

class test_session:
   def GET(self):
       session = web.config._session
       print 'session', session
       session.count += 1
       session.new = 'hello'
       session.kill()
       return ('it\'s cool it works yeah yeah ...' +
        'Hello, %s! %s' % (session.count, session.new))
