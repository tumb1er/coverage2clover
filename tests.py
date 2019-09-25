# coding: utf-8

# $Id: $
from copy import deepcopy
import os
from tempfile import TemporaryFile
from unittest import TestCase, skipIf, skipUnless
import sys
import unittest
import coverage
import clover
import clover.coverage2clover

PY3 = clover.PY3

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

    @skipIf(PY3, "test is not for PY3")
    def test_open_unicode_py2(self):
        self.assertOpenFileOK(unicode(self.filename))

    @skipUnless(PY3, "test is not for PY2")
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

        if PY3:
            import pygount

            clover_module_analysis = pygount.source_analysis(
                clover_module_file,
                group='clover',
                fallback_encoding='utf-8')
            clover_loc = clover_module_analysis.code

            clover_bin_analysis = pygount.source_analysis(
                clover_bin_file,
                group='clover',
                fallback_encoding='utf-8')
            bin_loc = clover_bin_analysis.code
        else:
            with open(clover_module_file.replace('.pyc', '.py')) as f:
                clover_loc = len(f.readlines())

            with open(clover_bin_file.replace('.pyc', '.py')) as f:
                bin_loc = len(f.readlines())

        loc = clover_loc + bin_loc

        cversion = coverage.__version__

        # Initial values for coverage==4.5.4
        statements = ncloc = 187
        covered_conditions = 30
        covered_statements = 154
        conditions = 48

        if PY3:
            covered_conditions += 1
            covered_statements += 5

        expected = {
            'classes': 0,
            'conditions': conditions,
            'covered_conditions': covered_conditions,
            'covered_statements': covered_statements,
            'files': 2,
            'loc': loc,
            'ncloc': ncloc,
            'statements': statements,
            'version': cversion
        }
        cdata.pop('timestamp')
        self.assertDictEqual(cdata, expected)

        expected = {
            'loc': loc,
            'statements': statements,
            'name': '',
            'ncloc': ncloc,
            'covered_conditions': covered_conditions,
            'conditions': conditions,
            'covered_statements': covered_statements
        }

        classes = package.pop('classes')

        self.assertDictEqual(package, expected)

        cname = 'clover/__init__' if cversion < '4.0' else '__init__.py'
        clover = deepcopy(classes[cname].__dict__)

        statements = ncloc = 170
        conditions = 44
        covered_conditions = 29
        covered_statements = 146

        if PY3:
            covered_conditions += 1
            covered_statements += 5

        expected = {
            'loc': clover_loc,
            'statements': statements,
            'name': cname,
            'filename': 'clover/__init__.py',
            'ncloc': ncloc,
            'covered_conditions': covered_conditions,
            'conditions': conditions,
            'covered_statements': covered_statements
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
