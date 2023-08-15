# Memprize prototype team Radboudumc

Reimplementation of the [submission for the memprize competition 2016/2017](https://www.psychologicalscience.org/publications/observer/obsonline/radboud-university-researchers-win-first-memrise-prize.html) organized by
[memrise](https://www.memrise.com).

The repository contains two versions of the experiment backing the submission:

1. The original Psychopy implementation, but updated to Python3 and using the
    newest Psychopy 2023.02.0 release.
2. A web-implementation of the same algorithm that can run in the browser.

## Web version

...

## The original Psychopy version

(Dutch only)

![Example of the psychopy version](doc/psychopy-screenshot1.png)

The original version of the experiment for testing the spacing algorithm.

## Steps for running

Required software:

- python 3.10 (or higher)
- [`pipenv` for Python](https://pypi.org/project/pipenv/)

With these packages installed:

- Clone the repository
- Change in the directory `psychopy`
- If you are using a python-version other than 3.10, edit the `Pipfile` and
  replace the version string 3.10 with the version you are using.
- Issue the command `pipenv install`
  - This _should_ install PsychoPy in a pipenv-environment. However, PsychoPy
    is a relatively heavy package with a lot of dependencies and might be more
    complicated to install on your system. If you encounter errors, try the
    alternative steps below.
- Now you can run the application using the command:

~~~~~~~~~.sh
pipenv run python main.py 
~~~~~~~~~

## Alternative steps for running

These steps are easier in case you are not able to install PsychoPy using the
steps above. These steps will run the program through a pre-built Standalone
PsychoPy bundle instead.

Note: These steps do not work on Linux and were only tested on Windows!

Required software:

- Install [PsychoPy](https://www.psychopy.org/) version 2023.02.0 in some other way
  - You sould be able to download the exact version from the release page:
  https://github.com/psychopy/psychopy/releases/tag/2023.2.0

Then:

- Clone the repository
- Change in the directory `psychopy`
