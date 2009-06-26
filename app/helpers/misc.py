# Author: Alex Ksikes

# TODO:
# - we should subclass form.Form instead.

import web, re, urlparse, datetime, urllib, utils, string

def format_date(d, f):
    return d.strftime(f)

def url_quote(url):
    return web.urlquote(url)

def html_quote(html):
    return web.htmlquote(url)

def url_encode(query, clean=True, doseq=True, **kw):
    query = web.dictadd(query, kw)
    if clean is True:
        for q, v in query.items():
            if not v:
                del query[q]
    return urllib.urlencode(query, doseq)

def cut_length(s, max=40, tooltip=False):
    s_cut = s[0:]
    if len(s) > max:
        s_cut = s[0:max] + '...'
    if tooltip:
        s_cut = '<span title="%s">%s</span>' % (s, s_cut)
    
    return s_cut

def get_nice_url(url):
    host, path = urlparse.urlparse(url)[1:3]
    if path == '/':
        path = ''
    return cut_length(host+path)

def capitalize_first(str):
    if not str:
        str = ''
    return ' '.join(map(string.capitalize, str.lower().split()))

def text2html(s):
    s = replace_breaks(s)
    s = replace_indents(s)
    return replace_links(s)
    
def replace_breaks(s):
    return re.sub('\n', '<br />', s)

def replace_indents(s):
    s = re.sub('\t', 4*' ', s)
    return re.sub('\s{2}', '&nbsp;'*2, s)

def replace_links(s):
    return re.sub('(http://[^\s]+)', r'<a rel="nofollow" href="\1">' + get_nice_url(r'\1') + '</a>', s, re.I)

# we may need to get months ago as well
def how_long(d):
    return web.datestr(d, datetime.datetime.now())

def split(pattern, str):
    return re.split(pattern, str)

def sub(pattern, rpl, str):
    p = re.compile(pattern, re.I)
    return p.sub(rpl, str)

def render_form(form, from_input, to_input):
    # do each input from from_input to to_input
    inputs = list(form.inputs)
    def index(inputs, name):
        for n, input in enumerate(inputs):
            if input.name == name:
                return n
        return -1
       
    start = index(inputs, from_input)
    till = index(inputs, to_input)
    form.inputs = inputs[start:till+1]
    
    # render the top note ourselves
    html = ''
    if start == 0 and not form.valid:
        if form.note:
            html = '<div class="wrong">%s</div>\n' % form.note
        else:
            html = '<div class="wrong">Oups looks like you\'ve made a couple of errors. Please correct the errors below and try again.</div>\n'
    form.note = None
    
    html += form.render_css()
    form.inputs = tuple(inputs)
    
    return html

def get_site_domain():
    import config
    return config.site_domain