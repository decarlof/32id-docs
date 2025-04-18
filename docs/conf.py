#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Project documentation build configuration file, created by
# sphinx-quickstart on Fri Mar 13 16:29:32 2015.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys
import os

import sphinx_rtd_theme

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath('..'))

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.mathjax',
    'sphinx.ext.todo',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinxcontrib.bibtex',
    'sphinx.ext.viewcode']

bibtex_bibfiles = [
    'source/pm/bibtex/ref.bib',
    'source/pm/bibtex/cite.bib',
    'source/txm/bibtex/ref.bib',
    'source/txm/bibtex/cite.bib',
    'source/hsi/AM/bibtex/AM_ref.bib',
    'source/hsi/manual/bibtex/scintilators.bib'
    ]

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = False
napoleon_use_rtype = False

todo_include_todos=True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
Affiliation = u'Argonne National Laboratory'
project = u'32-ID Docs'
copyright = u'2020, ' + Affiliation

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = open(os.path.join('..', 'VERSION')).read().strip()
# The full version, including alpha/beta/rc tags.
release = version

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

# The reST default role (used for this markup: `text`) to use for all
# documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
#keep_warnings = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_rtd_theme'

# on_rtd is whether we are on readthedocs.org
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

html_context = {
    "display_github": True, # Integrate GitHub
    "github_user": "xray-imaging", # Username
    "github_repo": "32id-docs", # Repo name
    "github_version": "master", # Version
    "conf_py_path": "/docs/", # Path in the checkout to the docs root
}

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
#html_extra_path = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = project+'doc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
# The paper size ('letterpaper' or 'a4paper').
#'papersize': 'letterpaper',

# The font size ('10pt', '11pt' or '12pt').
#'pointsize': '10pt',

# Additional stuff for the LaTeX preamble.
#'preamble': '',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
  ('index', 
  project+'.tex',
  project+u' Documentation',
  Affiliation,'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index',project, 
    project+u' Documentation',
    [Affiliation,],
    1)
]

# If true, show URL addresses after external links.
#man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  ('index', 
  project, 
  project+u' Documentation',
  Affiliation, 
  project, 
  'Scientific Data Exchange'),
]

# Documents to append as an appendix to all manuals.
#texinfo_appendices = []

# If false, no module index is generated.
#texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
#texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
#ztexinfo_no_detailmenu = False

# picked from http://read-the-docs.readthedocs.org/en/latest/faq.html
class Mock(object):

    __all__ = []

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return Mock()

    @classmethod
    def __getattr__(cls, name):
        return Mock()
    def __mul__(self, other):
        return Mock()
    def __rmul__(self, other):
        return Mock()
    def __pow__(self, other):
        return Mock()
    def __div__(self, other):
        return Mock()
    def __add__(self, other):
        return Mock()
    def __radd__(self, other):
        return Mock()

MOCK_MODULES = ['numpy']

for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = Mock()

from pybtex.style.formatting.unsrt import Style as UnsrtStyle
from pybtex.plugin import register_plugin
from pybtex.style.sorting import BaseSortingStyle
from pybtex.style.labels import BaseLabelStyle


class ReverseNumber(BaseLabelStyle):
    name = 'reverse_number'

    def format_labels(self, sorted_entries):
        for number in range(len(sorted_entries), 0, -1):
            yield str(number)

class ReverseSortingStyle(BaseSortingStyle):
    name = 'year_author_title'

    def sorting_key(self, entry):
        if entry.type in ('book', 'inbook'):
            author_key = self.author_editor_key(entry)
        elif 'author' in entry.persons:
            author_key = self.persons_key(entry.persons['author'])
        else:
            author_key = None
        return (-int(entry.fields.get('year', '')), author_key, entry.fields.get('title', ''))

    def persons_key(self, persons):
        return '   '.join(self.person_key(person) for person in persons)

    def person_key(self, person):
        return '  '.join((
            ' '.join(person.prelast() + person.last()),
            ' '.join(person.first() + person.middle()),
            ' '.join(person.lineage()),
        )).lower()

    def author_editor_key(self, entry):
        if entry.persons.get('author'):
            return self.persons_key(entry.persons['author'])
        elif entry.persons.get('editor'):
            return self.persons_key(entry.persons['editor'])

class ReverseDate(UnsrtStyle):
    name = 'reversedate'
    default_sorting_style = 'year_author_title'
    default_label_style = 'reverse_number'

register_plugin('pybtex.style.formatting', 'reversedate', ReverseDate)
register_plugin('pybtex.style.sorting', 'year_author_title', ReverseSortingStyle)
register_plugin('pybtex.style.labels', 'reverse_number', ReverseNumber)