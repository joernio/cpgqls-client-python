import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
os.chdir(here)


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="cpgqls-client",
    version="0.0.8",
    author="ShiftLeft Inc.",
    author_email="claudiu@shiftleft.io",
    description="A client library for CPGQL servers",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/joernio/cpgqls-client-python",
    install_requires=[
        "requests>=2.25.1",
        "websockets>=9.1",
    ],
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
