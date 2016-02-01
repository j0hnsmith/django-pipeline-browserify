from pipeline.compilers import SubProcessCompiler
from os.path import dirname
from django.conf import settings


class BrowserifyCompiler(SubProcessCompiler):
    output_extension = 'browserified.js'

    def match_file(self, path):
        print('\nmatching file:', path)
        return path.endswith('.browserify.js')

    def compile_file(self, infile, outfile, outdated=False, force=False):
        if not force and not outdated:
            # File doesn't need to be recompiled
            return
        pipeline_settings = getattr(settings, 'PIPELINE', {})
        command = "%s %s %s %s -o %s" % (
            pipeline_settings['BROWSERIFY_VARS'] if 'BROWSERIFY_VARS' in pipeline_settings else '',
            pipeline_settings['BROWSERIFY_BINARY'] if 'BROWSERIFY_BINARY' in pipeline_settings else '/usr/bin/env browserify',
            pipeline_settings['BROWSERIFY_ARGUMENTS'] if 'BROWSERIFY_ARGUMENTS' in pipeline_settings else '',
            infile,   
            outfile,
        )
        print('\ncommand:', command)
        return self.execute_command(command.split(), cwd=dirname(infile))
