from distutils.core import setup
from shutil import copy

try:
    copy("bin/coverage2clover.py", "bin/coverage2clover")
except (OSError, IOError):
    pass

setup(
    name='coverage2clover',
    version='1.0',
    packages=['clover'],
    scripts=["bin/coverage2clover"],
    url='http://github.com/tumb1er/coverage2clover',
    license='Beer License',
    author='tumbler',
    author_email='zimbler@gmail.com',
    description='A tool to convert python-coverage xml report to Atlassian Clover xml report format'
)
