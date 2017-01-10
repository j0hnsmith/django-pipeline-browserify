Django Pipeline Browserify
==========================

django-pipeline-browserify is a compiler for `django-pipeline <https://github.com/cyberdelia/django-pipeline>`_ (requires 16.9+). Making it really easy to use browserify with Django via pipeline.

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
        PIPELINE['BROWSERIFY_ARGS'] = ['-d']

Passing arguments as an array makes sure they are safely unambiguous, but the way browserify lets you pass nested arguments within brackets can make this very tedious::
    
    # this is very unreadable, and hard to maintain!
    PIPELINE['BROWSERIFY_ARGS'] = ['--transform', '[', 'babelify', '--presets', '[', 'es2015', 'react', ']', '--plugins', '[', 'transform-object-rest-spread', 'transform-class-properties', ']', ']']

To avoid this, when you know that no individual argument has a space within it, simply split the arguments yourself::

    # the easy way :-)
    PIPELINE['BROWSERIFY_ARGS'] = "--transform [ babelify --presets [ es2015 react ] --plugins [ transform-object-rest-spread transform-class-properties ] ]".split()


To set environment varaibles specific to the browserify command::

    PIPELINE['BROWSERIFY_ENV'] = {'NODE_ENV':'production'}

(Note that for an actual production build, this example is not sufficient. You'll probably want to use a transform like loose-envify so the minifier can optimize out debug statements. Browserify doesn't usually pass environment variables like that shown above into the compiled code; but it may effect the runtime behavior of browserify itself.)


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
