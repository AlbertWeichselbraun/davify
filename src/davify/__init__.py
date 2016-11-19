#!/usr/bin/env python3

'''
davify - uploads files to a webdav server for retrieval via https

'''


from argparse import ArgumentParser
from time import strftime
from os.path import splitext, basename, join as os_join
from os import getenv
try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote
from random import choice

import sys
import easywebdav
from davify import keyring, store_password
from davify.transform import int_to_letters, letters_to_int, INT_TO_CHR
from davify.config import FILENAME_PATTERN, FILE_URL_PATTERN, MESSAGE
from davify.clean_directory import clean_directory

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

    random_prefix = "".join((choice(INT_TO_CHR) for _ in range(4)))
    lifetime_str = int_to_letters(suggested_lifetime)
    fname, ext = splitext(basename(fname))

    return {'random_prefix' : random_prefix,
            'lifetime_str'  : lifetime_str,
            'fname'         : fname,
            'fname_quoted'  : quote(fname),
            'version_suffix': version_suffix,
            'ext'           : ext}


def upload(local_fname, lifetime, webdav_file_pattern, file_url_pattern):
    ''' uploads the given file to the webdav server :)

    ::param local_fname:
        file name of the local file

    ::param lifetime:
        suggested lifetime of the uploaded file
    '''
    file_storage = keyring.get_passwords()[0]
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
                           quote(webdav_file_pattern.format(**file_url_dict)))
    webdav.upload(local_fname, remote_fname)
    return file_url_dict

def print_notification_message(notification_message, file_url_dict):
    '''
    prints the notification message based on the file_url_dict
    '''
    msg = notification_message.format(**file_url_dict).replace("\\n", "\n")
    print(msg)

    # and send it to the clipboard :)
    from pyperclip import copy
    copy(msg)

def setup_webdav_server(default_protocol='https', default_server='localhost',
                        default_port=443, default_path='/',
                        default_username=getenv('USER')):
    '''
    Setup the webdav server
    '''
    from getpass import getpass

    print("Setup WebDAV server connection.")
    print("===============================")
    protocol = input("Protocol ({}) : ".format(default_protocol)) or default_protocol
    server = input("WebDAV server name ({}): ".format(default_server)) or default_server
    port = input("WebDAV server port ({}): ".format(default_port)) or default_port
    path = input("WebDAV server path ({}): ".format(default_path)) or default_path
    username = input("WebDAV server username ({}): ".format(default_username)) or default_username
    password = getpass("WebDAV server password: ")
    store_password(username, password, protocol, server, port, path)

def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("fname", help="File to davify or directory to clean.", nargs="*", default=None)
    parser.add_argument("--lifetime", help="Suggested file lifetime in hours (default: 1 week). Zero suggests that the file is never deleted.", type=int, default=168)
    parser.add_argument("--retrieval-url-pattern", help="Pattern to use for the retrieval URL.")
    parser.add_argument("--webdav-file-pattern", help="Pattern used to create the webdav file.", default=FILENAME_PATTERN)
    parser.add_argument("--file-url-pattern", help="Patterns used to retrieve the created file", default=FILE_URL_PATTERN)
    parser.add_argument("--clean-directory", help="Remove outdated files from the given directory.", action='store_true')
    parser.add_argument("--setup", help="Setup WebDAV connection.", action="store_true")
    return parser.parse_args()

# -----------------------------------------------------------------------------
# The main program
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    args = parse_arguments()

    if args.setup:
        setup_webdav_server()
    elif args.clean_directory:
        clean_directory(args.fname)
    else:
        if not args.fname:
            print("No filename provided.")
            sys.exit(-1)
        elif len(args.fname) == 1:
            filename = args.fname[0]
        else:
            # multi file support
            pass
        file_url_dict = upload(filename, args.lifetime,
                               webdav_file_pattern=FILENAME_PATTERN,
                               file_url_pattern=FILE_URL_PATTERN)
        print_notification_message(notification_message=MESSAGE, file_url_dict=file_url_dict)

