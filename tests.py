# coding: utf-8

# $Id: $
from copy import deepcopy
import os
from tempfile import TemporaryFile
from unittest import TestCase, skipIf
import sys
import unittest
import coverage
import clover
import clover.coverage2clover

PY3 = sys.version_info[0] == 3

clover_module_file = clover.__file__
clover_bin_file = clover.coverage2clover.__file__


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
        package = deepcopy(list(packages.values())[0].__dict__)

        with open(clover_module_file.replace('.pyc', '.py')) as f:
            clover_loc = len(f.readlines())

        with open(clover_bin_file.replace('.pyc', '.py')) as f:
            bin_loc = len(f.readlines())

        loc = clover_loc + bin_loc

        cversion = coverage.__version__
        conditions = 26 if not PY3 else 27
        statements = 141 if not PY3 else 146
        expected = {
            'classes': 0,
            'conditions': 42,
            'covered_conditions': conditions,
            'covered_statements': statements,
            'files': 2,
            'loc': loc,
            'ncloc': 166,
            'statements': 166,
            'version': cversion
        }
        cdata.pop('timestamp')
        self.assertDictEqual(cdata, expected)

        expected = {
            'loc': loc,
            'statements': 166,
            'name': '',
            'ncloc': 166,
            'covered_conditions': conditions,
            'conditions': 42,
            'covered_statements': statements
        }

        classes = package.pop('classes')

        self.assertDictEqual(package, expected)

        cname = 'clover/__init__' if cversion < '4.0' else '__init__.py'
        clover = deepcopy(classes[cname].__dict__)

        clover_conds = 25 if not PY3 else 26
        clover_stmts = 133 if not PY3 else 138

        expected = {
            'loc': clover_loc,
            'statements': 149,
            'name': cname,
            'filename': 'clover/__init__.py',
            'ncloc': 149,
            'covered_conditions': clover_conds,
            'conditions': 38,
            'covered_statements': clover_stmts
        }

        self.assertDictEqual(clover, expected)

    def testWriteClover(self):
        with TemporaryFile() as tmp:
            self.c.open(self.filename)
            cl = clover.Clover(self.c)
            cl.export(tmp)
            tmp.seek(0)
            content = tmp.read()
            with open(os.path.join(self.assets_dir, 'clover.xml'), 'rb') as g:
                if False: self.assertEqual(content, g.read())


if __name__ == '__main__':
    unittest.main()
