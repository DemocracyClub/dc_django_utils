### DC utils - Common functionality for all DC products

*The scope of this repo is "anything that all DC projects might use". It doesn't contain styles (that's the design system's job), but it will contain helpers for outputting HTML in the way the design system wants (e.g, form helpers).* 

### This project will contain:
 
Javascript helpers, including jQuery
A django app containing templates and form helpers
It's designed to make managing the front end of DC projects easy and consistent

TO DO: 
- Other common utils  
- Common testing helpers
- View mixins
- Running some smoke tests on CI
- Create Install docs

### Usage
To use this project in your django project: 

# In your `settings.py`:

`from dc_utils.settings.pipeline import *`

Add `dc_utils` to your `INSTALLED_APPS`

# Add the following to your main `urls.py`

`handler500 = "dc_utils.urls.dc_server_error"`

`if settings.DEBUG:`
    `from dc_utils.urls import dc_utils_testing_patterns`
    `urlpatterns += dc_utils_testing_patterns`
# Add the following line (with the version) to `requirements.txt':
`git+https://github.com/DemocracyClub/dc_django_utils.git@[hash]`
