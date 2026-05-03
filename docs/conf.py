# Configuration file for the Sphinx documentation builder.
import sys
from pathlib import Path

# Make the tricor source tree importable so autodoc can pull
# docstrings + signatures.  The tricor repo lives next to tricor-docs.
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tricor" / "src"))

project = "tricor"
copyright = "2025, Colin Ophus"
author = "Colin Ophus"
release = "0.1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.mathjax",
    "myst_nb",
]

# MyST (Markdown) support
myst_enable_extensions = [
    "colon_fence",
    "fieldlist",
    "dollarmath",
    "amsmath",
]
# Auto-generate anchors for H1..H3 so cross-doc links like
# ``[text](path.md#preset-summary)`` resolve.
myst_heading_anchors = 3
templates_path = ["_templates"]
exclude_patterns = ["_build", "_static/README.md"]

# Static assets (trajectory viewers, etc.)
html_static_path = ["_static"]

# Theme
html_theme = "furo"
html_title = "tricor"
html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#2a6e4e",
        "color-brand-content": "#2a6e4e",
    },
}

# Autodoc
autodoc_member_order = "bysource"
autodoc_typehints = "description"

# Intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "ase": ("https://wiki.fysik.dtu.dk/ase/", None),
}

# Napoleon (Google/NumPy docstrings)
napoleon_google_docstring = False
napoleon_numpy_docstring = True

# myst-nb: don't execute code cells during build
# (too slow for RTD; run locally and commit output if needed)
nb_execution_mode = "off"
