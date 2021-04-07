"""Setup configuration for investigator."""

import os
from pathlib import Path
from setuptools import setup


def get_version():
    """Get current version of adviser module."""
    with open(os.path.join("thoth", "investigator", "__init__.py")) as f:
        content = f.readlines()

    for line in content:
        if line.startswith("__version__ ="):
            # dirty, remove trailing and leading chars
            return line.split(" = ")[1][1:-2]
    raise ValueError("No version identifier found")


VERSION = get_version()
setup(
    name="thoth-investigator",
    version=VERSION,
    description="Thoth component used for manipulating with messages and workloads.",
    long_description=Path("README.rst").read_text(),
    license="GPLv3+",
    url="https://github.com/thoth-station/investigator",
    zip_safe=False,
    long_description_content_type="text/x-rst",
    command_options={
        "build_sphinx": {
            "version": ("setup.py", VERSION),
            "release": ("setup.py", VERSION),
        }
    },
)
