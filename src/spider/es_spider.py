import sys
sys.path.append("..")

from es_pipe import es_es_pipe
from es_filter import es_filter
from es_parser import es_parser
from es_linkdb import es_linkdb
from es_crawler import es_crawler

class es_spider(object):
    def __init__(self, workdir, crawler_num=1):
        self._workdir = workdir
        self._pipe = es_pipe()
        self._filter = es_filter()
        self._parser = es_parser()
        self._linkdb = es_linkdb(workdir)

        self._crawlers = []
        for i in range(0, crawler_num):
            self._crawlers.append(es_crawler(self._linkdb, self._parser, self._filter, self._pipe))

    def feed(self, title, url):
        self._linkdb.push_links([(title, url, 'blank')])

    def allow(self, rexpr):
        self._filter.add_white_list(rexpr)

    def disallow(self, rexpr):
        self._filter.add_black_list(rexpr)

    def start(self):
        for crawler in self._crawlers:
            crawler.start()

    def stop(self):
        for crawler in self._crawlers:
            crawler.stop()

if(__name__ == '__main__'):
    import sys
    if(len(sys.argv) != 2):
        print "usage: python spider <url>"
        print sys.argv
        sys.exit(1)
    print sys.argv
    myspider = es_spider("../")
    myspider.allow(r'http://www.letv.com/ptv/vplay/.*')
    myspider.allow(r'http://movie.letv.com/.*')
    myspider.allow(r'http://list.letv.com/listn/.*')
    myspider.allow(r'http://www.letv.com/')

    myspider.feed("test", sys.argv[1])
    myspider.start()

    while(1):
        import time
        time.sleep(1)

