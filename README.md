# DC utils - Common functionality for all DC products

*The scope of this repo is "anything that all DC projects might use". It doesn't contain styles (that's the design system's job), but it will contain helpers for outputting HTML in the way the design system wants (e.g, form helpers).* 

### This project will contain:
 
A django app containing templates and form helpers.
It's designed to make managing the front end of DC projects easy and consistent.

Common templates include:

- `base_naked.html`: This template includes the basic html doc structure and template tags encasing details for open graph tags. Additional template tags for page titles, site css, site and page meta as well as body are included here. 
- `base.html`: This template includes content and template tags for the page body. Basic `dc_design_system` branding and page structure is included here - header, nav, footer - as well as template tags for js and google analytics tracking code. 
- Server Error (`500.html`) and Page Not Found (`404.html`): Using (Django's built-in views)[https://docs.djangoproject.com/en/4.0/ref/views/#the-404-page-not-found-view] for these templates breaks the static pipeline meaning we cannot rely on the base templates mentioned above and need repeat the basic template structure with absolute (rather than static) paths to branding assets. 

Common assets include those files found in `/static/..` and `/static/favicon` which are used in the base templates.
### Usage
To use this project in your django project: 

### In your `settings.py`:

`from dc_utils.settings.pipeline import *`

Add `dc_utils` to your `INSTALLED_APPS`

Add `dc_utils.context_processors.dc_django_utils` to your
`context_processors` list.

### Add the following to your main `urls.py`

`handler500 = "dc_utils.urls.dc_server_error"`

```py
if settings.DEBUG:
    from dc_utils.urls import dc_utils_testing_patterns
    urlpatterns += dc_utils_testing_patterns
```


### Add the following line with the [latest version](https://github.com/DemocracyClub/dc_django_utils/releases) to `requirements.txt':
`git+https://github.com/DemocracyClub/dc_django_utils.git@[hash]`

### Using the DS Link Widget 

 The DS Link Widget in [filter_widgets](dc_utils/filter_widgets.py) extends the Link Widget from django-filter in order to customize its html. Your project will therefore need to have [django-filter](https://github.com/carltongibson/django-filter) already installed if you want to use it.

### Basic auth middleware

If you want to hide your site behind HTTP Basic Auth, you can use the 
`BasicAuthMiddleware`:

In your `settings.py` add the following to `MIDDLEWARE`:

`"dc_utils.context_processors.dc_django_utils",`

By default this will be enabled if the `DC_ENVIRONMENT` environment variable 
is set to one of `staging` or `development`. If you want to enable it anyway,
set `BASIC_AUTH_ENABLED = True` in `settings.py`.

The default username and password is `dc`. This isn't meant to be secure (if 
you want to hide the site in a secure way, use a different authorization 
system!). 

If you want to change the default, you need to make a new header value. This 
is in the format of `Basic [base64 encoded username:password`. Use [this 
handy tool](https://www.debugbear.com/basic-auth-header-generator) to make 
the header. You need to include the `Basic ` part in the value.

Then set this to `BASIC_AUTH_VALUE` in `settings.py`.

#### Allow lists

There may be some paths that you never want to be behind HTTP Basic Auth.

In this case, create `settings.BASIC_AUTH_ALLOWLIST` as a list of strings.

The strings can contain wildcards, so for example `/foo/*` would allow 
access to every path under `/foo/`.


### Local Development
Install the dev dependencies:

    pip install -e .[dev]

This project uses [pre-commit](https://pre-commit.com/#quick-start) to run `black` and `djhtml` before each commit. To enable this, after installing the dev dependencies run:

`pre-commit install`

### Test your changes in another product which uses  `dc_django_utils` as a dependency

While in your product directory, run:
 `pip install -e /path/to/locations/repo` (with the local path location to `dc_django_utils`)

This will overwrite the directory in site-packages with a symbolic link to the locations repository, meaning any changes to code in there will automatically be reflected - just reload the page (so long as you're using the development server).
### New Release
Once a PR (or a set of PRs) is merged: 

1. Update version in `dc_utils/__init__.py` (commit and push to main, or do it in the github interface).
2. Draft a new release [here](https://github.com/DemocracyClub/dc_django_utils/releases). Make sure to create a new tag and name (both should just be the version number). 
3. Update versions number in `base.py` in related repos. At the time of writing this is WCIVF, DC Website and WDIV. 
