"""Various utility functions to manage Python environments"""

from typing import List

import os
import sys
import warnings
from platform import python_version

import importlib_metadata

# Libs to be excluded when create a kernel automatically from the current env
EXCLUDED_PYLIBS = [
    "setuptools",
    "pip",
]


def get_python_requirements() -> str:
    pip_requirements = os.popen(f"{sys.executable} -m pip list --format freeze").read()
    if pip_requirements:
        return pip_requirements
    else:
        raise RuntimeError(
            "Python requirements could not be resolved. "
            + "Please use one of the following Python package managers: "
            + "Poetry, Pipenv or Pip."
        )


def get_python_version() -> str:
    return python_version()


def warning(content: str):
    warnings.warn(content, stacklevel=2)


def format_pylib_extras(name):
    extras = importlib_metadata.metadata(name).get_all("Provides-Extra")
    if not extras or len(extras) == 0:
        return ""
    else:
        return f"[{', '.join(extras)}]"


def freeze_dependency_list(exact_deps: bool = False, excludes: List[str] = EXCLUDED_PYLIBS, only_giskard: bool = False):
    return [
        f"{dep}=={ver}"
        for dep, ver in freeze_dependencies(exact_deps=exact_deps, excludes=excludes, only_giskard=only_giskard).items()
    ]


def freeze_dependencies(exact_deps: bool = False, excludes: List[str] = EXCLUDED_PYLIBS, only_giskard: bool = False):
    return {
        f"{dist.name}{format_pylib_extras(dist.name) if exact_deps or dist.name == 'giskard' else ''}": "{dist.version}"
        for dist in importlib_metadata.distributions()
        if dist.name not in excludes and (not only_giskard or dist.name == "giskard")
    }
