#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from taganalyser import TagAnalyser

class PeopleAnalyser(TagAnalyser):

    def __init__(self, *args, **kwargs):
        super(PeopleAnalyser, self).__init__(*args, **kwargs)
        self.KNOWN_TAGS = (
            "Claude", "Françoise", "Céline", "Sonia", "Mickaël", "Fabien",
            "Bernard", "Christian", "Odile", "Alain",
            "Auguste", "Marie-Louise", "Maurice", "Pépé", "Mémé",
            "Cyril", "Jérôme", "Blandine", "Pascal", "Alexis", "Elodie",
            "Christophe", "Mélanie",
            "Attila", "Louky", "Poluche"
        )
        self.ALIAS_TAGS = (
            (["dad"],                           ["Claude"]),
            (["mum"],                           ["Françoise"]),
            (["nous", "tous", "famille"],       ["Claude", "Françoise", "enfants"]),
            (["enfants"],                       ["Céline", "Sonia", "Mickaël", "Fabien"]),
            (["garçons"],                       ["Mickaël", "Fabien"]),
            (["filles"],                        ["Céline", "Sonia"]),
            (["pepere"],                        ["Auguste"]),
            (["Athila", "chat"],                ["Attila"]),
            (["Loucky", "loup"],                ["Louky"]),
            (["jeome"],                         ["Jérôme"]),
        )

        # liste des alias connus
        res = []
        for aliases_list, _ in self.ALIAS_TAGS:
            res.extend(aliases_list)
        self._unknown_registrar.set_aliases(res)

