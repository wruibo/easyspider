#!/usr/bin/env python3
import hashlib

#return md5 string of specified string data
def md5(strdata):
    bdata = strdata.encode()
    m = hashlib.md5()
    m.update(bdata)
    return m.hexdigest()

#return sha1 string of specified string data
def sha1(strdata):
    bdata = strdata.encode()
    m = hashlib.sha1()
    m.update(bdata)
    return m.hexdigest()
        