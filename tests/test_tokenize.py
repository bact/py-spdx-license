# SPDX-FileContributor: Arthit Suriyawongkul
# SPDX-FileCopyrightText: Joshua Watt <JPEWhacker@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: MIT

from py_spdx_license import parse
from py_spdx_license.ast import ParseError, tokenize

import pytest

# (expression, [(value, start, end), ...], str(parse()) or (error, error range))
# fmt: off
CASES = [
    ("((mit)AND( apache-2.0 WITH classpath-exception-2.0 ))", [("(", 0, 1), ("(", 1, 2), ("mit", 2, 5), (")", 5, 6), ("AND", 6, 9), ("(", 9, 10), ("apache-2.0", 11, 21), ("WITH", 22, 26), ("classpath-exception-2.0", 27, 50), (")", 51, 52), (")", 52, 53)], "MIT AND Apache-2.0 WITH Classpath-exception-2.0"),
    ("\tMIT AND (bsd-3-clause\r\n  OR LicenseRef-x)\nOR DocumentRef-d.1:LicenseRef-y  ", [("MIT", 1, 4), ("AND", 5, 8), ("(", 9, 10), ("bsd-3-clause", 10, 22), ("OR", 26, 28), ("LicenseRef-x", 29, 41), (")", 41, 42), ("OR", 43, 45), ("DocumentRef-d.1:LicenseRef-y", 46, 74)], "MIT AND (BSD-3-Clause OR LicenseRef-x) OR DocumentRef-d.1:LicenseRef-y"),
    ("GPL-2.0+", [("GPL-2.0", 0, 7), ("+", 7, 8)], ("Unexpected '+'", (7, 8))),
    (" \n\t", [], ("Empty expression", None)),
    ("MIT OR ISC AND", [("MIT", 0, 3), ("OR", 4, 6), ("ISC", 7, 10), ("AND", 11, 14)], ("Unexpected 'OR'", (4, 6))),
    ("(MIT AND ISC", [("(", 0, 1), ("MIT", 1, 4), ("AND", 5, 8), ("ISC", 9, 12)], ("Unexpected '('", (0, 1))),
    ("MIT AND UNKNOWNID", [("MIT", 0, 3), ("AND", 4, 7), ("UNKNOWNID", 8, 17)], ("Unknown Expression 'UNKNOWNID'", (8, 17))),
]
# fmt: on
IDS = [repr(c[0]) for c in CASES]


@pytest.mark.parametrize("expression,tokens,result", CASES, ids=IDS)
def test_tokenize(expression, tokens, result):
    assert [(t.value, t.start, t.end) for t in tokenize(expression)] == tokens


@pytest.mark.parametrize("expression,tokens,result", CASES, ids=IDS)
def test_parse(expression, tokens, result):
    if isinstance(result, str):
        assert str(parse(expression)) == result
        return

    with pytest.raises(ParseError) as e:
        parse(expression)
    node_range = e.value.n.get_range() if e.value.n else None
    assert (str(e.value), node_range) == result
