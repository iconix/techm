#!/usr/bin/env python

# custom module
from utils import get_trending_topics


class Section(object):  # new-style class, inherits from 'object'
    def __str__(self):
        # JSON formatted
        return ('{"title": "' + str(self.title) +
                '", "url": "' + str(self.url) +
                '", "TTOPICS": ' + str(self.trending_topics) + '}')

    def __repr__(self):
        return str(self)

    def __init__(self, title, url):
        self._TTopic = None  # inner class
        self._title = title
        self._url = url
        self._trending_topics = get_trending_topics(self)

    @property
    def title(self):
        return self._title

    @property
    def url(self):
        return self._url

    @property
    def trending_topics(self):
        return self._trending_topics

    @property
    def TTopic(self):
        return self._TTopic

    @TTopic.setter
    def TTopic(self, value):
        self._TTopic = value
