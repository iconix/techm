#!/usr/bin/env python

import feedparser
from pattern.web import URL, Element, plaintext
import urllib
import unicodedata

# Google News Frontpage
GN_FRONT = 'https://www.google.com/news?pz=1&cf=all&ned=us&hl=en&output=rss'


class section:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.trending_topics = self.__get_trending_topics()

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "SECTION " + str(self.name) + " " + str(self.url) + " " + str(self.trending_topics)

    def get_trending_topics(self):
        nav_topic_list = Element(self.url.download()).by_id('nav-topic-list')

        if nav_topic_list is not None:
            plaintext_src = plaintext(nav_topic_list.source)
            topics = filter(None, plaintext_src.splitlines())
        else:  # no particular topics
            topics = [u'All']

        trending_topics = []

        print "SECTION", self.name

        for topic in topics:
            t = self.__ttopic__(topic)
            trending_topics.append(t)

        return trending_topics

    __get_trending_topics = get_trending_topics  # private copy

    class __ttopic__:
        def __init__(self, name):
            print name
            normalized_name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
            self.name = normalized_name
            url = GN_FRONT + '&q=' + urllib.quote(self.name)
            self.titles = self.__get_titles(url)

        def __repr__(self):
            return str(self)

        def __str__(self):
            return '{TOPIC: ' + str(self.name) + ', ' + str(self.titles) + '}'

        def get_titles(self, rss_url):
            """ PARAM: url of Google News RSS feed
                RETURNS: article titles for url """

            feed = feedparser.parse(rss_url)

            titles = []

            # for each article
            for i in range(0, len(feed.entries)):
                # convert unicode to string
                title_str = feed.entries[i].title.encode('ascii', 'ignore')

                # remove news organization at end of title
                title_str = title_str[:title_str.index(' - ')]

                titles.append(title_str)

            return titles

        __get_titles = get_titles  # private copy


def set_urls_dict():
    url_prefix = 'https://news.google.com/news/section?pz=1&cf=all&topic='
    urls_dict = {}

    urls_dict['Front Page'] = URL(GN_FRONT)
    urls_dict['Top Stories'] = URL('https://news.google.com/nwshp?hl=en&tab=nn')

    urls_dict['World'] = URL(url_prefix + 'w')
    urls_dict['U.S.'] = URL(url_prefix + 'n')
    urls_dict['Business'] = URL(url_prefix + 'b')
    urls_dict['Technology'] = URL(url_prefix + 'tc')
    urls_dict['Entertainment'] = URL(url_prefix + 'e')
    urls_dict['Sports'] = URL(url_prefix + 's')
    urls_dict['Health'] = URL(url_prefix + 'm')
    urls_dict['Science'] = URL(url_prefix + 'snc')

    return urls_dict


def main():
    urls_dict = set_urls_dict()

    sections = []

    for name, url in urls_dict.iteritems():
        s = section(name, url)
        sections.append(s)

    print sections

if __name__ == "__main__":
    main()

# next: run titles through Stanford Named Entity Tagger
  # if no tags made in a title, go to 'summary' and choose another title there to tag

# TODO change class string representations to JSON format
# TODO need more output to command line when running code
# TODO more comments
