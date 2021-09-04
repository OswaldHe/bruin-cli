from setuptools import setup, find_packages
from io import open
from os import path

import pathlib

CURDIRT = pathlib.Path(__file__).parent

README = (CURDIRT / "README.md").read_text()