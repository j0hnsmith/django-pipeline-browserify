from pipeline.compilers import SubProcessCompiler
from os.path import dirname
import json
from django.conf import settings
from django.core.exceptions import SuspiciousFileOperation

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

    def is_outdated(self, infile, outfile):
        """Check if the input file is outdated.

        The difficulty with the default implementation is that any file that is
        `require`d from the entry-point file will not trigger a recompile if it
        is modified. This overloaded version of the method corrects this by generating
        a list of all required files that are also a part of the storage manifest
        and checking if they've been modified since the last compile.

        The command used to generate the list of dependencies is the same as the compile
        command but includes the `--deps` option.

        WARNING: It seems to me that just generating the dependencies may take just
        as long as actually compiling, which would mean we would be better off just
        forcing a compile every time.
        """

        # Check for missing file or modified entry-point file.
        if super(BrowserifyCompiler, self).is_outdated(infile, outfile):
            return True

        # Check if we've already calculated dependencies.
        deps = getattr(self, '_deps', None)
        if not deps:

            # Collect dependency information.
            command = "%s %s %s --deps %s" % (
                getattr(settings, 'PIPELINE_BROWSERIFY_VARS', ''),
                getattr(settings, 'PIPELINE_BROWSERIFY_BINARY', '/usr/bin/env browserify'),
                getattr(settings, 'PIPELINE_BROWSERIFY_ARGUMENTS', ''),
                self.storage.path(infile),
            )
            dep_json = self.execute_command(command) #, cwd=dirname(infile))

            # Process the output data. It's JSON, and the file's path is coded
            # in the "file" field. We also want to save the content of each file
            # so we can check if they're outdated, which is coded under "source".
            deps = []
            for dep in json.loads(dep_json.decode()):

                # Is this file managed by the storage?
                try:
                    exists = self.storage.exists(dep['file'])
                except SuspiciousFileOperation:
                    exists = None
                if exists == True or exists == False:
                    deps.append(dep['file'])

            # Cache the dependencies for the next possible run.
            self._deps = deps

        # Test the dependencies to see if they're out of date.
        for dep in deps:
            if super(BrowserifyCompiler, self).is_outdated(dep, outfile):
                return True

        return False
