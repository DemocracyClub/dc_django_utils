import os

root_path = os.path.dirname(os.path.abspath(__file__))

STATICFILES_STORAGE = "dc_utils.storages.StaticStorage"

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "pipeline.finders.CachedFileFinder",
    "pipeline.finders.PipelineFinder",
    "pipeline.finders.ManifestFinder",
)

SASS_INCLUDE_PATHS = [root_path]


def build_sass_args(extra_include_paths):
    paths = SASS_INCLUDE_PATHS + extra_include_paths
    args = ["-I " + p for p in paths]
    args.append("--style compressed")
    args.append("--sourcemap")
    return " ".join(args)


DEFAULT_PIPELINE = {
    "COMPILERS": ("pipeline.compilers.sass.SASSCompiler",),
    "SASS_BINARY": "sassc",
    "SASS_ARGUMENTS": build_sass_args(SASS_INCLUDE_PATHS),
    "CSS_COMPRESSOR": "pipeline.compressors.NoopCompressor",
    "STYLESHEETS": {
        "styles": {
            "source_filenames": [],
            "output_filename": "css/styles.css",
            "extra_context": {
                "media": "screen,projection,print",
            },
        },
    },
    "JS_COMPRESSOR": "pipeline.compressors.jsmin.JSMinCompressor",
    "JAVASCRIPT": {
        "scripts": {
            "source_filenames": [],
            "output_filename": "js/scripts.js",
        }
    },
}


def get_pipeline_settings(
    extra_css=None, extra_js=None, extra_include_paths=None
):
    PIPELINE = DEFAULT_PIPELINE
    if extra_include_paths:
        PIPELINE["SASS_ARGUMENTS"] = build_sass_args(extra_include_paths)
    if extra_css:
        PIPELINE["STYLESHEETS"]["styles"]["source_filenames"] += extra_css
    if extra_js:
        PIPELINE["JAVASCRIPT"]["scripts"]["source_filenames"] += extra_js
    return PIPELINE
