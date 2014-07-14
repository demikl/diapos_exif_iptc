#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from taganalyser import TagAnalyser


class PlaceAnalyser(TagAnalyser):

    def __init__(self, *args, **kwargs):
        super(PlaceAnalyser, self).__init__(*args, **kwargs)
        self.PLACES = (
            ("Challes",                 (45.5498625,5.982836)),
            ("Briançon",                (44.8995264,6.6536545)),
            ("Quinéville",              (49.5107505,-1.305604)),
            ("Criel",                   (50.0220695,1.3213355)),
            ("Argelès",                 (42.530141,3.0231845)),
            ("Banyuls",                 (42.4601954,3.1014855)),
            ("Lac Pavin",               (45.4959025,2.887924)),
            ("Utah",                    (49.4133856,-1.173743)),
            ("Queyras",                 (44.755773,6.877993)),
            ("Cauterets",               (42.8656675,-0.1429615)),
            ("La Raviège",              (43.591483,2.62282)),
            ("Ault",                    (50.0942384,1.443966)),
            ("Savines",                 (44.530011,6.3950151)),
            ("Vendée",                  (46.7452249,-1.9797417)),
            ("Friebourg",               (47.999718,7.6439847)),
            ("Chamonix",                (45.9296295,6.9293924)),
            ("Domme",                   (44.809095,1.2423955)),
            ("Sauze",                   (44.485987,6.3277345)),
            ("Manigod",                 ()),
            ("Kayserberg",              ()),
            ("Blaye",                   ()),
            ("St Antonin Noble Val",    ()),
            ("Megève",                  ()),
        )
        self.KNOWN_TAGS = [name for name, geopos in self.PLACES]
        self.ALIAS_TAGS = (
            (["querras"],               ["Queyras"]),
            (["cauteret"],              ["Cauterets"]),
            (["antonin"],               ["St Antonin Noble Val"]),
        )

        # liste des alias connus
        res = []
        for aliases_list, _ in self.ALIAS_TAGS:
            res.extend(aliases_list)
        self._unknown_registrar.set_aliases(res)
