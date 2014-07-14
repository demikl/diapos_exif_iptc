#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from unidecode import unidecode
import re

class TagAnalyser(object):

    def __init__(self, unknown_tags_registrar, debug=False):
        self._unknown_registrar = unknown_tags_registrar
        self.KNOWN_TAGS = ()
        self.ALIAS_TAGS = ( ([], []) )
        self._debug = debug

    def get_known_tags(self, triplet):
        if self._debug: print "  analysing", triplet
        to_check = [triplet]
        res = []

        while to_check:
            prec, name, suiv = to_check.pop()
            if self._debug: print "     resolve alias", (prec,name,suiv)
            new_names = self._resolve_alias(name, prec, suiv)

            # si invariance : plus de résolutions a effectuer
            if len(new_names)==1 and new_names[0] == name:
                if self._debug: print "       got invariance:", name
                res.append(name)
            else:
                # on empile les nouveaux noms obtenus sans le contexte précédent et suivant
                if self._debug: print "       got new words:", new_names
                to_check.extend([("",n,"") for n in new_names])

        if self._debug: print "tags for triplet {}: {}".format(triplet, res)
        tags = []
        for name in res:
            matched = [(idx,tag) for idx, tag in enumerate(self.KNOWN_TAGS) if sanitize(tag) == sanitize(name)]
            if not matched:
                if self._debug: print "unknown:",name
                self._unknown_registrar.set_unknown(sanitize(name))
            else:
                if self._debug: print "matched: ", repr(matched)
                name = self.KNOWN_TAGS[matched[0][0]]
                self._unknown_registrar.is_known(self.__class__.__name__, sanitize(name))
                tags.append(name)
        return tags

    def _resolve_alias(self, name, prec, suiv):
        # ignorer les accents et autres caractères non ASCII, et tout mettre en minuscule
        try:
            u_prec = sanitize(prec)
            u_name = sanitize(name)
            u_suiv = sanitize(suiv)
        except:
            print "Impossible de decoder: ({}, {}, {})".format(repr(prec), repr(name), repr(suiv))
            raise

        # séparateur des mots composés
        compound_names_pattern = re.compile(' |-')

        # est-on en présence d'un alias ?
        for aliases, real_names in self.ALIAS_TAGS:
            for alias in aliases:
                alias = sanitize(alias)
                num_words = len(compound_names_pattern.split(alias))
                if num_words == 2:
                    checked_words = [' '.join([u_prec, u_name]), ' '.join([u_name, u_suiv])]
                elif num_words == 3:
                    checked_words = [' '.join([u_prec, u_name, u_suiv])]
                else:
                    checked_words = [u_name]
                if alias in checked_words:
                    return real_names
        return [name]


def sanitize(word):
    return unidecode(unicode(word, 'utf8')).lower()
