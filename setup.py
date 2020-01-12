import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


setup(
    name="forester",
    version="0.5.0",
    url="https://github.com/chr1st1ank/forester",
    license='MIT',

    author="chr1st1ank",
    author_email="chr1st1ank@pferdeplan.de",

    description="Shell scripts for nursing a linux machine",
    long_description=read("README.rst"),

    packages=find_packages(exclude=('tests',)),

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

    entry_points={
        'console_scripts': [
            'forester = forester.cli:call_main',
        ],
    }
)
