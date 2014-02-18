import re
from es_error import es_error

def parse_charset(bhtml):
    cre = re.compile('charset=["]*([a-zA-Z-0-9]+)["]*', re.IGNORECASE)
    charset = cre.search(bhtml)
    if(charset):
        return charset.group(1)
    raise eserror("parse charset from html content failed.", __file__)

def html2unicode(bhtml):
    try:
        charset = parse_charset(bhtml)
        uhtml = bhtml.decode(charset, 'ignore')
        return uhtml
    except Exception as err:
        raise es_error(err.message, __file__)
    finally:
        pass

def parse_baseurl(uurl):
    basere = re.compile(ur'(^[^/]+//[^/]+/?)', re.IGNORECASE)
    resobj = basere.search(uurl)
    if(resobj):
        baseurl = resobj.group(1)
        if(baseurl[-1] != u'/'):
            baseurl += u'/'
        return baseurl
    raise es_error("parse base url from url failed.", __file__)

def extract_title(uhtml):
    utext = []
    pos, endpos, is_datafield = 0, len(uhtml), True
    while pos<endpos:
        if(uhtml[pos] == u'<'): 
            is_datafield = False
        elif(uhtml[pos] == u'>'):
            is_datafield = True
        else:
            if(is_datafield and uhtml[pos] != u' ' and uhtml[pos] != '\n' and uhtml[pos] != '\r' and uhtml[pos] != '\t'):
                utext.append(uhtml[pos])
        pos += 1
    
    title = u''.join(utext)
    if(not title):
        altrule = re.compile(ur'alt=["|\']*([^"\']+)["|\']*')
        titles = altrule.findall(uhtml)
        if(titles):title = titles[0]

    return title
