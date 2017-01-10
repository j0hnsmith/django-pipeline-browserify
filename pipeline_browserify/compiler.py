from pipeline.compilers import SubProcessCompiler
from django.conf import settings
from django.core.exceptions import SuspiciousFileOperation
from pipeline.exceptions import CompilerError

class BrowserifyCompiler(SubProcessCompiler):
    output_extension = 'browserified.js'
    
    def match_file(self, path):
        if self.verbose:
            print('matching file:', path)
        return path.endswith('.browserify.js')
    
    # similar to old removed in https://github.com/jazzband/django-pipeline/commit/1f6b48ae74026a12f955f2f15f9f08823d744515
    def simple_execute_command(self, cmd, **kwargs):
        import subprocess
        pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)
        stdout, stderr = pipe.communicate()
        if self.verbose:
            print stdout
            print stderr
        if pipe.returncode != 0:
            raise CompilerError("Compiler returned non-zero exit status %i" % pipe.returncode, command=cmd, error_output=stderr)
        return stdout
    
    def _get_cmd_parts(self):
        pipeline_settings = getattr(settings, 'PIPELINE', {})
        tool = pipeline_settings.get('BROWSERIFY_BINARY', "/usr/bin/env browserify")
        args = pipeline_settings.get('BROWSERIFY_ARGUMENTS', [])
        if not isinstance(args, list):
            args = args.split()
        
        env = pipeline_settings.get('BROWSERIFY_VARS', {})
        if not isinstance(env, dict):
            env = dict(map(lambda s: s.split('='), env.split()))
        if len(env):
            # even if there's custom variables, we need to pass along the original environment
            import os
            _env = {}
            _env.update(os.environ)
            _env.update(env)
            env = _env
        else:
            # drop any empty dict and let subprocess retain environment automatically
            env = None
        
        return tool, args, env
    
    def compile_file(self, infile, outfile, outdated=False, force=False):
        if not force and not outdated:
            return
        
        tool, args, env = self._get_cmd_parts()
        args.extend([infile, '--outfile', outfile])
        cmd = [tool] + args
        
        if self.verbose:
            print "compile_file command:", cmd, env
        self.simple_execute_command(cmd, env=env)
    
    def is_outdated(self, infile, outfile):
        """Check if the input file is outdated.
        
        The difficulty with the default implementation is that any file that is
        `require`d from the entry-point file will not trigger a recompile if it
        is modified. This overloaded version of the method corrects this by generating
        a list of all required files that are also a part of the storage manifest
        and checking if they've been modified since the last compile.
        
        The command used to generate the list of dependencies is the same as the compile
        command but uses the `--list` option instead of `--outfile`.
        
        WARNING: It seems to me that just generating the dependencies may take just
        as long as actually compiling, which would mean we would be better off just
        forcing a compile every time.
        """
        
        # Preliminary check for simply missing file or modified entry-point file.
        if super(BrowserifyCompiler, self).is_outdated(infile, outfile):
            return True
        
        # Otherwise we need to see what dependencies there are now, and if they're modified.
        tool, args, env = self._get_cmd_parts()
        args.extend(['--list', infile])
        cmd = [tool] + args
        if self.verbose:
            print "is_outdated command:", cmd, env
        dep_list = self.simple_execute_command(cmd, env=env)
        if self.verbose:
            print "dep_list is:", dep_list
        for dep_file in dep_list.strip().split('\n'):
            if super(BrowserifyCompiler, self).is_outdated(dep_file, outfile):
                if self.verbose:
                    print "Found dep_file \"%s\" updated." % dep_file
                return True
        
        return False
