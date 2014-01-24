import sys
sys.path.append("..")

import re
from esutil import es_html
from es_error import es_error

class es_parser(object):
    #regex for parse out the url & text from a html
    _linkre = re.compile(ur'<a.* href="([^"]+)"[^>]*>(.*)</a>', re.IGNORECASE)

    #parse 
    def parse(self, url, ref, uhtml):
        try:
            baseurl = es_html.parse_baseurl(url)
            relative_links = self._linkre.findall(uhtml)
            links = []
            for link in relative_links:
                url, title = link
                if(not url.startswith(u'/') and not url.startswith(u'http')): continue

                if(url.startswith(u'/')):
                    url = baseurl + url[1:]
                title = es_html.extract_text(title)
                links.append((title, url, ref))
            return links
        except Exception as err:
            raise es_error(err.message)
        finally:
            pass

if(__name__ == "__main__"):
    import sys
    import urllib2
    if(len(sys.argv) < 2):
        print("Usage: python parser.py <url>")
        sys.exit(-1)

    url = sys.argv[1]
    con = urllib2.urlopen(url)
    bhtml = con.read()
    con.close()

    encoding = es_html.parse_charset(bhtml)
    uhtml = es_html.html2unicode(bhtml)
    parser = es_parser()
    links = parser.parse(url, 'unknown', uhtml)
    for link in links:
        print link[0], link[1]

