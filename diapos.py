#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import os
import fnmatch
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
        self.peoples = set()
        self.places = set()
        self.dates = set()

    def set_unknown(self, tag):
        self.unknowns.add(tag)

    def is_people(self, name):
        self.peoples.add(name)
        try:
            self.unknowns.remove(name)
        except KeyError:
            pass

if __name__ == '__main__':
    unknowns = UnknownTags()
    for f in diapos_list(sys.argv[1]):
        analyser = FileAnalyser(f[0], f[1], unknowns)
        print analyser.peoples()
    print "Unknowns:", unknowns.unknowns
    print "People:", unknowns.peoples
