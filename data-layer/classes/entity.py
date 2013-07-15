#!/usr/bin/env python


class _Entity(object):  # new-style class, inherits from 'object'
    def __str__(self):
        # JSON formatted
        return ('{"name": "' + str(self.name) +
                '", "count": ' + str(self.count) +
                ', "ARTICLES": ' + str(self.articles) + '}')

    def __repr__(self):
        return str(self)

    def __init__(self, name, count):
        self._name = name
        self._count = count
        # inefficiency: letting each entity have its own copy of articles
        self._articles = []

    def add_article(self, article):
        self._articles.append(article)

    @property
    def name(self):
        return self._name

    @property
    def count(self):
        return self._count

    @property
    def articles(self):
        return self._articles
