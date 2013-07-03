#!/usr/bin/env python

# set_urls_dict()
from pattern.web import URL

# get_ner_entities()
import ner
import re

# get_articles()
# also in namespace: classes.article._Article
import feedparser
import collections

# get_trending_topics()
# also in namespace: classes.ttopic._TTopic
from pattern.web import Element, plaintext


def set_urls_dict():
    url_prefix = 'https://news.google.com/news/section?pz=1&cf=all&topic='
    urls_dict = {}

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

    tmp = []
    # remove '&' and extra spaces in entities
    for entity in entity_values:
        if '&' in entity:
            entity = entity.replace('&', '').strip()
        tmp.append(entity)
    entity_values = tmp

    return entity_values


def get_articles(ttopic):
    from classes.article import _Article  # custom module

    feed = feedparser.parse(ttopic.url)
    #feed = feedparser.parse(r'/home/narhodes/Documents/google_news_feed/kim_kardashian.rss')
    entries = feed.entries

    articles = []

    # for each article on rss page
    for i in range(0, len(entries)):
        # article URL
        url = str(entries[i].link)
        url = url[url.find('&url=') + 5:]

        # convert unicode to string
        title = entries[i].title.encode('ascii', 'ignore')

        # avoid incorrect quotation formatting in JSON representation
        title = title.replace('"', "'")

        # remove news organization at end of article
        end = title.find(' - ')
        if end != -1:  # substring not found
            title = title[:end]

        entities = get_ner_entities(title, ttopic.name)

        # count occurrences of each entity (returns list of tuples)
        entity_freqs = collections.Counter(entities).most_common()

        ttopic.Article = _Article  # set inner class
        article_obj = ttopic.Article(title, url, entity_freqs, ttopic.freqs)
        articles.append(article_obj)

    return articles


def get_trending_topics(section):
    from classes.ttopic import _TTopic  # custom module

    gn_nav_topic_list = 'nav-topic-list'  # DOM
    topics_element = Element(section.url.download()).by_id(gn_nav_topic_list)
    #topics_element = None

    if topics_element is not None:
        plaintext_src = plaintext(topics_element.source)
        topics = filter(None, plaintext_src.splitlines())
    else:  # no particular topics, which shouldn't happen currently
        #topics = [u'All']
        topics = [u'Kim Kardashian']

    trending_topics = []

    print "# trending topics:", len(topics)

    for topic in topics:
        section.TTopic = _TTopic  # set inner class
        t_obj = section.TTopic(topic, section.url)
        trending_topics.append(t_obj)

    return trending_topics


def remove_unrelated_articles(ttopic):
    entities = dict(ttopic.freqs).keys()

    new_articles = []
    for article in ttopic.articles:
        if not len(article.entity_freqs):
            continue

        is_in_article = False
        for entity in entities:
            if entity in article.entity_freqs.keys():
                is_in_article = True
        if is_in_article:
            new_articles.append(article)

    return new_articles


def cluster_entities(entities):
    from operator import itemgetter

    entities_keys = entities.keys()
    groups = []

    for i in range(len(entities_keys)):
        curr = entities_keys[i]
        curr_group = set([(curr, entities[curr])])
        for j in range(i + 1, len(entities_keys)):
            rest = entities_keys[j]
            if curr.lower() in rest.lower():
                if entities[curr] == entities[rest] and (curr, entities[curr]) in curr_group:
                    curr_group.remove((curr, entities[curr]))
                curr_group.add((rest, entities[rest]))
            if rest.lower() in curr.lower() and entities[curr] != entities[rest]:
                curr_group.add((rest, entities[rest]))

        prev_entity = None
        for entity in sorted(curr_group, key=itemgetter(1), reverse=True):
            if prev_entity is not None:
                if (prev_entity[1] == entity[1]):
                    if (len(entity[0]) < len(prev_entity[0])):
                        curr_group.remove(entity)
                    else:
                        curr_group.remove(prev_entity)
                        prev_entity = entity
                else:
                    prev_entity = entity
            else:
                prev_entity = entity

        groups.append(curr_group)

    tmp = []
    used = []
    for i in range(len(groups)):
        s = groups[i]
        if s not in used:
            for j in range(i + 1, len(groups)):
                t = groups[j]
                if t not in used and len(s & t):
                    s = s | t
                    used.append(t)
            tmp.append(dict(s))

    groups = tmp
    return groups
