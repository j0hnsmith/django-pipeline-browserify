from pipeline.compilers import SubProcessCompiler
from os.path import dirname
from django.conf import settings


class BrowserifyCompiler(SubProcessCompiler):
    output_extension = 'js'

    def match_file(self, path):
        print('\nmatching file:', path)
        return path.endswith('.browserify.js')

    def compile_file(self, infile, outfile, outdated=False, force=False):
        if not force and not outdated:
            # File doesn't need to be recompiled
            return
        pipeline_settings = getattr(settings, 'PIPELINE', {})
        command = "%s %s %s -o %s" % (
            getattr(pipeline_settings, 'BROWSERIFY_VARS', ''),
            getattr(pipeline_settings, 'BROWSERIFY_BINARY', '/usr/bin/env browserify'),
            getattr(pipeline_settings, 'BROWSERIFY_ARGUMENTS', ''),
            infile,   
        )
        print('\ncommand:', command)
        return self.execute_command(command.split(), cwd=dirname(infile))
