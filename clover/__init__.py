# coding: utf-8

from datetime import datetime
from xml.etree import ElementTree as ET
import re
import subprocess
import sys

__all__ = ['Cobertura', 'Clover']


if sys.version_info[0] == 2:
    # For python < 3.x
    is_file = lambda x: isinstance(x, file)

    def open_file(file_or_name, mode='r'):
        if is_file(file_or_name):
            # file descriptor already opened
            return file_or_name

        if isinstance(file_or_name, (str, unicode)):
            # open filename and return FD
            return open(file_or_name, mode)

        raise ValueError("Invalid agrument")

else:
    # For python >= 3.x
    import io
    is_file = lambda x: isinstance(x, io.IOBase)

    def open_file(file_or_name, mode='r'):
        if is_file(file_or_name):
            # file descriptor already opened
            return file_or_name

        if isinstance(file_or_name, (bytes, str)):
            # open filename and return FD
            return open(file_or_name, mode)

        raise ValueError("Invalid agrument")


class Package(object):

    def __init__(self, name):
        self.name = name
        self.statements = 0
        self.classes = {}
        self.statements = 0
        self.covered_statements = 0
        self.conditions = 0
        self.covered_conditions = 0
        self.loc = 0
        self.ncloc = 0

    def add_class(self, c):
        self.classes[c.name] = c
        self.statements += c.statements
        self.covered_statements += c.covered_statements
        self.conditions += c.conditions
        self.covered_conditions += c.covered_conditions
        self.loc += c.loc
        self.ncloc += c.ncloc


class Class(object):

    def __init__(self, name, filename, statements, covered_statements,
                 conditions, covered_conditions):
        self.name = name
        self.filename = filename
        self.statements = statements
        self.covered_statements = covered_statements
        self.conditions = conditions
        self.covered_conditions = covered_conditions
        self.ncloc = statements

    def count_loc(self):
        output = subprocess.check_output(['wc', '-l', self.filename])
        m = re.match(b'^[\s]*([\d]+).*', output)
        self.loc = int(m.group(1))


class Cobertura(object):
    """ XML-parser for coverage.py xml report."""

    def __init__(self):
        self.loc = 0
        self.ncloc = 0
        self.files = 0
        self.packages = {}
        self.classes = 0
        self.statements = 0
        self.covered_statements = 0
        self.conditions = 0
        self.covered_conditions = 0

    def add_package(self, p):
        self.packages[p.name] = p
        self.statements += p.statements
        self.covered_statements += p.covered_statements
        self.conditions += p.conditions
        self.covered_conditions += p.covered_conditions
        self.files += len(p.classes)
        self.loc += p.loc
        self.ncloc += p.ncloc

    def open(self, file_like_object):
        f = open_file(file_like_object, 'r')
        root = ET.parse(f).getroot()
        f.close()
        timestamp = float(root.get('timestamp') or 0) / 1000
        self.timestamp = datetime.fromtimestamp(timestamp)
        self.version = root.get('version') or ''
        for package in root.iter('packages'):
            name = package.get('name') or ''
            p = Package(name)
            for class_info in package.iter('class'):
                name = class_info.get('name')
                filename = class_info.get('filename')
                statements = 0
                covered_statements = 0
                conditions = 0
                covered_conditions = 0
                for line in class_info.iter('line'):
                    statements += 1
                    if line.get('hits') == '1':
                        covered_statements += 1
                    if line.get('branch') == 'true':
                        cc = line.get('condition-coverage')
                        m = re.match(r'([\d]+)%[\s]+\(([\d]+)/([\d]+)\)', cc)
                        conditions += int(m.group(3))
                        covered_conditions += int(m.group(2))

                c = Class(name, filename, statements, covered_statements,
                          conditions, covered_conditions)
                c.count_loc()
                p.add_class(c)
            self.add_package(p)


class Clover(object):
    def __init__(self, coverage):
        self.c = coverage
        self.autoclose = True

    def export(self, file_like_object):
        if is_file(file_like_object):
            self.autoclose = False
        generated = self.c.timestamp.strftime('%d-%m-%y')
        root = ET.Element('coverage', generated=generated, clover=self.c.version)
        project = ET.Element('project', timestamp=generated)
        root.append(project)
        covered_elements = self.c.covered_statements + self.c.covered_conditions
        project_metrics = ET.Element(
            'metrics',
            packages=str(len(self.c.packages)),
            elements=str(self.c.statements + self.c.conditions),
            coveredelements=str(covered_elements),
            statements=str(self.c.statements),
            coveredstatements=str(self.c.covered_statements),
            conditionals=str(self.c.conditions),
            coveredconditionals=str(self.c.covered_conditions),
            files=str(self.c.files),
            loc=str(self.c.loc),
            ncloc=str(self.c.ncloc))
        project.append(project_metrics)
        classes = 0
        for pname in sorted(self.c.packages.keys()):
            p = self.c.packages[pname]
            package = ET.Element('package', name=p.name)
            project.append(package)
            covered_elements = p.covered_statements + p.covered_conditions
            metrics = ET.Element(
                'metrics',
                elements=str(p.statements + p.conditions),
                coveredelements=str(covered_elements),
                statements=str(p.statements),
                coveredstatements=str(p.covered_statements),
                conditionals=str(p.conditions),
                coveredconditionals=str(p.covered_conditions),
                files=str(len(p.classes)),
                classes=str(len(p.classes)),
                loc=str(p.loc),
                ncloc=str(p.ncloc))
            package.append(metrics)
            for cname in sorted(p.classes.keys()):
                classes += 1
                c = p.classes[cname]
                covered_elements = c.covered_statements + c.covered_conditions
                class_info = ET.Element('class', name=c.name, filename=c.filename)
                package.append(class_info)
                metrics = ET.Element(
                    'metrics',
                    elements=str(c.statements + c.conditions),
                    coveredelements=str(covered_elements),
                    statements=str(c.statements),
                    coveredstatements=str(c.covered_statements),
                    conditionals=str(c.conditions),
                    coveredconditionals=str(c.covered_conditions),
                    files='1',
                    loc=str(c.loc),
                    ncloc=str(c.ncloc))
                class_info.append(metrics)
        project_metrics.set('classes', str(classes))

        self.write_clover(root, file_like_object)

    def write_clover(self, root, file_like_object):
        f = open_file(file_like_object, 'w')
        if sys.version_info[0] == 2:
            ET.ElementTree(root).write(f, encoding='utf-8', xml_declaration=True)
        else:
            import io
            b = io.BytesIO()
            ET.ElementTree(root).write(b, encoding='utf-8', xml_declaration=True)
            if 'b' not in f.mode:
                f.write(b.getvalue().decode("utf-8"))
            else:
                f.write(b.getvalue())
        if self.autoclose:
            f.close()
