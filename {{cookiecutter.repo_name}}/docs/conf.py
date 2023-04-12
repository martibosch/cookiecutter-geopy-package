import os
import sys

project = "{{ cookiecutter.project_name }}"
author = "{{ cookiecutter.author_name }}"

__version__ = "{{ cookiecutter.version }}"
version = __version__
release = __version__

extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "myst_parser"]

autodoc_typehints = "description"
html_theme = "default"

# add module to path
sys.path.insert(0, os.path.abspath(".."))
