# -*- coding: utf-8 -*-

from os.path import join, dirname, isfile
from json import loads


#!blog_title = u'VUnit Blog'
#!blog_baseurl = 'http://vunit.github.io'
#!blog_authors = {
#!    'Olof Kraigher': ('kraigher', None),
#!    'Lars Asplund': ('lasplund', None),
#!}

# post_date_format = '%b %d, %Y'
# post_auto_excerpt = 1
# post_auto_image = 0

# -- Sphinx Options -----------------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.extlinks',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinxarg.ext', # Automatic argparse command line argument documentation
]

# The suffix(es) of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'VUnit'
copyright = u'2014-2019, Lars Asplund'
author = u'lasplund'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = ''
# The full version, including alpha/beta/rc tags.
release = ''

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['release_notes/*.*']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'stata-dark'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = '_theme'

html_context = {
    'use_gfonts': True,
    'display_github': True,
    'slug_user': 'VUnit',
    'slug_repo': 'vunit',
    'slug_version': 'master/docs/',
    'description': 'A test framework for HDL',
    'current_version': 'master',
    'copyright_extra': ' - <a href="mailto:vunitframework@gmail.com">VUnitFramework</a>',
}

ctx = join(dirname(__file__), 'context.json')
if isfile(ctx):
    html_context.update(loads(open(ctx).read()))

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    'style_nav_header_background': '#0c479dff',
    'logo_only': True,
    'home_breadcrumbs': False,
    'home_logo': False,
    'prevnext_location': 'bottom'
}

# Add any paths that contain custom themes here, relative to this directory.
#!html_theme_path = [alabaster.get_path()]
html_theme_path = ['.']

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = '_static/img/VUnit_banner_white_250.png'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = join(html_static_path[0], 'vunit_neg.ico')

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%b %d, %Y'

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# Output file base name for HTML help builder.
htmlhelp_basename = 'vunitdoc'

extlinks = {'vunit_example' : ('https://github.com/VUnit/vunit/tree/master/examples/%s/', ''),
            'vunit_file' : ('https://github.com/VUnit/vunit/tree/master/%s/', ''),
            'vunit_commit' : ('https://github.com/vunit/vunit/tree/%s/', '@'),
            'vunit_issue' : ('https://github.com/VUnit/vunit/issues/%s/', '#')}
