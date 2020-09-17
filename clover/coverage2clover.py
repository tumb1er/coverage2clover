#!/usr/bin/env python
import sys
from argparse import ArgumentParser

from clover import Cobertura, Clover

# Transforms coverage.py xml report to
# Atlassian Clover xml report format

parser = ArgumentParser()
parser.add_argument(
    "-i",
    "--input-file",
    dest="inputfile",
    default=None,
    help="read coverage report from FILE",
    metavar="FILE",
)
parser.add_argument(
    "-o",
    "--output-file",
    dest="outputfile",
    default=None,
    help="write clover report to FILE",
    metavar="FILE",
)


def main(*args):
    if not args:
        args = parser.parse_args()
    inputfile = args.inputfile or sys.stdin
    outputfile = args.outputfile or sys.stdout
    cov = Cobertura()
    cov.open(inputfile)
    cl = Clover(cov)
    cl.export(outputfile)


if __name__ == "__main__":
    main()
