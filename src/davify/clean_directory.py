#!/usr/bin/env python
"""
removes outdated files from the given directory
"""

from argparse import ArgumentParser
from os import remove
from os.path import getmtime, basename
from time import time
from glob import glob
from re import compile
from datetime import timedelta

from davify.transform import CHR_TO_TIME
from davify.config import EXTRACT_LIFETIME_STR


def clean_directory(location):
    """
    ::param location:
        location to clean
    """
    for fname in glob("{0}/*".format(location)):
        file_age_in_hours = timedelta(seconds=time() - getmtime(fname))
        file_max_age = get_max_file_age(fname)

        # only remove the file, if file_max_age > file_age and
        # file_max_age != 0 or None
        if file_max_age and file_age_in_hours > file_max_age:
            remove(fname)


def get_max_file_age(fname):
    """
    determines the maximum file age based on the file name
    """
    fname = basename(fname)
    m = compile(EXTRACT_LIFETIME_STR).search(fname)
    if m:
        lifetime_str = m.group(1)
        assert len(lifetime_str) == 1
        return CHR_TO_TIME[lifetime_str]

    return None


# -----------------------------------------------------------
# - Unit tests
# -----------------------------------------------------------


def test_max_file_age():
    from datetime import timedelta

    fname = "EIcLm-buchungen-fernw%C3%A4rme-23dez-0657.pdf"
    assert get_max_file_age(fname) == timedelta(weeks=1)


def parse_arguments():
    """prepares the argument parser"""
    parser = ArgumentParser()
    parser.add_argument("fname", help="The directory to clean.")
    return parser.parse_args()


# -----------------------------------------------------------------------------
# The main program
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    args = parse_arguments()
    clean_directory(args.fname)
