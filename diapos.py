#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import os
import fnmatch
from unidecode import unidecode
from collections import defaultdict
from fileanalyser import FileAnalyser

def diapos_list(path):
    KNOWN_EXTENSIONS = ('jpg', 'JPG', 'JPEG', 'jpeg')
    for root, dirs, files in os.walk(os.path.abspath(path)):
        pictures = (f for f in files if any([f.endswith(ext) for ext in KNOWN_EXTENSIONS]))
        for filename in pictures:
            yield root, filename, os.path.join(root, filename)

class UnknownTags(object):
    def __init__(self):
        self.unknowns = set()
        self.knowns = defaultdict(set)

    def set_unknown(self, tag):
        if not any([tag in known for known in self.knowns.values()]):
            if need_debug(tag): print "***SETTING TO UNKNOWN: {}***".format(tag)
            self.unknowns.add(tag)

    def is_known(self, categ, name):
        self.knowns[categ].add(name)
        if name in self.unknowns:
            self.unknowns.remove(name)

    def set_aliases(self, aliases):
        aliases = [sanitize(s) for s in aliases]
        self.knowns["alias"] |= set(aliases)

def sanitize(word):
    return unidecode(unicode(word, 'utf8')).lower()

def need_debug(f):
    f = sanitize(f)
    for keyword in ["filles"]:
        try:
            f.index(sanitize(keyword))
        except:
            pass
        else:
            return True
    return False

if __name__ == '__main__':
    unknowns = UnknownTags()
    for f in diapos_list(sys.argv[1]):
        debug = need_debug(f[1])
        analyser = FileAnalyser(f[0], f[1], unknowns, debug)
        analyser.peoples()
        analyser.places()
    print "Unknowns:", unknowns.unknowns
    for categ, values in unknowns.knowns.iteritems():
        print categ, values
