#
# Copyright Joshua Watt <JPEWhacker@gmail.com>
#
# SPDX-License-Identifier: MIT
#

import py_spdx_license
from py_spdx_license.ast import ParseError, tokenize

import pytest


def test_token_ranges():
    tokens = tokenize("MIT AND (Apache-2.0)")
    assert [(t.value, t.start, t.end) for t in tokens] == [
        ("MIT", 0, 3),
        ("AND", 4, 7),
        ("(", 8, 9),
        ("Apache-2.0", 9, 19),
        (")", 19, 20),
    ]


def test_large_input():
    py_spdx_license.parse("LicenseRef-" + "a" * 200000)
    # Many tokens, kept flat to stay clear of the recursion limit
    with pytest.raises(ParseError, match="Unexpected Expression"):
        py_spdx_license.parse("MIT " * 40000)
