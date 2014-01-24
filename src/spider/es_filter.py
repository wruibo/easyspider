import sys
sys.path.append("..")

import re

class es_filter(object):
    def __init__(self):
        self._regex_white_list = []
        self._regex_black_list = []

    def add_white_list(self, rexpr):
        reg = re.compile(rexpr, re.IGNORECASE)
        self._regex_white_list.append(reg)
    
    def add_black_list(self, rexpr):
        reg = re.compile(rexpr, re.IGNORECASE)
        self._regex_black_list.append(reg)

    def allow(self, url):
        if(self._regex_black_list):
            for regex in self._regex_black_list:
                if(regex.match(url)):
                    return False

        if(self._regex_white_list):
            for regex in self._regex_white_list:
                if(regex.match(url)):
                    return True
        else:
            return True







