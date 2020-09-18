Coverage to Atlassian Clover conversion tool
============================================

A tool to convert python-coverage xml report to Atlassian Clover xml report 
format.

[![Build Status](https://github.com/tumb1er/coverage2clover/workflows/Build/badge.svg?branch=master&event=push)](https://github.com/tumb1er/coverage2clover/actions?query=event%3Apush+branch%3Amaster+workflow%3ABuild)
[![PyPI version](https://badge.fury.io/py/coverage2clover.svg)](http://badge.fury.io/py/coverage2clover)
[![Python Versions](https://img.shields.io/pypi/pyversions/coverage2clover.svg)](https://pypi.python.org/pypi/coverage2clover)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Usage
-----
```sh
pip install coverage2clover

coverage2clover < coverage.xml > clover.xml
coverage2clover -i coverage.xml -o clover.xml
```


