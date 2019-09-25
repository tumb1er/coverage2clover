import sys
from setuptools import setup

PY3 = sys.version_info[0] == 3

install_requires = ['coverage']
if PY3:
    install_requires.append('pygount')

setup(
    name='coverage2clover',
    version='1.4.0',
    packages=['clover'],
    url='http://github.com/tumb1er/coverage2clover',
    license='Beer License',
    entry_points={
        'console_scripts': [
            'coverage2clover = clover.coverage2clover:main'
        ]
    },
    author='tumbler',
    author_email='zimbler@gmail.com',
    description='A tool to convert python-coverage xml report to Atlassian Clover xml report format',
    classifiers=['Development Status :: 4 - Beta',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Topic :: Text Processing :: Markup :: XML',
                 'Topic :: Software Development :: Quality Assurance',
                 'Topic :: Software Development :: Testing'],
    install_requires=install_requires,
)
