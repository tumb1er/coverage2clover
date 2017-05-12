Coverage to Atlassian Clover conversion tool
============================================

A tool to convert python-coverage xml report to Atlassian Clover xml report 
format.

[![Build Status](https://travis-ci.org/tumb1er/coverage2clover.svg?branch=master)](https://travis-ci.org/tumb1er/coverage2clover)
[![PyPI version](https://badge.fury.io/py/coverage2clover.svg)](http://badge.fury.io/py/coverage2clover)
[![Python Versions](https://img.shields.io/pypi/pyversions/coverage2clover.svg)](https://pypi.python.org/pypi/coverage2clover)

Usage
-----
```sh
pip install coverage2clover

coverage2clover < coverage.xml > clover.xml
coverage2clover -i coverage.xml -o clover.xml
```


