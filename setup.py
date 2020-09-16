from setuptools import setup

setup(
    name="coverage2clover",
    version="3.0.0",
    packages=["clover"],
    url="http://github.com/tumb1er/coverage2clover",
    license="Beer License",
    entry_points={"console_scripts": ["coverage2clover = clover.coverage2clover:main"]},
    author="tumbler",
    author_email="zimbler@gmail.com",
    description="A tool to convert python-coverage xml report to Atlassian Clover xml report format",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Text Processing :: Markup :: XML",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
    ],
    install_requires=["coverage==5.3", "pygount==1.2.4"],
)
