# -*- coding: utf-8 -*-
#
# Python documentation build configuration file
#
# This file is execfile()d with the current directory set to its containing dir.
#
# The contents of this file are pickled, so don't put values in the namespace
# that aren't pickleable (module imports are okay, they're removed automatically).

import sys, os, time
sys.path.append(os.path.abspath('tools/sphinxext'))

# General configuration
# ---------------------

# ../Include ディレクトリが存在しないので、coverage拡張を無効化
# 翻訳時のtodoを記録するために、todo拡張を有効化

extensions = ['sphinx.ext.refcounting',
              'sphinx.ext.doctest',
              'pyspecific',
              'sphinx.ext.todo',
              'jpsupport',
              ]
templates_path = ['tools/sphinxext']

# General substitutions.
project = 'Python'
copyright = '1990-%s, Python Software Foundation' % time.strftime('%Y')

# The default replacements for |version| and |release|.
#
# The short X.Y version.
# version = '2.6'
# The full version, including alpha/beta/rc tags.
# release = '2.6a0'

# We look for the Include/patchlevel.h file in the current Python source tree
# and replace the values accordingly.
#import patchlevel
#version, release = patchlevel.get_version_info()
version, release = '2.7', '2.7ja1'

language = 'ja'

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
today = ''
# Else, today_fmt is used as the format for a strftime call.
today_fmt = u'%Y年 %m月 %d日'

# List of files that shouldn't be included in the build.
unused_docs = [
    'maclib/scrap',
    'library/xmllib',
    'library/xml.etree',
    'documenting/sphinx',
]

# Relative filename of the reference count data file.
refcount_file = 'data/refcounts.dat'

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = True

# directory paths to ignore
exclude_trees = [
        'refs',
        'tools',
]

exclude_dirnames = ['diff', 'orig', 'tools']

trim_doctest_flags = False


# Options for HTML output
# -----------------------

html_theme = 'sphinxdoc'

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%Y-%m-%d'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
html_use_smartypants = True

# Custom sidebar templates, filenames relative to this file.
html_sidebars = {
    'index': 'indexsidebar.html',
}

# Additional templates that should be rendered to pages.
html_additional_pages = {
    #'download': 'download.html',
    'index': 'indexcontent.html',
}

# Output an OpenSearch description file.
html_use_opensearch = 'http://docs.python.org/dev'

# Additional static files.
html_static_path = ['tools/sphinxext/static']

# Output file base name for HTML help builder.
htmlhelp_basename = 'python' + release.replace('.', '')

# Split the index
html_split_index = True


# Options for LaTeX output
# ------------------------

# todo: translate commented topics.
# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, document class [howto/manual]).
_stdauthor = r'Guido van Rossum\\Fred L. Drake, Jr., editor'
latex_documents = [
    ('c-api/index', 'c-api.tex',
     '', _stdauthor, 'manual'),
    ('distutils/index', 'distutils.tex',
     '', _stdauthor, 'manual'),
    ('documenting/index', 'documenting.tex',
     '', 'Georg Brandl', 'manual'),
    ('extending/index', 'extending.tex',
     '', _stdauthor, 'manual'),
    ('install/index', 'install.tex',
     '', _stdauthor, 'manual'),
    ('library/index', 'library.tex',
     '', _stdauthor, 'manual'),
    ('reference/index', 'reference.tex',
     '', _stdauthor, 'manual'),
    ('tutorial/index', 'tutorial.tex',
     '', _stdauthor, 'manual'),
    ('using/index', 'using.tex',
     '', _stdauthor, 'manual'),
    ('faq/index', 'faq.tex',
     '', _stdauthor, 'manual'),
    ('whatsnew/' + version, 'whatsnew.tex',
     '', 'A. M. Kuchling', 'howto'),
]

# Collect all HOWTOs individually
latex_documents.extend(('howto/' + fn[:-4], 'howto-' + fn[:-4] + '.tex',
                        '', _stdauthor, 'howto')
                       for fn in os.listdir('howto')
                       if fn.endswith('.rst') and fn != 'index.rst')

# Additional stuff for the LaTeX preamble.
latex_preamble = r'''
\authoraddress{
  \strong{Python Software Foundation}\\
  Email: \email{docs@python.org}
}
'''

# Documents to append as an appendix to all manuals.
latex_appendices = ['glossary', 'about', 'license', 'copyright']

latex_docclass = {'manual': 'jsbook', 'howto': 'jsarticle'}
latex_elements = {
        'papersize': 'a4paper',
        'pointsize': '10pt',
        }

# Options for the coverage checker
# --------------------------------

# The coverage checker will ignore all modules/functions/classes whose names
# match any of the following regexes (using re.match).
coverage_ignore_modules = [
    r'[T|t][k|K]',
    r'Tix',
    r'distutils.*',
]

coverage_ignore_functions = [
    'test($|_)',
]

coverage_ignore_classes = [
]

# Glob patterns for C source files for C API coverage, relative to this directory.
coverage_c_path = [
    '../Include/*.h',
]

# Regexes to find C items in the source files.
coverage_c_regexes = {
    'cfunction': (r'^PyAPI_FUNC\(.*\)\s+([^_][\w_]+)'),
    'data': (r'^PyAPI_DATA\(.*\)\s+([^_][\w_]+)'),
    'macro': (r'^#define ([^_][\w_]+)\(.*\)[\s|\\]'),
}

# The coverage checker will ignore all C items whose names match these regexes
# (using re.match) -- the keys must be the same as in coverage_c_regexes.
coverage_ignore_c_items = {
#    'cfunction': [...]
}


# -- Options for Epub output ---------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = u'Python ドキュメント 日本語訳'
epub_author = u'Python ドキュメント 翻訳プロジェクト'
epub_publisher = epub_author
epub_copyright = u'2010, Pythonドキュメント翻訳プロジェクト'

# The language of the text. It defaults to the language option
# or en if the language is not set.
#epub_language = ''

# The scheme of the identifier. Typical schemes are ISBN or URL.
#epub_scheme = ''

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#epub_identifier = ''

# A unique identification for the text.
#epub_uid = ''

# HTML files that should be inserted before the pages created by sphinx.
# The format is a list of tuples containing the path and title.
#epub_pre_files = []

# HTML files shat should be inserted after the pages created by sphinx.
# The format is a list of tuples containing the path and title.
#epub_post_files = []

# A list of files that should not be packed into the epub file.
#epub_exclude_files = []

# The depth of the table of contents in toc.ncx.
#epub_tocdepth = 3

# Allow duplicate toc entries.
#epub_tocdup = True
