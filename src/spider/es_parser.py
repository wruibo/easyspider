import sys
sys.path.append("..")

import re
from esutil import es_html
from es_error import es_error

class es_parser(object):
    #regex for parse out the url & text from a html
    _linkre = re.compile(ur'<a.* href="([^"]+)"[^>]*>(.*)</a>', re.IGNORECASE)

    #parse links from html content
    def parse(self, link, uhtml):
        try:
            title, url, ref = link
            baseurl = es_html.parse_baseurl(url)
            relative_links = self.__clean(self._linkre.findall(uhtml))
            links = []
            for newlink in relative_links:
                newurl, newtitle = newlink
                if(not newurl.startswith(u'/') and not newurl.startswith(u'http')): continue
                if(newurl.startswith(u'/')):
                    newurl = baseurl + newurl[1:]
                newtitle = es_html.extract_title(newtitle)
                links.append((newtitle, newurl, url))
            return links
        except Exception as err:
            raise es_error(err.message)
        finally:
            pass

    def __clean(self, links):
        tmpdict = {}
        for url, title in links:
            if(not tmpdict.has_key(url)):
                tmpdict[url] = (url, title)
            else:
                if(title and not tmpdict[url][1]):
                    tmpdict[url] = (url, title)
        return tmpdict.values()



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

