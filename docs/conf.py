"""
Sphinx documentation configuration file for Modern Python Project.
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("../src"))

# -- Project information -----------------------------------------------------
project = "Modern Python"
copyright = "2024, Modern Python Team"
author = "Modern Python Team"
release = "0.1.0"
version = "0.1.0"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.githubpages",
    "sphinx.ext.doctest",
    "sphinx_autodoc_typehints",
    "myst_parser",
]

# Add support for Markdown files
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# The master toctree document
master_doc = "index"

# Templates path
templates_path = ["_templates"]

# List of patterns to exclude
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**.ipynb_checkpoints"]

# Pygments style for syntax highlighting
pygments_style = "sphinx"

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"

# Theme options
html_theme_options = {
    "logo_only": False,
    "display_version": True,
    "prev_next_buttons_location": "bottom",
    "style_external_links": False,
    "vcs_pageview_mode": "",
    "style_nav_header_background": "#2980B9",
    # Toc options
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}

# Add any paths that contain custom static files
html_static_path = ["_static"]

# Custom sidebar templates
html_sidebars = {
    "**": [
        "relations.html",
        "searchbox.html",
    ]
}

# -- Options for autodoc -----------------------------------------------------
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}

autodoc_typehints = "both"
autodoc_typehints_format = "short"

# Napoleon settings for Google and NumPy style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# -- Options for intersphinx -------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pytest": ("https://docs.pytest.org/en/stable", None),
    "pydantic": ("https://docs.pydantic.dev", None),
    "httpx": ("https://www.python-httpx.org", None),
}

# -- Options for todo extension ----------------------------------------------
todo_include_todos = True

# -- Options for MyST parser -------------------------------------------------
myst_enable_extensions = [
    "deflist",
    "tasklist",
    "html_image",
    "colon_fence",
    "smartquotes",
    "replacements",
    "linkify",
    "strikethrough",
]

myst_heading_anchors = 3

# -- Options for coverage extension ------------------------------------------
coverage_show_missing_items = True


# -- Custom setup ------------------------------------------------------------
def setup(app):
    """Custom Sphinx setup."""
    app.add_css_file("custom.css")

    # Create _static directory if it doesn't exist
    static_dir = Path(__file__).parent / "_static"
    static_dir.mkdir(exist_ok=True)

    # Create custom CSS file
    custom_css = static_dir / "custom.css"
    if not custom_css.exists():
        custom_css.write_text("""
/* Custom CSS for Modern Python documentation */
.wy-nav-content {
    max-width: 1200px !important;
}

.rst-content code {
    font-size: 90%;
    background: #f5f5f5;
    border: 1px solid #e1e4e5;
    border-radius: 3px;
    padding: 1px 4px;
}

.rst-content pre {
    font-size: 85%;
}

/* Better tables */
.rst-content table.docutils {
    border: 1px solid #e1e4e5;
}

.rst-content table.docutils td,
.rst-content table.docutils th {
    padding: 8px 12px;
    border: 1px solid #e1e4e5;
}

/* Admonitions */
.admonition {
    border-radius: 4px;
}

.admonition-title {
    border-radius: 4px 4px 0 0;
}
""")
