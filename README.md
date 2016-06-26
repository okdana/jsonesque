# jsonesque

`jsonesque` is a module for processing JSON-like strings into valid, minified
JSON. It enables a Python application to support an 'enhanced' form of JSON that
contains comments and trailing commas.

For example, given the following JSON-like input:

```
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
```

`jsonesque` would produce the following valid JSON:

```
{"a":1,"b":2,"c":[1,2,3]}
```

This could then be passed into `json.loads()` or similar.

## Usage

Currently, `jsonesque` exposes just a single function called `process()`. It
takes one argument — a JSON-like string — and returns a new string with the
aforementioned enhanced features removed. The string is additionally stripped of
extra white-space (minified).

To use `jsonesque`, simply `import jsonesque` and call `process()` on your
string:

```python
import json, jsonesque

invalid_json = '[1, 2, /* comment */ 3,]'
valid_json   = jsonesque.process(invalid_json) # Yields string: '[1,2,3]'
decoded      = json.loads(valid_json)          # Yields list:   [1, 2, 3]
```

`jsonesque` is smart enough that it won't break on the contents of strings (for
example, it correctly handles input like `{ "//": "/* foo */" }`). However, it
*does not* attempt validation — all it does is strip any comments and trailing
commas it finds, optimistically assuming that the rest of the input is valid.
This means that any other instances of invalid JSON, like single-quotes instead
of double-quotes, consecutive commas without a value in an array/object, and so
on will make it through the `process()` call and will break whatever you pass
the result into.

## Dependencies and compatibility

`jsonesque` doesn't depend on anything outside the stdlib. It should run on any
version of Python 2 (>= 2.2) or Python 3.

## Installing, building, and testing

If possible, you should install the package from PyPI using `pip` or `pip3`:

```
pip install jsonesque
```

If you need to build from source, simply check out the repo and run `make`
and/or `make install`. To run the unit tests, run `make test`. If you're on
Python 2 and the `make` commands don't work, you can use `python ./setup.py`
instead.

## Credits and licence

`jsonesque` is heavily based on (i.e., a fork of)
[JSON.minify](https://github.com/getify/JSON.minify/tree/python). Like
JSON.minify, it is available under the [MIT licence](LICENCE).

## See also

There are a handful of similar projects i found before i started working on
this one, all of which have their own advantages and disadvantages:

* [JSON.minify](https://github.com/getify/JSON.minify/tree/python) —
  Slightly faster; doesn't support Python-style comments, doesn't support
  trailing commas, isn't available in PyPI
* [Hjson](https://github.com/laktak/hjson-py/) —
  Extremely featureful, well maintained; just over-kill for my purposes
* [json-comment](https://bitbucket.org/Dando_Real_ITA/json-comment) —
  Probably faster (doesn't use regular expressions), supports INI-style comments
  and Python-style multi-line strings; doesn't support single-line C-style
  comments or in-line C-style comments, uses an extremely naïve parsing method,
  doesn't seem to be maintained
* [commentjson](https://github.com/vaidik/commentjson) —
  Provides complete re-implementations of `json.*` functions; possibly slower
  due to heavier use of regular expressions, doesn't support multi-line/in-line
  C-style comments, doesn't support trailing commas

