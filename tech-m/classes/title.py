#!/usr/bin/env python

import json


class _Title(object):  # new-style class, inherits from 'object'
    def __str__(self):
        # JSON formatted
        return ('{"TITLE": ' +
                '{"title_str": "' + str(self.title_str) +
                '", "entities": ' + json.dumps(self.entity_freqs) + '}}')

    def __repr__(self):
        return str(self)

    def __init__(self, title_str, entity_freqs, all_ttopic_freqs):
        self.title_str = title_str
        self.entity_freqs = dict(entity_freqs)

        # build list of entities for ENTIRE trending topic
        for e in entity_freqs:
            all_ttopic_freqs.append(str(e[0])*int(e[1]))
