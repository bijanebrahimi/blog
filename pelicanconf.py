#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Bijan'
SITENAME = 'Routines Excluded'
SITEURL = ''

PATH = 'content'
STATIC_PATHS = ['assets']
EXTRA_PATH_METADATA = {
    'assets/favicon.ico': {'path': 'favicon.ico'}
}

TIMEZONE = 'Asia/Tehran'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Fork Me on Github', 'https://github.com/bijanebrahimi/blog'),)

# Social widget
SOCIAL = (('Twitter', 'https://twitter.com/xxbijanxx'),
          ('Github', 'https://github.com/bijanebrahimi'),)

DEFAULT_PAGINATION = 5

# Plugins
# PLUGINS = ['sitemap', 'headerid']

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# THEME related configs
THEME = 'pelican-medius'
MEDIUS_AUTHORS = {
    'Bijan': {
        'description': """
            I Love to Read, Code and Explore the Possibilities.
        """,
        'cover': 'http://bijanebrahimi.github.io/blog/assets/images/post_category_linux.jpg',
        'image': 'http://bijanebrahimi.github.io/blog/assets/images/author.jpg',
        'links': (('github', 'https://github.com/bijanebrahimi'),
                  ('twitter-square', 'https://twitter.com/xxbijanxx')),
    }
}
MEDIUS_CATEGORIES = {
    'Projects': {
        'description': 'You can follow me also at github.com/bijanebrahimi',
        'thumbnail': 'http://bijanebrahimi.github.io/blog/assets/images/category_projects_thumb.png'
    },
    'Gist': {
        'description': 'Useful snippets of code',
        'thumbnail': 'http://bijanebrahimi.github.io/blog/assets/images/category_gist_thumb.png'
    },
    'Linux': {
        'description': 'Linux Related Stuff',
        'thumbnail': 'http://bijanebrahimi.github.io/blog/assets/images/category_linux_thumb.png'
    },
}
