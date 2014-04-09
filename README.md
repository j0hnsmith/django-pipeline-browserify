Django Pipeline Browserify
==========================

django-pipeline-browserify is a compiler for [django-pipeline](https://github.com/cyberdelia/django-pipeline). Making it really easy to use browserify with Django via pipeline.

To install it :

    sudo npm install -g browserify
    pip install django-pipeline-browserify

And add it as a compiler to pipeline in your django `settings.py`.

	PIPELINE_COMPILERS = (
	    'pipeline_browserify.compiler.BrowserifyCompiler',
    )

To add source maps during development (or any other browserify args)

    if DEBUG:
        PIPELINE_BROWSERIFY_ARGUMENTS = '-d'

__Important:__ give your entry-point file a `.browserify.js` extension (required).

    PIPELINE_JS = {
        'browserify': {
            'source_filenames': (
                'js/entry-point.browserify.js',
            ),
            'output_filename': 'js/browserified.js',
        },
    }

To suggest a feature or report a bug :
<https://github.com/j0hnsmith/django-pipeline-browserify/issues>
