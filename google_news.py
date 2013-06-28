#!/usr/bin/env python

import feedparser
from pattern.web import URL, Element, plaintext
import urllib
import unicodedata
import ner
import collections
import json
import re


class section:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.trending_topics = self.__get_trending_topics()

    def __repr__(self):
        return str(self)

    def __str__(self):
        # JSON formatted
        return '{"SECTION": {"name": "' + str(self.name) + '", "url": "' + str(self.url) + '", "trending_topics": ' + str(self.trending_topics) + '}}'

    def get_trending_topics(self):
        nav_topic_list = Element(self.url.download()).by_id('nav-topic-list')  # DOM

        if nav_topic_list is not None:
            plaintext_src = plaintext(nav_topic_list.source)
            topics = filter(None, plaintext_src.splitlines())
        else:  # no particular topics, which shouldn't happen anymore
            topics = [u'All']

        trending_topics = []

        print "# trending topics:", len(topics)

        for topic in topics:
            t = self.__ttopic__(topic, self.url)
            trending_topics.append(t)

        return trending_topics

    __get_trending_topics = get_trending_topics  # private copy

    class __ttopic__:
        def __init__(self, name, url):
            normalized_name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
            #self.name = normalized_name
            self.name = "Kim Kardashian"
            if self.name != 'All':
                gn_rss = 'https://www.google.com/news?cf=all&ned=us&hl=en&output=rss&num=100'
                url_str = gn_rss + '&q=' + urllib.quote(self.name)
            else:  # no particular topics
                url_str = url.string.encode('ascii', 'ignore')
            self.url = url_str
            self.freqs = []
            self.titles = self.__get_titles(self.url)
            self.freqs = collections.Counter(self.freqs).most_common()

        def __repr__(self):
            return str(self)

        def __str__(self):
            # JSON formatted
            return '{"TOPIC": {"name": "' + str(self.name) + '", "url": "' + str(self.url) + '", "all_topic_entities": ' + json.dumps(dict(self.freqs)) + ', "titles": ' + str(self.titles) + '}}'

        """
        :param rss_url: raw string representing Google News RSS feed url
        :returns: article titles for url
        """
        def get_titles(self, rss_url):
            #feed = feedparser.parse(rss_url)
            feed = feedparser.parse(r'/home/narhodes/Documents/google_news_feed/kim_kardashian.rss')
            entries = feed.entries

            titles = []

            # for each article on rss page
            for i in range(0, len(entries)):
                # convert unicode to string
                title_str = entries[i].title.encode('ascii', 'ignore')

                # avoid incorrect quotation formatting in JSON representation
                title_str = title_str.replace('"', "'")

                # remove news organization at end of title
                end = title_str.find(' - ')
                if end != -1:  # substring not found
                    title_str = title_str[:end]

                entities = self.__get_ner_entities(title_str)

                # count occurrences of each entity (returns list of tuples)
                entity_freqs = collections.Counter(entities).most_common()

                title = self.__title__(title_str, entity_freqs, self.freqs)
                titles.append(title)

            return titles

        def get_ner_entities(self, string):
            host = 'localhost'
            tagger = ner.SocketNER(host=host, port=8888, output_format='slashTags')

            entity_dict = tagger.get_entities(string)
            for k in entity_dict.keys():
                if k != "LOCATION" and k != "ORGANIZATION" and k != "PERSON":
                    del entity_dict[k]

            entity_values = []  # don't need NER tags within dict keys

            # remove all mentions of words contained in ttopic.name
            for k, v in entity_dict.items():
                for entity in v:
                    for word in re.split('\s', self.name):
                        entity = entity.replace(word, '').strip()
                    if entity != '':
                        entity_values.append(entity)

            return entity_values

        class __title__:
            def __init__(self, title_str, entity_freqs, all_ttopic_freqs):
                self.title_str = title_str
                self.entity_freqs = entity_freqs

                # build list of entities for ENTIRE trending topic
                for e in self.entity_freqs:
                    all_ttopic_freqs.append(str(e[0])*int(e[1]))

            def __repr__(self):
                return str(self)

            def __str__(self):
                # JSON formatted
                return '{"TITLE": {"title_str": "' + str(self.title_str) + '", "entities": ' + json.dumps(dict(self.entity_freqs)) + '}}'

        __get_titles = get_titles  # private copy
        __get_ner_entities = get_ner_entities  # private copy


def set_urls_dict():
    url_prefix = 'https://news.google.com/news/section?pz=1&cf=all&topic='
    urls_dict = {}

    #urls_dict['Front Page'] = URL(GN_RSS_FRONT)
    urls_dict['Top Stories'] = URL('https://news.google.com/nwshp?hl=en&tab=nn')

    '''urls_dict['World'] = URL(url_prefix + 'w')
    urls_dict['U.S.'] = URL(url_prefix + 'n')
    urls_dict['Business'] = URL(url_prefix + 'b')
    urls_dict['Technology'] = URL(url_prefix + 'tc')
    urls_dict['Entertainment'] = URL(url_prefix + 'e')
    urls_dict['Sports'] = URL(url_prefix + 's')
    urls_dict['Health'] = URL(url_prefix + 'm')
    urls_dict['Science'] = URL(url_prefix + 'snc')'''

    return urls_dict


def main():
    urls_dict = set_urls_dict()

    sections = []
    count = 1
    total = len(urls_dict)

    for name, url in urls_dict.iteritems():
        print "Creating section", count, "of", total, "... (", name, ")"
        s = section(name, url)
        sections.append(s)
        count += 1

    print sections


if __name__ == "__main__":
    main()
