#!/usr/bin/env python

# coding: utf-8

from optparse import OptionParser
import sys

from clover import Cobertura, Clover


# Transforms coverage.py xml report to
# Atlassian Clover xml report format


parser = OptionParser()
parser.add_option("-i", "--input-file", dest="inputfile", default=None,
                  help="read coverage report from FILE", metavar="FILE")
parser.add_option("-o", "--output-file", dest="outputfile", default=None,
                  help="write clover report to FILE", metavar="FILE")


def main(*args, **options):
    if not args:
        options, args = parser.parse_args()
    inputfile = options.inputfile or sys.stdin
    outputfile = options.outputfile or sys.stdout
    cov = Cobertura()
    cov.open(inputfile)
    cl = Clover(cov)
    cl.export(outputfile)


if __name__ == '__main__':
    main()
