# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Giskard'
copyright = '2023, Giskard AI'
author = 'Giskard AI'
release = '2.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["myst_parser",
              'nbsphinx',
              'sphinx_design',
              'sphinx.ext.todo',
              'sphinx.ext.napoleon',
              'sphinx.ext.autodoc',
              'sphinx.ext.linkcode',
              'sphinx_tabs.tabs',
              'sphinx_copybutton',
              'sphinx_tabs.tabs',
              'sphinx_click']

# autodoc_mock_imports = ["giskard.ml_worker.generated"]
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

myst_enable_extensions = [
    "amsmath",
    "attrs_inline",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# -----------------------------------------------------------------------------
# HTML output
# -----------------------------------------------------------------------------

html_title = "Giskard Documentation"

html_theme = 'furo'
html_static_path = ['_static']

html_css_files = ['css/custom.css']
html_js_files = ["js/githubStargazers.js"]

html_theme_options = {
    "light_logo": "logo_black.png",
    "dark_logo": "logo_white.png",
    "light_css_variables": {
        "color-brand-content": "#173A2F",
        "color-api-highlight": "#56D793",
        "color-api-background": "#F5F5F5",
        "color-toc-item-text--active": "#56D793",
        "color-sidebar-current-text": "#56D793",
        "color-sidebar-link-text--top-level": "#0c0c0c",
        "color-content-foreground": "#484848",
        "social-button-background": "#FFFFFF",
        "social-button-text": "#91F6C0",
    },
    "dark_css_variables": {
        "color-brand-primary": "#56D793",
        "color-brand-content": "#91F6C0",
        "color-api-background": "#242424",
        "color-sidebar-current-text": "#56D793",
        "color-toc-item-text--active": "#56D793",
        "color-sidebar-link-text--top-level": "#FcFcFc",
        "color-content-foreground": "#FFFFFF",
        "social-button-background": "#000000",
        "social-button-text": "#000000",
    },
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "top_of_page_button": "edit",
    "source_repository": "https://github.com/Giskard-AI/giskard",
    "source_branch": "feature/sphinx-documentation",
    "source_directory": "python-client/docs/",
    "source_edit_link": "https://github.com/Giskard-AI/giskard/edit/feature/sphinx-documentation/python-client/docs/{filename}",
}

add_function_parentheses = False
# Do not execute the notebooks when building the docs
nbsphinx_execute = "never"

import inspect
import os
import sys

sys.path.insert(0, os.path.abspath('../'))


# make github links resolve
def linkcode_resolve(domain, info):
    if domain != "py":
        return None

    modname = info["module"]
    fullname = info["fullname"]

    submod = sys.modules.get(modname)
    print(submod)
    if submod is None:
        return None

    for part in fullname.split("."):
        try:
            obj = getattr(submod, part)
            print(obj)
        except:  # noqa: E722
            return None

    try:
        fn = inspect.getsourcefile(obj.test_fn)  # TODO: generalise for other objects!
        print(fn)
    except:  # noqa: E722
        fn = None
    if not fn:
        return None

    try:
        source, lineno = inspect.getsourcelines(obj)
    except:  # noqa: E722
        lineno = None

    if lineno:
        linespec = "#L%d-L%d" % (lineno, lineno + len(source) - 1)
    else:
        linespec = ""

    filename = fn.split("python-client", 1)[-1]
    return f"https://github.com/Giskard-AI/giskard/blob/feature/ai-test-v2-merged/python-client{filename}{linespec}"
