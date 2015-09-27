#!/usr/bin/env bash
coverage run --branch --source=`pwd`/clover tests.py
coverage xml
mv coverage.xml assets

coverage2clover < assets/coverage.xml > assets/clover.xml
