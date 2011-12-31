#!/usr/bin/env python
# -*- coding: utf-8 -*-

#### sphinx part. same as build.py

from sphinx.websupport import WebSupport
from sphinx.websupport.errors import DocumentNotFoundError
from sphinx.websupport.search import whooshsearch
from sphinx.websupport.storage.sqlalchemystorage import SQLAlchemyStorage

from werkzeug import SharedDataMiddleware

from whoosh.fields import Schema, ID, TEXT, NGRAM

import os
import cPickle as pickle

ROOT = os.path.dirname(os.path.abspath(__file__))
SRCDIR = os.path.join(ROOT, 'source')
BUILDDIR = os.path.join(ROOT, 'build', 'web')
INDEXDIR = os.path.join(BUILDDIR, "data", "db")

print("SRC:{0}, BUILD:{1}, INDEX:{2}".format(SRCDIR,
                                             BUILDDIR,
                                             INDEXDIR))

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

#### flask part 

from flask import Flask, render_template, abort, g, request, jsonify, url_for
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)

#app.debug = True # 

app.jinja_env = Environment(loader = FileSystemLoader(os.path.join(ROOT, "_templates/")),
			    extensions=['jinja2.ext.i18n'])

app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/static/': os.path.join(BUILDDIR, 'static')
    })

def get_doc(docname, datadir):
    docpath = os.path.join(datadir, 'pickles', docname)
    if os.path.isdir(docpath):
        infilename = docpath + '/index.fpickle'
        if not docname:
            docname = 'index'
        else:
            docname += '/index'
    else:
        infilename = docpath + '.fpickle'
    try:
        f = open(infilename, 'rb')
    except IOError, e:
        raise DocumentNotFoundError(
            'The document "%s" could not be found' % docname)
    try:
        document = pickle.load(f)
    finally:
        f.close()
    return document

@app.route('/<path:docname>/')  # http://127.0.0.1/index/?highlight=<keyword>
@app.route('/<path:docname>')
def index(docname):
    try:
        h = request.args.get('highlight', '')
        docname = docname.rstrip('/') #delete last "/"
        document = get_doc(docname, support.datadir)
        if (h):
            document['body'] = document['body'].replace(h, '<strong>'+h+'</strong>')
    except DocumentNotFoundError, e:
        abort(404)
    except Exception, e:
        print(e)
        abort(500)

    try:
        return render_template('doc.html', document=document)
    except Exception, e:
        print(e)
        abort(503)

@app.route('/_add_comment', methods=['POST'])
def add_comment():
    parent_id = request.form.get('parent', '')
    node_id = request.form.get('node', '')
    text = request.form.get('text', '')
    proposal = request.form.get('proposal', '')
    username = None
    comment = support.add_comment(text, node_id=node_id,
                                  parent_id=parent_id,
                                  username=username, proposal=proposal)
    return jsonify(comment=comment)

@app.route('/_get_comments')
def get_comments():
    username = None
    node_id = request.args.get('node', '')
    data = support.get_data(node_id, username=username)
    return jsonify(**data)

@app.route('/search/')
def search():
    q = request.args.get('q')
    document = support.get_search_results(q)
    return render_template('doc.html', document=document)

if __name__ == '__main__':
    app.run()
