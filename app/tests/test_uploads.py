# Author: Alex Ksikes 

import web
import config

from config import view
from web import form


class upload:
    def GET(self):
        return r'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>Apply</title>
        <link href="mlss.css" rel="stylesheet" type="text/css" />
        </head>
        
        <body>
        
        <div class="submitted">
        </div>
        <form action="/apply" enctype="multipart/form-data" method="post" name='theform'> 
            <fieldset>
            <legend>Application to MLSS 2009: (All fields are required)</legend>
            <label for="resume_fn">Upload your resume in PDF</label><input type="file" name="resume_fn" id="resume_fn" />
            <label for="submit"></label><button name="submit" type="submit" id="submit">submit</button>
            </fieldset>
        </form>
        </body>
        </html>'''
        
    def POST(self):
        return 'OK'
    
class upload2:
    def GET(self):
        yield r'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            </head>
        <body>
        <form action="" enctype="multipart/form-data" method="post">'''
        yield self.form().render_css()
        yield '<form action="" enctype="multipart/form-data" method="post">'
        yield '</form></body></html>'
        
    def POST(self):
        f = self.form()
        f.validates(web.input(_unicode=False))
        yield f.d.resume_fn
        if not f.valid:
            yield 'Missing something'
        yield 'You will never see this text if you upload a file.'
    
    def form(self):
        return form.Form(
            form.File('resume_fn', 
                form.notnull,
                description='It will take forever if we validate the form'),
            form.Button('submit', type='submit', value='Apply'))