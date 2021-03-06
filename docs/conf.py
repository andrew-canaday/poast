#!/usr/bin/env python
#
# poast documentation build configuration file, created by
# sphinx-quickstart on Fri Jun  9 13:47:02 2017.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another
# directory, add these directories to sys.path here. If the directory is
# relative to the documentation root, use os.path.abspath to make it
# absolute, like shown here.
#
import poast.openapi3
import os
import sys
sys.path.insert(0, os.path.abspath('..'))


# -- General configuration ---------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.napoleon",
    "recommonmark",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_suffix = ['.rst', '.md']

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'poast'
copyright = "2020, Andrew T. Canaday"
author = "Andrew T. Canaday"

# The version info for the project you're documenting, acts as replacement
# for |version| and |release|, also used in various other places throughout
# the built documents.
#
# The short X.Y version.
version = poast.__version__
# The full version, including alpha/beta/rc tags.
release = poast.__version__

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True
todo_emit_warnings = False

# Autodoc stuff:
autodoc_member_order = 'groupwise'

# Diagram stuff:
graphviz_output_format = 'svg'
inheritance_alias = {
    'poast.openapi3.spec.model.baseobj.OpenApiBaseObject': 'OpenApiBaseObject',
    'poast.openapi3.spec.model.containers.OpenApiContainer': 'OpenApiContainer',
    'poast.openapi3.spec.model.containers.OpenApiList': 'OpenApiList',
    'poast.openapi3.spec.model.containers.OpenApiMap': 'OpenApiMap',
    'poast.openapi3.spec.model.entity.OpenApiEntity': 'OpenApiEntity',
    'poast.openapi3.spec.model.exceptions.DocumentParsingException': 'DocumentParsingException',
    'poast.openapi3.spec.model.exceptions.MalformedDocumentException': 'MalformedDocumentException',
    'poast.openapi3.spec.model.exceptions.InvalidFieldValueException': 'InvalidFieldValueException',
    'poast.openapi3.spec.model.exceptions.MissingRequiredFieldException': 'MissingRequiredFieldException',
    'poast.openapi3.spec.model.field.OpenApiDataSpec': 'OpenApiDataSpec',
    'poast.openapi3.spec.model.field.OpenApiFieldSpec': 'OpenApiFieldSpec',
    'poast.openapi3.spec.model.field.OpenApiFieldUnion': 'OpenApiFieldUnion',
    'poast.openapi3.spec.model.primitives.OpenApiPrimitive': 'OpenApiPrimitive',
    'poast.openapi3.spec.model.primitives.OpenApiInteger': 'OpenApiInteger',
    'poast.openapi3.spec.model.primitives.OpenApiNumber': 'OpenApiNumber',
    'poast.openapi3.spec.model.primitives.OpenApiString': 'OpenApiString',
    'poast.openapi3.spec.model.primitives.OpenApiBoolean': 'OpenApiBoolean',
    'poast.openapi3.spec.model.primitives.OpenApiAny': 'OpenApiAny',
    'poast.openapi3.spec.model.reference.ReferenceObject': 'ReferenceObject',
}
inheritance_graph_attrs = dict(
    rankdir="LR",
    size='"6.0, 8.0"',
    fontsize=24,
    ratio='compress',
)
inheritance_node_attrs = dict(
    fontsize=24,
    height=0.75,
)

# -- Options for HTML output -------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'
html_logo = 'img/poast-logo-200.png'
html_favicon = 'img/favicon.ico'

# Theme options are theme-specific and customize the look and feel of a
# theme further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    "show_powered_by": False,
    "github_user": "andrew-canaday",
    "github_repo": "poast",
    # "github_banner": True,
    "github_banner": False,
    # "show_related": False,
    "show_related": True,
    "note_bg": "#FFF59C",
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
#html_static_path = ['_static']
html_static_path = []
# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'poast'


# -- Options for LaTeX output ------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass
# [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'poast.tex',
     'poast Documentation',
     'Andrew T. Canaday', 'manual'),
]


# -- Options for manual page output ------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'poast',
     'poast Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'poast',
     'poast Documentation',
     author,
     'poast',
     'OpenAPI 3.0 parser/validator + client generator.',
     'OpenAPI'),
]


intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "requests": ("https://requests.readthedocs.io/en/master/", None),
    "requests-oauthlib": ("https://requests-oauthlib.readthedocs.io/en/latest/", None),
}
