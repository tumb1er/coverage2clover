#!/usr/bin/env bash
coverage -x tests.py
coverage xml
mv coverage.xml assets

PYTHONPATH=$PYTHONPATH:. python bin/coverage2clover.py < assets/coverage.xml > assets/clover.xml
