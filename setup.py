from setuptools import setup

setup(
    name="coverage2clover",
    version="2.0.1",
    packages=["clover"],
    url="http://github.com/tumb1er/coverage2clover",
    license="Beer License",
    entry_points={"console_scripts": ["coverage2clover = clover.coverage2clover:main"]},
    author="tumbler",
    author_email="zimbler@gmail.com",
    description="A tool to convert python-coverage xml report to Atlassian Clover xml report format",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Text Processing :: Markup :: XML",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
    ],
    install_requires=["coverage", "pygount"],
)
