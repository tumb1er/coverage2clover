#!/usr/bin/env bash
coverage run --source=`pwd` --omit=`pwd`/setup.py tests.py
coverage xml
mv coverage.xml assets

coverage2clover < assets/coverage.xml > assets/clover.xml
