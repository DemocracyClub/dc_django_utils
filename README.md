# DC utils - Common functionality for all DC products

*The scope of this repo is "anything that all DC projects might use". It doesn't contain styles (that's the design system's job), but it will contain helpers for outputting HTML in the way the design system wants (e.g, form helpers).* 

### This project will contain:
 
A django app containing templates and form helpers
It's designed to make managing the front end of DC projects easy and consistent

TO DO: 
- Other common utils  
- Common testing helpers
- View mixins
- Base template with common structure

### Usage
To use this project in your django project: 

## In your `settings.py`:

`from dc_utils.settings.pipeline import *`

Add `dc_utils` to your `INSTALLED_APPS`

## Add the following to your main `urls.py`

`handler500 = "dc_utils.urls.dc_server_error"`

`if settings.DEBUG:`
    `from dc_utils.urls import dc_utils_testing_patterns`
    `urlpatterns += dc_utils_testing_patterns`
## Add the following line with the [latest version](https://github.com/DemocracyClub/dc_django_utils/releases) to `requirements.txt':
`git+https://github.com/DemocracyClub/dc_django_utils.git@[hash]`

## Local Development
Install the dev dependencies:

    pip install -r requirements/dev.txt

This project uses [pre-commit](https://pre-commit.com/#quick-start) to run `black` and `djhtml` before each commit. To enable this, after installing the dev dependencies run:

    pre-commit install

# Test your changes in another product which uses  `dc_utils` as a dependency

While in your product directory, run:
 `pip install -e /path/to/locations/repo` (with the local path location to `dc_utils`)

This will overwrite the directory in site-packages with a symbolic link to the locations repository, meaning any changes to code in there will automatically be reflected - just reload the page (so long as you're using the development server).
## New Release
Once a PR (or a set of PRs) is merged: 

1. Update version in `dc_utils/__init__.py` (commit and push to main, or do it in the github interface).
2. Draft a new release [here](https://github.com/DemocracyClub/dc_django_utils/releases). Make sure to create a new tag and name (both should just be the version number). 
3. Update versions number in `base.py` in related repos. At the time of writing this is WCIVF, DC Website and WDIV. 
