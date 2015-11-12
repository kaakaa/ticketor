import os, sys, re

import distutils.cmd
import distutils.log
import setuptools
import subprocess

class BuildApiCommand(distutils.cmd.Command):
  """A custom command to build api document with Sphinx"""

  description = 'run sphinx-apidoc'
  user_options = []

  def initialize_options(self):
    """Set default values for options."""

  def finalize_options(self):
    """Post-process options."""

  def run(self):
    from sphinx.apidoc import main
    """Run command."""
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    exit = main(['sphinx-apidoc', '-F', '-o', './docs', './app'])
    self.run_command('build_sphinx')