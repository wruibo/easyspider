import sys
sys.path.append("..")

import os
import json
import bsddb
import shutil
import threading

from esutil import es_digest
from es_error import es_error



class es_linkdb(object):
    def __init__(self, workdir):
        #working directory for persistance
        self._linkdb_dir = workdir+"/links"
        #all history links crawled, key->sha1(url), value-><title, url, ref>
        self._linkdb_file = self._linkdb_dir+"/links.db"

        #file queues for persistent the new links
        self._fileq = es_fileq(workdir, "new_links_", 10000)

        #lock for thread access safety
        self._lock = threading.Lock()

        #open the database
        self.__open()

    def __del__(self):
        #close the database
        self.__close()

    def __open(self):
        #create relate work directory if needed
        if(not os.path.exists(self._linkdb_dir)):
            os.makedirs(self._linkdb_dir)

        #load the link db if exist otherwise create it
        self._linkdb = bsddb.btopen(self._linkdb_file, 'c')

        #current links for crawling
        self._currlinks = []

    def __close(self):
        self._lock.acquire()

        self.__flush_newlinks_to_file()

        self._lock.release()

    def push_links(self, links):
        self._lock.acquire()

        for link in links:
            title, url, ref = link
            urlsha1 = es_digest.sha1(url)
            if((not self._linkdb.has_key(urlsha1))):
                self._newlinks.append(link)
                self._linkdb[urlsha1] = self.__make_link_record(link)

        self.__flush_next_newlink_file()

        self._lock.release()

    def pop_links(self, num = None):
        links = None
        if(not num): num = 1
        self._lock.acquire()

        if(not self._currlinks):
           self.__load_next_newlink_file()

        if(self._currlinks): 
            links = self._currlinks[0:num]
            self._currlinks = self._currlinks[num:]

        self._lock.release()
        return links

    def pop_link(self):
        link = None
        self._lock.acquire()

        if(not self._currlinks):
           self._currlinks = 

        if(self._currlinks): 
            link = self._currlinks.pop(0)

        self._lock.release()
        return link

    def clear(self):
        shutil.rmtree(self._linkdb_dir)
   
    def __make_link_record(self, link):
        title, url, ref = link
        return json.dumps({'title':title, 'url':url, 'ref':ref})

    def __load_link_record(self, str):
        record = json.loads(str)
        return (record['title'], record['url'], record['ref'])

if( __name__ == '__main__'):
    linkdb = es_linkdb('d:/testdb')
    for i in range(0, 20001):
        linkdb.push_links([('test', 'http://www.baidu.com/'+str(i)+"/", 'none')])

    links = linkdb.pop_links(10000)
    links = linkdb.pop_links(1)
