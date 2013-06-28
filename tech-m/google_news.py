#!/usr/bin/env python

# custom modules
from utils import set_urls_dict
from classes.section import Section


def main():
    urls = set_urls_dict()

    sections = []
    count = 1
    total = len(urls)

    for name, url in urls.iteritems():
        print "Creating section", count, "of", total, "... (", name, ")"
        s_obj = Section(name, url)
        sections.append(s_obj)
        count += 1

    print sections


if __name__ == "__main__":
    main()
