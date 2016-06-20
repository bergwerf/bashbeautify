the Bash Script Beautifier
==========================
[![Build Status](https://travis-ci.org/hermanbergwerf/bashbeautify.svg?branch=master)](https://travis-ci.org/hermanbergwerf/bashbeautify/)

This is a wrapper of the Bash Script Beautifier by Paul Lutus for pip, the
Python Package index. The Bash Script Beautifier is a beautifier for Bash shell
scripts written in Python. I do not own any copyrights of this code, the
original copyright notice is unchanged, see:
http://arachnoid.com/python/beautify_bash_program.html.

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
