#!/usr/bin/env python

'''
standard file name and data type transformations

'''

from os.path import dirname, basename, join as os_join
from string import ascii_lowercase, ascii_uppercase, digits

INT_TO_CHR = ascii_lowercase + ascii_uppercase + digits + "_-"

# changes filename prefix to a subdir
# 1H5McO-keyring-12dec-1031pm.py > 1H5McO/keyring-12dec-1031pm.py
subdir_prefix = lambda s: os_join(dirname(s), basename(s)[:6] + "/" + basename(s)[7:])

new_base_url = lambda newbase, s: os_join(newbase, basename(s))

def int_to_letters(i):
    '''
    converts an integer between 0 and 4096 to a two letter
    string which is then base64 encoded.
    '''
    assert i < 4096
    low, high = i % 64, i // 64
    return INT_TO_CHR[high] + INT_TO_CHR[low]

def letters_to_int(s):
    ''' converts a two letter combination to an integer '''
    assert len(s) == 2
    low, high = INT_TO_CHR.index(s[1]), INT_TO_CHR.index(s[0])
    return 64*high + low


# -----------------------------------------------------------
# - Unit tests
# -----------------------------------------------------------

def test_int_to_letters():
    from random import randint

    assert int_to_letters(0) == 'aa'
    assert int_to_letters(4095) == '--'

    for no in xrange(16):
        i = randint(0, 4095)
        assert i == letters_to_int(int_to_letters(i))

def test_subdir_prefix():
    assert subdir_prefix('http://www.test.org/mydir/dav/1H5McO-keyring-12dec-1031pm.py') == 'http://www.test.org/mydir/dav/1H5McO/keyring-12dec-1031pm.py'

def test_new_base_url():
     assert new_base_url('http://dav.test.org', 'http://www.test.org/mydir/dav/1H5McO-keyring-12dec-1031pm.py') == 'http://dav.test.org/1H5McO-keyring-12dec-1031pm.py'

