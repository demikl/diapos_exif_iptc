#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from unidecode import unidecode
import re
import os
from peopleanalyser import PeopleAnalyser
from placeanalyser import PlaceAnalyser

class FileAnalyser(object):

    def __init__(self, path, name, unknown_tags_registrar, debug=False):
        self._path = path
        self._filename = name
        self._name = os.path.splitext(name)[0]
        self._unknown_registrar = unknown_tags_registrar
        self._debug = debug
        if self._debug: print "Analyser for [{}]".format(repr(self._name))

    def _is_skipped_word(self, word):
        return any([
                re.match('^b?[0-9]{1,2}$', sanitize(word)) is not None,
                re.match('^d?0?[0-9]{1,3}$', sanitize(word)) is not None,
                re.match('^img_[0-9]+$', sanitize(word)) is not None,
                re.match(r'^\([0-9]+\)$', sanitize(word)) is not None,
                re.match(r'^[ad46]_[0-9]+$', sanitize(word)) is not None,
        ])

    def peoples(self):
        analyser = PeopleAnalyser(self._unknown_registrar, self._debug)
        return self._analyse_category(analyser)

    def places(self):
        analyser = PlaceAnalyser(self._unknown_registrar, self._debug)
        return self._analyse_category(analyser)

    def _analyse_category(self, analyser):
        res = []
        words = self._name.split()
        if self._debug: print "Words for file:", words
        for idx, word in enumerate(words):
            if self._is_skipped_word(word):
                continue
            triplet = (
                    words[idx-1] if idx > 0 else "",
                    word,
                    words[idx+1] if idx+1 < len(words) else ""
            )
            if self._debug: print "triplet:", repr(triplet)
            names = analyser.get_known_tags(triplet)
            if names:
                res.extend(names)
        # déduplication
        return list(set(res))



def sanitize(word):
    return unidecode(unicode(word, 'utf8')).lower()
