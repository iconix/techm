#!/usr/bin/env python


class _Article(object):  # new-style class, inherits from 'object'
    def __str__(self):
        # JSON formatted
        return ('{"title": "' + str(self.title) +
                '", "url": "' + str(self.url) + '"}')

    def __repr__(self):
        return str(self)

    #def __init__(self, title, url, entity_freqs, all_ttopic_freqs):
    def __init__(self, title, url):
        self._title = title
        self._url = url

    @property
    def title(self):
        return self._title

    @property
    def url(self):
        return self._url
