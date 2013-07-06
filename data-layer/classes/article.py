#!/usr/bin/env python

import json


class _Article(object):  # new-style class, inherits from 'object'
    def __str__(self):
        # JSON formatted
        return ('{"title": "' + str(self.title) +
                '", "url": "' + str(self.url) +
                '", "entities": ' + json.dumps(self.entity_freqs) + '}')

    def __repr__(self):
        return str(self)

    def __init__(self, title, url, entity_freqs, all_ttopic_freqs):
        self._title = title
        self._url = url
        self._entity_freqs = dict(entity_freqs)

        # build list of entities for ENTIRE trending topic
        for e in entity_freqs:
            all_ttopic_freqs.append(str(e[0])*int(e[1]))

    @property
    def title(self):
        return self._title

    @property
    def url(self):
        return self._url

    @property
    def entity_freqs(self):
        return self._entity_freqs
