# coding: utf-8

# $Id: $
from copy import deepcopy
import os
from tempfile import TemporaryFile
from unittest import TestCase, skipIf
import sys
import unittest
import datetime
from StringIO import StringIO

import clover


clover_module_file = clover.__file__


class AssetsMixin(object):
    """ helper for computing absolute path to assets. """

    def setUp(self):
        super(AssetsMixin, self).setUp()
        project_root = os.path.dirname(__file__)
        self.assets_dir = os.path.join(project_root, 'assets')


class OpenHelperTestCase(AssetsMixin, TestCase):
    """ Testing open file helper function. """

    def setUp(self):
        super(OpenHelperTestCase, self).setUp()
        self.filename = os.path.join(self.assets_dir, 'coverage.xml')

    def assertOpenFileOK(self, filename):
        try:
            with open(filename) as g:
                f = clover.open_file(filename)
                self.assertEqual(f.read(), g.read())
        finally:
            f.close()

    def test_open_str(self):
        self.assertOpenFileOK(self.filename)

    @skipIf(sys.version_info[0] != 2, "test is not for PY2")
    def test_open_unicode_py2(self):
        self.assertOpenFileOK(unicode(self.filename))

    @skipIf(sys.version_info[0] == 2, "test is not for PY3")
    def test_open_bytes_py3(self):
        self.assertOpenFileOK(bytes(self.filename, encoding='utf-8'))

    def test_open_stdin(self):
        try:
            f = clover.open_file(sys.stdin)
            self.assertIs(f, sys.stdin)
        finally:
            f.close()

    def test_open_fd(self):
        with open(self.filename) as g:
            try:
                f = clover.open_file(g)
                self.assertIs(f, g)
            finally:
                f.close()


class CoberturaTestCase(AssetsMixin, TestCase):
    """ Testing opening of coverage report."""

    def setUp(self):
        super(CoberturaTestCase, self).setUp()
        self.c = clover.Cobertura()
        self.filename = os.path.join(self.assets_dir, 'coverage.xml')

    def testOpenCoverage(self):
        self.c.open(self.filename)
        cdata = deepcopy(self.c.__dict__)
        packages = cdata.pop('packages')
        package = deepcopy(packages.values()[0].__dict__)

        with open(__file__.replace('.pyc', '.py')) as f:
            tests_loc = len(f.readlines())

        with open(clover_module_file.replace('.pyc', '.py')) as f:
            clover_loc = len(f.readlines())

        loc = tests_loc + clover_loc

        expected = {
            'classes': 0,
            'conditions': 0,
            'covered_conditions': 0,
            'covered_statements': 0,
            'files': 2,
            'loc': loc,
            'ncloc': 2,
            'statements': 2,
            'version': '3.7.1'
        }
        cdata.pop('timestamp')
        self.assertDictEqual(cdata, expected)

        expected = {
            'loc': loc,
            'statements': 2,
            'name': '',
            'ncloc': 2,
            'covered_conditions': 0,
            'conditions': 0,
            'covered_statements': 0
        }

        classes = package.pop('classes')

        self.assertDictEqual(package, expected)

        clover = deepcopy(classes['clover/__init__'].__dict__)

        expected = {
            'loc': clover_loc,
            'statements': 1,
            'name': 'clover/__init__',
            'filename': 'clover/__init__.py',
            'ncloc': 1,
            'covered_conditions': 0,
            'conditions': 0,
            'covered_statements': 0
        }

        self.assertDictEqual(clover, expected)

    def testWriteClover(self):
        with TemporaryFile() as tmp:
            self.c.open(self.filename)
            cl = clover.Clover(self.c)
            cl.export(tmp)
            tmp.seek(0)
            content = tmp.read()
            with open(os.path.join(self.assets_dir, 'clover.xml')) as g:
                self.assertEqual(content, g.read())


if __name__ == '__main__':
    unittest.main()
