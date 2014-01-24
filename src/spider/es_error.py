import sys

class es_error(Exception):
    def __init__(self, errmsg, file):
       self.message = "Error: " + errmsg + " [" + file + "]"

if(__name__ == '__main__'):
    import sys
    try:
        raise es_error("test error", __file__)
    except Exception as err:
        print err.message


