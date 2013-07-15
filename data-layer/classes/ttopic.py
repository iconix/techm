#!/usr/bin/env python

import unicodedata
import urllib

# custom modules
from utils import get_entities


class _TTopic(object):  # new-style class, inherits from 'object'
        def __str__(self):
            # JSON formatted
            return ('{"name": "' + str(self.name) +
                    '", "url": "' + str(self.url) +
                    '", "ENTITIES": ' + str(self.entities) + '}')

        def __repr__(self):
            return str(self)

        def __init__(self, name, url):
            normalized_name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
            if normalized_name == 'All':  # no particular topics
                url_str = url.string.encode('ascii', 'ignore')
            else:
                gn_rss = 'https://www.google.com/news?cf=all&ned=us&hl=en&output=rss&num=100'
                url_str = gn_rss + '&q=' + urllib.quote(normalized_name)

            self._Article = None  # inner class
            self._name = normalized_name
            self._url = url_str
            self._entities = get_entities(self)

        @property
        def name(self):
            return self._name

        @property
        def url(self):
            return self._url

        @property
        def entities(self):
            return self._entities

        @property
        def Article(self):
            return self._Article

        @Article.setter
        def Article(self, value):
            self._Article = value
