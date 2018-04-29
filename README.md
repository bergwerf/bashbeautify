the Bash Script Beautifier
==========================
[![Build Status](https://travis-ci.org/bergwerf/bashbeautify.svg?branch=master)](https://travis-ci.org/bergwerf/bashbeautify/)
[![PyPI](https://img.shields.io/pypi/v/bashbeautify.svg?maxAge=2592000)](https://pypi.python.org/pypi/bashbeautify)

This is a wrapper of the Bash Script Beautifier by Paul Lutus for PyPI, the
Python Package Index. The Bash Script Beautifier is a beautifier for Bash shell
scripts. I do not own any copyrights of this code, the original copyright notice
is unchanged, see: http://arachnoid.com/python/beautify_bash_program.html.

I am currently not able to patch bugs in this program. Any contributions are
welcome. A testing system is in place (see `./test`).

Install
-------
```
pip install --upgrade bashbeautify
```

Use
---
Beautify a single Bash file.
```
bashbeautify file.sh
```

Beautify all Bash files in a directory (or in other words, you can use globs).
```
bashbeautify *.sh
```

Or send a string to BashBeautify.
```
bashbeautify - < input.sh > output.sh
```
