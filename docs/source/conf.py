# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Flappy Bird'
copyright = '2023, Andrew Birukov, Aleksandra Korabulina, Diana Rudenko'
author = 'Andrew Birukov, Aleksandra Korabulina, Diana Rudenko'
release = '0.0.1'

import os
import sys
sys.path.insert(0, os.path.abspath('../..'))
sys.path.append(os.path.abspath(
    os.path.join(__file__, "../../FlappyBird")
))

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc']

templates_path = []
exclude_patterns = ['build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = []

locale_dirs = ['locales/']
gettext_compact = False
