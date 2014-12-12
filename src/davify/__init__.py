#!/usr/bin/env python

'''
davify - uploads files to a webdav server for retrieval via https
'''


from argparse import ArgumentParser
from time import strftime
from string import ascii_lowercase, ascii_uppercase, digits
from os.path import splitext, basename, join as os_join
from random import choice

import easywebdav
from davify import keyring
from davify.transform import int_to_letters, letters_to_int

INT_TO_CHR = ascii_lowercase + ascii_uppercase + digits + "_-"
APPLICATION_NAME = 'davify'

get_version_suffix = lambda: strftime("-%d%b-%I%M%p").lower()

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


def test_int_to_letters():
    from random import randint

    assert int_to_letters(0) == 'aa'
    assert int_to_letters(4095) == '--'

    for no in xrange(16):
        i = randint(0, 4095)
        assert i == letters_to_int(int_to_letters(i))


def get_file_name(fname, suggested_lifetime, version_suffix=''):
    '''
    ::param fname:
        name of the file to davify
    ::param suggested_lifetime:
        suggested file lifetime in hours
    ::param fname_suffix:
        optional version_suffix

    ::returns:
        a filename which follows the following pattern
          rrrrtt-fname-suffix.ext

        rrrr   ... random prefix
        tt     ... lifetime
        fname  ... filename (without extension)
        suffix ... version suffix
        ext    ... the file extension
    '''
    assert suggested_lifetime < 4096

    random_prefix = "".join((choice(INT_TO_CHR) for _ in xrange(4)))
    lifetime_str  = int_to_letters(suggested_lifetime)
    fname, ext    = splitext(basename(fname))

    return "%s%s-%s%s%s" % (random_prefix, lifetime_str, fname,
                           version_suffix, ext)

def upload(local_fname, lifetime):
    ''' uploads the given file to the webdav server :) 
    
    ::param local_fname:
        file name of the local file

    ::param lifetime:
        suggested lifetime of the uploaded file
    '''
    file_storage = keyring.get_passwords(APPLICATION_NAME)[0]
    webdav = easywebdav.connect(file_storage.server,
                                username=file_storage.username,
                                password=file_storage.password,
                                protocol=file_storage.protocol)
    remote_fname = os_join(file_storage.path,
                           get_file_name(local_fname, lifetime, get_version_suffix()))
    webdav.upload(local_fname, remote_fname)
    print remote_fname


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("fname", help="File to davify.", default=None)
    parser.add_argument("--lifetime", help="Suggested file lifetime in hours (default: 1 week).", default=168)
    parser.add_argument("--retrieval-url-pattern", help="Pattern to use for the retrieval URL.")
    return parser.parse_args()



# -----------------------------------------------------------------------------
# The main program
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    args = parse_arguments()
    upload(args.fname, args.lifetime)

