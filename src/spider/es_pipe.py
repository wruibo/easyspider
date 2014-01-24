import sys
sys.path.append("..")

class es_pipe(object):
    def __init__(self):
        pass

    def deal(self, link, uhtml):
        title, url, ref = link
        print "fetched: ", title, url, ref


