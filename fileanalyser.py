#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from unidecode import unidecode
import re
import os

class FileAnalyser(object):

    KNOWN_PEOPLE = (
            "Claude", "Françoise", "Céline", "Sonia", "Mickaël", "Fabien",
            "Bernard", "Christian", "Odile", "Alain",
            "Auguste", "Marie-Louise", "Maurice",
            "Cyril", "Jérôme", "Blandine", "Pascal", "Alexis", "Elodie",
            "Christophe", "Mélanie",
            "Attila", "Louky", "Poluche"
    )
    ALIAS_PEOPLE = (
        (["dad"],                           ["Claude"]),
        (["mum"],                           ["Françoise"]),
        (["nous", "tous", "famille"],       ["Claude", "Françoise", "enfants"]),
        (["enfants"],                       ["Céline", "Sonia", "Mickaël", "Fabien"]),
        (["garçons"],                       ["Mickaël", "Fabien"]),
        (["filles"],                        ["Céline", "Sonia"]),
        (["Athila", "chat"],                ["Attila"]),
        (["Loucky", "loup"],                ["Louky"])
    )


    def __init__(self, path, name, unknown_tags_registrar):
        self._path = path
        self._filename = name
        self._name = os.path.splitext(name)[0]
        print "Analyser for [{}]".format(repr(self._name))
        self._unknown_registrar = unknown_tags_registrar

    def peoples(self):
        res = []
        words = self._name.split()
        for idx, word in enumerate(words):
            triplet = (
                    words[idx-1] if idx > 0 else "",
                    word,
                    words[idx+1] if idx+1 < len(words) else ""
            )
            print "triplet:", repr(triplet)
            names = self._get_canonical_names(triplet)
            if names:
                res.extend(names)
        # déduplication
        return list(set(res))

    def _get_canonical_names(self, triplet):
        to_check = [triplet]
        res = []

        while to_check:
            prec, name, suiv = to_check.pop()
            new_names = self._resolve_people_alias(name, prec, suiv)

            # si invariance : plus de résolutions a effectuer
            if len(new_names)==1 and new_names[0] == name:
                res.append(name)
            else:
                # on empile les nouveaux noms obtenus sans le contexte précédent et suivant
                to_check.extend([("",n,"") for n in new_names])

        print "tags for triplet {}: {}".format(triplet, res)
        peoples = []
        for name in res:
            matched = [(idx,who) for idx, who in enumerate(self.KNOWN_PEOPLE) if sanitize(who) == sanitize(name)]
            if not matched:
                print "unknown:",name
                self._unknown_registrar.set_unknown(name)
            else:
                print "matched: ", repr(matched)
                name = self.KNOWN_PEOPLE[matched[0][0]]
                self._unknown_registrar.is_people(name)
                peoples.append(name)
        return peoples

    def _resolve_people_alias(self, name, prec, suiv):
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
        for aliases, real_people_names in self.ALIAS_PEOPLE:
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
                    return real_people_names
        return [name]


def sanitize(word):
    return unidecode(unicode(word, 'utf8')).lower()
