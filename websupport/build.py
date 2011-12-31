#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sphinx.websupport import WebSupport
from sphinx.websupport.errors import DocumentNotFoundError
from sphinx.websupport.search import whooshsearch
from sphinx.websupport.storage.sqlalchemystorage import SQLAlchemyStorage

from whoosh.fields import Schema, ID, TEXT, NGRAM

import os

ROOT = os.path.dirname(os.path.abspath(__file__))
SRCDIR = os.path.join(ROOT, 'source')
BUILDDIR = os.path.join(ROOT, 'build', 'web')
INDEXDIR = os.path.join(BUILDDIR, "data", "db")

uri = os.environ.get('DATABASE_URL')  # DATABSE_URL is given
storage = SQLAlchemyStorage(uri)

whoosh = whooshsearch.WhooshSearch
whoosh.schema = Schema(path=ID(stored=True, unique=True),
                       title=TEXT(field_boost=2.0, stored=True),
                       text=NGRAM(stored=True))

search = whoosh(INDEXDIR)

support = WebSupport(srcdir=SRCDIR,
                     builddir=BUILDDIR,
                     search=search,
                     storage=storage)
support.build()
