#!/usr/bin/env python

"""
Document storage.

One davenport oughta be enough for anybody. (This module is a singleton.)

The davenport described herein is both, a sofa and a desk.
"""

DATABASE = 'pyhkal'
REMEMBER = 'config'

import couchdb.client

_sofa = None

def use(location=None):
    """Start storing your documents in a davenport. `location` can be used to occupy a
    remote davenport. Otherwise use your local desk.

    """
    global _sofa
    server = couchdb.client.Server(location or couchdb.client.DEFAULT_BASE_URI)
    try:
        _sofa = server[DATABASE]
    except couchdb.client.ResourceNotFound:
        _sofa = server.create(DATABASE)

_none = object()
def remember(breadcrumbs, default=_none):
    """Remember that random fact that popped into your head 2 AM in the
    morning. For some weird reason, you need a sofa to remember.

    """
    config = get_by_label(REMEMBER)
    try:
        return reduce(lambda doc, value: doc[value],
                breadcrumbs.split(), config)
    except KeyError:
        if default is not _none:
            return default
        raise

def get_by_label(label):
    return _sofa[label]