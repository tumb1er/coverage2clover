#!/usr/bin/env bash
coverage -x tests.py
coverage xml
mv coverage.xml assets

coverage2clover < assets/coverage.xml > assets/clover.xml
