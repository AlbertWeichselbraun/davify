#!/usr/bin/env python

'''
davify - uploads files to a webdav server for retrieval via https

'''


from argparse import ArgumentParser
from time import strftime
from os.path import splitext, basename, join as os_join
from random import choice
import gtk

import easywebdav
from davify import keyring
from davify.transform import int_to_letters, letters_to_int, INT_TO_CHR
from davify.config import FILENAME_PATTERN, FILE_URL_PATTERN, MESSAGE

APPLICATION_NAME = 'davify'
get_version_suffix = lambda: strftime("-%d%b-%I%M%p").lower()

def get_file_name_dict(fname, suggested_lifetime, version_suffix=''):
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

    return {'random_prefix' : random_prefix,
            'lifetime_str'  : lifetime_str,
            'fname'         : fname,
            'version_suffix': version_suffix,
            'ext'           : ext}


def upload(local_fname, lifetime, webdav_file_pattern, file_url_pattern):
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
    file_url_dict = get_file_name_dict(local_fname, lifetime, get_version_suffix())
    file_url_dict['protocol'] = file_storage.protocol
    file_url_dict['file_server'] = file_storage.server
    file_url_dict['file_path'] = file_storage.path
    file_url_dict['hours'] = lifetime
    file_url_dict['url'] = file_url_pattern.format(**file_url_dict)

    remote_fname = os_join(file_storage.path,
                           webdav_file_pattern.format(**file_url_dict))
    webdav.upload(local_fname, remote_fname)
    return file_url_dict

def print_notification_message(notification_message, file_url_dict):
    '''
    prints the notification message based on the file_url_dict
    '''
    msg = notification_message.format(**file_url_dict).replace("\\n", "\n")
    print(msg)

    # and send it to the clipboard :)
    clipboard = gtk.clipboard_get()
    clipboard.set_text(msg)
    clipboard.store()


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("fname", help="File to davify.", default=None)
    parser.add_argument("--lifetime", help="Suggested file lifetime in hours (default: 1 week).", default=168)
    parser.add_argument("--retrieval-url-pattern", help="Pattern to use for the retrieval URL.")
    parser.add_argument("--webdav-file-pattern", help="Pattern used to create the webdav file.", default=FILENAME_PATTERN)
    parser.add_argument("--file-url-pattern", help="Patterns used to retrieve the created file", default=FILE_URL_PATTERN)
    return parser.parse_args()



# -----------------------------------------------------------------------------
# The main program
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    args = parse_arguments()
    file_url_dict = upload(args.fname, args.lifetime,
            webdav_file_pattern = FILENAME_PATTERN, file_url_pattern=FILE_URL_PATTERN)
    print_notification_message(notification_message=MESSAGE, file_url_dict=file_url_dict)
