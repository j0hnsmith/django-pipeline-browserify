Django Pipeline Browserify
==========================

django-pipeline-browserify is a compiler for `django-pipeline <https://github.com/cyberdelia/django-pipeline>`_. Making it really easy to use browserify with Django via pipeline.

To install it::

    sudo npm install -g browserify
    pip install django-pipeline-browserify

And add it as a compiler to pipeline in your django `settings.py`::

    PIPELINE = {
        # ...
        'COMPILERS': ('pipeline_browserify.compiler.BrowserifyCompiler', ),
        # ...
    )

To add source maps during development (or any other browserify args)::

    if DEBUG:
        PIPELINE['BROWSERIFY_ARGUMENTS'] = '-d'

To add variable assignments before the browserify command::

    PIPELINE['BROWSERIFY_VARS'] = 'NODE_ENV=production'

**Important:** give your entry-point file a `.browserify.js` extension::

    PIPELINE = {
        # ...
        'javascript':{
            'browserify': {
                'source_filenames' : (
                    'js/entry-point.browserify.js',
                ),
                'output_filename': 'js/entry-point.js',
            },
        }
    }

To suggest a feature or report a bug:
https://github.com/j0hnsmith/django-pipeline-browserify/issues
