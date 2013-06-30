#!/usr/bin/env python

import collections
import json
import re
import unicodedata
import urllib

# custom modules
from utils import get_titles
from classes.ps import PrefixSpan


class _TTopic(object):  # new-style class, inherits from 'object'
        def __str__(self):
            # JSON formatted
            return ('{"name": "' + str(self.name) +
                    '", "url": "' + str(self.url) +
                    '", "all_topic_entities": ' + json.dumps(dict(self.freqs)) +
                    ', "TITLES": ' + str(self.titles) + '}')

        def __repr__(self):
            return str(self)

        def __init__(self, name, url):
            normalized_name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
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

            # start PrefixSpan
            db = []
            for entity in self._freqs:
                db.append(re.split('\s+', entity))
            span = PrefixSpan(db)
            span.run(2)
            patterns = span.get_patterns()

            formatted_patterns = []
            for p in patterns:
                p0 = ' '.join(p[0])
                t = [p0] * int(p[1])
                formatted_patterns.extend(t)
            # end PrefixSpan

            self._freqs = collections.Counter(formatted_patterns).most_common()

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
