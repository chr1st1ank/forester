# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method before making a change. 


## Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a 
   build.
2. Update the README.md with details of changes to the interface, this includes new command line parameters, environment 
   variables etc.
3. Make sure to add tests for your changes and make sure thes tests run fast. All tests have to pass before the pull
   request can be merged.
4. Be aware that with your code changes you submit your work to the licensing of this project. So make sure you don't 
   copy in other people's work with an incompatible licensing (e.g. you can't copy work under GPL into a MIT licensed
   project without breaking the copyleft restriction).


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
