from docutils.nodes import Text, paragraph
import re

_PAT = re.compile(ur"([^\u0000-\u00ff])\n([^\u0000-\u00ff])")

def trunc_whitespace(app, doctree, docname):
    if not app.config.japanesesupport_trunc_whitespace:
        return
    for node in doctree.traverse(Text):
        if isinstance(node.parent, paragraph):
            newtext = _PAT.sub(ur"\1\2", node.astext())
            node.parent.replace(node, Text(newtext))

def setup(app):
    app.add_config_value('japanesesupport_trunc_whitespace', True, True)
    app.connect("doctree-resolved", trunc_whitespace)
