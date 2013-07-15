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

# build_entities()
# in namespace: classes.entity._Entity

# cluster_entities()
from operator import attrgetter


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


def get_entities(ttopic):
    from classes.ps import PrefixSpan  # custom module

    articles = get_articles(ttopic)
    all_ttopic_freqs = []  # build list of entities for ENTIRE trending topic

    for article in articles:
        title = article.title
        entities = get_ner_entities(title, ttopic.name)

        # count occurrences of each entity (returns list of tuples)
        entity_freqs = collections.Counter(entities).most_common()
        for e in entity_freqs:
            all_ttopic_freqs.append(str(e[0])*int(e[1]))

    # start PrefixSpan
    db = []
    for entity in all_ttopic_freqs:
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

    all_ttopic_freqs = collections.Counter(formatted_patterns).most_common()
    entities = build_entities(ttopic, all_ttopic_freqs, articles)
    entities = cluster_entities(entities)

    return entities


def get_articles(ttopic):
    from classes.article import _Article  # custom module

    feed = feedparser.parse(ttopic.url)
    #feed = feedparser.parse(r'/home/narhodes/Documents/google_news_feed/data-layer/output/kim_kardashian.rss')
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

        ttopic.Article = _Article  # set inner class
        article_obj = ttopic.Article(title, url)
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


def build_entities(ttopic, all_ttopic_freqs, articles):
    from classes.entity import _Entity  # custom module

    ttopic.Entity = _Entity  # set inner class
    entities = []
    used_tuples = []

    for article in articles:
        for name, count in dict(all_ttopic_freqs).items():
            if name in article.title:
                if (name, count) in used_tuples:
                    index = used_tuples.index((name, count))
                    e_obj = entities.pop(index)
                    used_tuples.pop(index)
                else:
                    e_obj = ttopic.Entity(name, count)

                e_obj.add_article(article)
                entities.append(e_obj)
                used_tuples.append((name, count))

    return entities


def cluster_entities(entities):
    # there's definitely a better way to do this
    # by passing around indices into "entities" list rather
    # then the entities themselves...
    groups = []

    for i in range(len(entities)):
        curr = entities[i]
        curr_group = set([curr])
        for j in range(i + 1, len(entities)):
            other = entities[j]
            if curr.name.lower() in other.name.lower():
                if curr.count == other.count and curr in curr_group:
                    curr_group.remove(curr)
                curr_group.add(other)
            if other.name.lower() in curr.name.lower() and curr.count != other.count:
                curr_group.add(other)

        prev_e = None
        for e in sorted(curr_group, key=attrgetter('count'), reverse=True):
            if prev_e is not None:
                if (prev_e.count == e.count):
                    if (len(e.name) < len(prev_e.name)):
                        curr_group.remove(e)
                    else:
                        curr_group.remove(prev_e)
                        prev_e = e
                else:
                    prev_e = e
            else:
                prev_e = e

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
            tmp.append(list(s))

    groups = tmp
    return groups
