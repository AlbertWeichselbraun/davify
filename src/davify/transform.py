#!/usr/bin/env python

'''
standard file name transformations
'''

from os.path import dirname, basename, join as os_join

# changes filename prefix to a subdir
# 1H5McO-keyring-12dec-1031pm.py > 1H5McO/keyring-12dec-1031pm.py
subdir_prefix = lambda s: os_join(dirname(s), basename(s)[:6] + "/" + basename(s)[7:])

new_base_url = lambda newbase, s: os_join(newbase, basename(s))


def test_subdir_prefix():
    assert subdir_prefix('http://www.test.org/mydir/dav/1H5McO-keyring-12dec-1031pm.py') == 'http://www.test.org/mydir/dav/1H5McO/keyring-12dec-1031pm.py'

def test_new_base_url():
     assert new_base_url('http://dav.test.org', 'http://www.test.org/mydir/dav/1H5McO-keyring-12dec-1031pm.py') == 'http://dav.test.org/1H5McO-keyring-12dec-1031pm.py'

