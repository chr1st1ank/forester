# forester

This will be my collection of scripts for the linux shell. Currently I am onboarding them one by one. So come back in a couple of weeks.

[![codecov](https://codecov.io/gh/chr1st1ank/forester/branch/master/graph/badge.svg)](https://codecov.io/gh/chr1st1ank/forester)

## Usage

## Installation

## Setting up the development environment

First get a Python interpreter independent from system Python. [Pyenv](https://github.com/pyenv/pyenv) 
is a good choice for this:

    pip install pyenv
    pyenv install 3.7.5
    
Now activate the new interpreter and install [pipenv](https://github.com/pypa/pipenv) which is used to manage the 
project's dependencies:

    pyenv global 3.7.5
    pyenv exec pip install pipenv
    
Install the actual dependencies into a virtual environment and activate it:    
    
    pyenv exec pipenv install --dev --python 3.7.5
    pipenv shell

## Licence

The code in this repository is made available under the MIT license. Feel free to use, change and distribute it.
