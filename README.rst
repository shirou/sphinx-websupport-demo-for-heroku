Sphinx Web support demo for Heroku
=================================================

This is a Sphinx web support demo repository.

This can

- n-gram full-text search by using whoosh(https://bitbucket.org/mchaput/whoosh/wiki/Home)

can not

- voting
- comment

This repository includes (a part of) python-doc-ja which can not be searched original Sphinx javascript search. By using this web support, you can search with any keyword with few seconds.


On th local environment
---------------------------

::

  % git clone 
  % cd 
  % virtualenv --no-site-packages .
  % bin/activate
  % pip install -r requirements.txt
  % python websupport/build.py
  % python websupport/__init__.py
  (access to http://127.0.0.1:5000/contents via your web browser)	


On the Heroku
----------------------

::

  (activate heroku environment)
  % python websupport/build.py
  % git add websupport/build
  % git commit
  % git push heroku master

Since index files and html files could not be generated on the Heroku, you should run the build.py script on your local machine. After generated, add these files to the git repository and push to the Heroku.



TODO
--------------

write this document.

