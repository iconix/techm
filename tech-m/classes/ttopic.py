#!/usr/bin/env python

import collections
import json
import unicodedata
import urllib

# custom module
from utils import get_titles


class _TTopic(object):  # new-style class, inherits from 'object'
        def __str__(self):
            # JSON formatted
            return ('{"TOPIC": ' +
                    '{"name": "' + str(self.name) +
                    '", "url": "' + str(self.url) +
                    '", "all_topic_entities": ' + json.dumps(dict(self.freqs)) +
                    ', "titles": ' + str(self.titles) + '}}')

        def __repr__(self):
            return str(self)

        def __init__(self, name, url):
            #normalized_name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
            normalized_name = "Kim Kardashian"

            if normalized_name == 'All':  # no particular topics
                url_str = url.string.encode('ascii', 'ignore')
            else:
                gn_rss = 'https://www.google.com/news?cf=all&ned=us&hl=en&output=rss&num=100'
                url_str = gn_rss + '&q=' + urllib.quote(normalized_name)

            self._Title = None  # inner class
            self._name = normalized_name
            self._url = url_str
            self._freqs = []
            self._titles = get_titles(self)
            self._freqs = collections.Counter(self._freqs).most_common()

        @property
        def name(self):
            return self._name

        @property
        def url(self):
            return self._url

        @property
        def titles(self):
            return self._titles

        @property
        def freqs(self):
            return self._freqs

        @property
        def Title(self):
            return self._Title

        @Title.setter
        def Title(self, value):
            self._Title = value
