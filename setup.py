import os
from setuptools import setup, find_packages
from openbudget import __version__


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="openbudget",
    version=__version__,
    url="https://github.com/hp0404/openbudget-api.git",
    author="Hryhorii Pavlenko",
    author_email="hryhorii.pavlenko@gmail.com",
    description="Openbudget API wrapper",
    long_description=get_long_description(),
    packages=find_packages(),
)
