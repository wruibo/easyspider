import sys
sys.path.append("..")

import urllib2
import threading

from esutil import es_html
from es_error import es_error

class es_crawler(threading.Thread):
    def __init__(self, linkdb, parser, filter, pipe):
        self._linkdb = linkdb
        self._parser = parser
        self._pipe = pipe
        self._filter = filter
        
        self._stopped = True
        threading.Thread.__init__(self)

    def start(self):
        if(self._stopped):
            self._stopped = False
            self.setDaemon(True)
            threading.Thread.start(self)

    def stop(self):
        if(not self._stopped):
            self._stopped = True
            self.join(None)

    def pop_link(self):
        link = self._linkdb.pop_link()
        return link

    def fetch_html(self, link):
        try:
            title, url, ref = link
            req = urllib2.urlopen(url)
            uhtml = es_html.html2unicode(req.read())
            req.close()
            return uhtml
        except Exception as err:
            raise es_error("fetch url: "+url+" failed.", __file__)
        finally:
            pass
    
    def parse_links(self, link, uhtml):
        links = self._parser.parse(link, uhtml)
        return links
    
    def push_links(self, links):
        allow_links = []
        for link in links:
            title, url, ref = link
            if(self._filter.allow(url)):
                allow_links.append(link)
        self._linkdb.push_links(allow_links)

    def deal_html(self, link, uhtml):
        self._pipe.deal(link, uhtml)

    def run(self):
        while(not self._stopped):
            try:
                #get next link to fetch
                link = self.pop_link()
                if(link):
                    #fetch the link content
                    uhtml = self.fetch_html(link)

                    #parse links from response content
                    links = self.parse_links(link, uhtml)

                    #put the new links to linkdb
                    self.push_links(links)

                    #deal the response content use pipe
                    self.deal_html(link, uhtml)
                else:
                    import time
                    time.sleep(1)
            except Exception as err:
                print err.message
                




