import re
import sys
sys.path.append("..")

class es_pipe(object):
    def __init__(self):
        self._rule = re.compile(r'http://www.letv.com/ptv/vplay/\d+.html', re.IGNORECASE)
        pass

    def deal(self, link, uhtml):
        title, url, ref = link
        if(self._rule.match(url)):
            print "fetched: ", title, url, ref


