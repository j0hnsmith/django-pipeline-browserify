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
            pipeline_settings.get('BROWSERIFY_VARS', ''),
            pipeline_settings.get('BROWSERIFY_BINARY', '/usr/bin/env browserify'),
            pipeline_settings.get('BROWSERIFY_ARGUMENTS', ''),
            infile,   
            outfile,
        )
        print('\ncommand:', command)
        return self.execute_command(command.split(), cwd=dirname(infile))
