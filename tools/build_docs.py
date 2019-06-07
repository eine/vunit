# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2014-2019, Lars Asplund lars.anders.asplund@gmail.com

"""
Command line utility to build documentation/website
"""

from subprocess import check_call
from os.path import join, dirname
import sys
from docs_utils import (
    examples,
    copy_common,
    custom_last,
    get_theme,
    third_party_vcs
)
from create_release_notes import create_release_notes


def main():
    """
    Build documentation/website
    """
    get_theme(
        url='https://codeload.github.com/buildthedocs/sphinx_btd_theme/tar.gz/vunit',
        strip=2,
        tarfilter='sphinx_btd_theme-vunit/sphinx_rtd_theme'
    )
    copy_common()
    custom_last('VUnit', 'vunit')
    examples()
    third_party_vcs('/src')
    create_release_notes()
    check_call([sys.executable, "-m", "sphinx",
                "-T", "-E", "-W", "-a", "-n", "-b", "html",
                join(dirname(__file__), "..", "docs"), sys.argv[1]])


if __name__ == "__main__":
    main()
