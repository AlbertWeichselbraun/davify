#!/usr/bin/env python

'''
removes outdated files from the given directory

'''

from os import remove
from os.path import getmtime, basename
from time import time
from glob import glob
from re import compile

from davify.transform import letters_to_int
from davify.config import EXTRACT_LIFETIME_STR

def clean_directory(location):
    '''
    ::param location:
        location to clean
    '''
    for fname in glob("{0}/*".format(location)):
        file_age_in_hours = time() - getmtime(fname) / 3600
        file_max_age = get_max_file_age(fname)

        if file_max_age and file_age_in_hours > file_max_age:
            remove(fname)


def get_max_file_age(fname):
    '''
    determines the maximum file age based on the file name
    '''
    fname = basename(fname)
    m = compile(EXTRACT_LIFETIME_STR).search(fname)
    if m:
        lifetime_str = m.group(1)
        assert len(lifetime_str) == 2
        return letters_to_int(lifetime_str)

    return None
    

# -----------------------------------------------------------
# - Unit tests
# -----------------------------------------------------------

def test_max_file_age():
    fname = "EIcLcO-buchungen-fernw%C3%A4rme-23dez-0657.pdf"
    assert get_max_file_age(fname) == 168
