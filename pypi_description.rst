jsonesque
=========

Overview
--------

``jsonesque`` is a module for processing JSON-like strings into valid, minified
JSON. It enables a Python application to support an 'enhanced' form of JSON that
contains comments and trailing commas.

For example, given the following JSON-like input:

::

    {
        # This is a Python-style comment
        "a": 1,
        // This is a C-style comment
        "b": 2,
        /*
          This is a multi-line C-style comment
        */
        "c": [
            1,
            2,
            3, // This is a trailing comment pointing out a trailing comma
        ],
    }

``jsonesque`` would produce the following valid JSON:

::

    {"a":1,"b":2,"c":[1,2,3]}

This could then be passed into ``json.loads()`` or similar.

Usage
-----

Currently, ``jsonesque`` exposes just a single function called ``process()``. It
takes one argument — a JSON-like string — and returns a new string with the
aforementioned enhanced features removed. The string is additionally stripped of
extra white-space (minified).

To use ``jsonesque``, simply ``import jsonesque`` and call ``process()`` on your
string:

::

    import json, jsonesque

    invalid_json = '[1, 2, /* comment */ 3,]'
    valid_json   = jsonesque.process(invalid_json) # Yields string: '[1,2,3]'
    decoded      = json.loads(valid_json)          # Yields list:   [1, 2, 3]

More information
----------------

For the most complete and up-to-date documentation, please refer to the
``jsonesque`` GitHub repository: https://github.com/okdana/jsonesque/
