#!/usr/bin/env python

"""
standard file name and data type transformations
"""

from os.path import dirname, basename, join as os_join
from datetime import timedelta
from collections import OrderedDict


#
# static list of VALID_LIFE_TIMES and the corresponding
# mapping to one letter codes
#
VALID_LIFE_TIMES = OrderedDict(
    [
        ("forever", timedelta()),
        ("5 min", timedelta(minutes=5)),
        ("10 min", timedelta(minutes=10)),
        ("20 min", timedelta(minutes=20)),
        ("40 min", timedelta(minutes=40)),
        ("1 hour", timedelta(hours=1)),
        ("2 hours", timedelta(hours=2)),
        ("4 hours", timedelta(hours=4)),
        ("8 hours", timedelta(hours=8)),
        ("16 hours", timedelta(hours=16)),
        ("1 day", timedelta(days=1)),
        ("2 days", timedelta(days=2)),
        ("4 days", timedelta(days=4)),
        ("1 week", timedelta(weeks=1)),
        ("2 weeks", timedelta(weeks=2)),
        ("1 month", timedelta(days=31)),
        ("2 months", timedelta(days=62)),
        ("1 quarter", timedelta(days=92)),
        ("2 quarters", timedelta(days=183)),
        ("3 quarters", timedelta(days=275)),
        ("1 year", timedelta(days=366)),
        ("2 years", timedelta(days=731)),
        ("4 years", timedelta(days=1461)),
    ]
)

TIME_TO_CHR = {
    timedelta(): "0",
    timedelta(minutes=5): "a",
    timedelta(minutes=10): "b",
    timedelta(minutes=20): "c",
    timedelta(minutes=40): "d",
    timedelta(hours=1): "e",
    timedelta(hours=2): "f",
    timedelta(hours=4): "g",
    timedelta(hours=8): "h",
    timedelta(hours=16): "i",
    timedelta(days=1): "j",
    timedelta(days=2): "k",
    timedelta(days=4): "l",
    timedelta(weeks=1): "m",
    timedelta(weeks=2): "n",
    timedelta(days=31): "o",
    timedelta(days=62): "p",
    timedelta(days=92): "q",
    timedelta(days=183): "r",
    timedelta(days=275): "s",
    timedelta(days=366): "t",
    timedelta(days=731): "u",
    timedelta(days=1461): "v",
}

CHR_TO_TIME = {ch: delta for delta, ch in TIME_TO_CHR.items()}


# changes filename prefix to a subdir
# 1H5Mc-keyring-12dec-1031pm.py > 1H5McO/keyring-12dec-1031pm.py
def subdir_prefix(s):
    return os_join(dirname(s), basename(s)[:5] + "/" + basename(s)[6:])


def new_base_url(newbase, s):
    return os_join(newbase, basename(s))


# -----------------------------------------------------------
# - Unit tests
# -----------------------------------------------------------
def test_subdir_prefix():
    assert (
        subdir_prefix("http://www.test.org/mydir/dav/1H5cO-keyring" "-12dec-1031pm.py")
        == "http://www.test.org/mydir/"
        "dav/1H5cO/keyring-12dec-10"
        "31pm.py"
    )


def test_new_base_url():
    assert (
        new_base_url(
            "http://dav.test.org",
            "http://www.test.org/mydir/dav/15McO-keyring" "-12dec-1031pm.py",
        )
        == "http://dav.test.org/15McO-"
        "keyring-12dec-1031pm.py"
    )
