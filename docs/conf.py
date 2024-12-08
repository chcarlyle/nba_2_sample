# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'nba_2_sample'
copyright = '2024, Caleb Carlyle'
author = 'Caleb Carlyle'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Add the path to your source code
sys.path.insert(0, os.path.abspath('C:\Users\caleb\OneDrive\Documents\Stat 386\nba_2_sample\nba_2_sample'))  # Update '../src' with the correct relative path to your source code

extensions = [
    'sphinx.ext.autodoc',  # Enables autodoc for automatic API documentation
    'sphinx.ext.napoleon',  # Supports Google-style and NumPy-style docstrings
    'sphinx.ext.viewcode',  # Adds links to source code
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
