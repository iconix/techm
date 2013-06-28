#!/usr/bin/env python

# set_urls_dict()
from pattern.web import URL

# get_ner_entities()
import ner
import re

# get_titles()
# also in namespace: classes.title._Title
import feedparser
import collections

# get_trending_topics()
# also in namespace: classes.ttopic._TTopic
from pattern.web import Element, plaintext


def set_urls_dict():
    url_prefix = 'https://news.google.com/news/section?pz=1&cf=all&topic='
    urls_dict = {}

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


def get_ner_entities(string, name=None, host='localhost', port=8888, output_format='slashTags'):
    # output_format can also be 'xml' or 'inlineXML'

    tagger = ner.SocketNER(host=host, port=port, output_format=output_format)
    entity_dict = tagger.get_entities(string)

    for k in entity_dict.keys():
        if k != "LOCATION" and k != "ORGANIZATION" and k != "PERSON":
            del entity_dict[k]

    entity_values = []  # don't need NER tags within dict keys

    if name is not None:
        # remove all mentions of words contained in 'name' from entities
        for k, v in entity_dict.items():
            for entity in v:
                for word in re.split('\s', name):
                    entity = entity.replace(word, '').strip()
                if len(entity):  # if entity not empty
                    entity_values.append(entity)

    return entity_values


def get_titles(ttopic):
    from classes.title import _Title  # custom module

    #feed = feedparser.parse(ttopic.url)
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

        entities = get_ner_entities(title_str, ttopic.name)

        # count occurrences of each entity (returns list of tuples)
        entity_freqs = collections.Counter(entities).most_common()

        ttopic.Title = _Title  # set inner class
        title_obj = ttopic.Title(title_str, entity_freqs, ttopic.freqs)
        titles.append(title_obj)

    return titles


def get_trending_topics(section):
    from classes.ttopic import _TTopic  # custom module

    gn_nav_topic_list = 'nav-topic-list'  # DOM
    topics_element = Element(section.url.download()).by_id(gn_nav_topic_list)

    if topics_element is not None:
        plaintext_src = plaintext(topics_element.source)
        topics = filter(None, plaintext_src.splitlines())
    else:  # no particular topics, which shouldn't happen currently
        topics = [u'All']

    trending_topics = []

    print "# trending topics:", len(topics)

    for topic in topics:
        section.TTopic = _TTopic  # set inner class
        t_obj = section.TTopic(topic, section.url)
        trending_topics.append(t_obj)

    return trending_topics
