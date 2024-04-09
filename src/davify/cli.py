#!/usr/bin/env python

"""
davify - uploads files to a webdav server for retrieval via https

   .. moduleauthor:: Albert Weichselbraun albert.weichselbraun@fhgr.ch

"""

from argparse import ArgumentParser
from time import strftime
from os.path import splitext, basename, join as os_join, isdir
from os import getenv
from tempfile import TemporaryDirectory
from glob import glob
from typing import List
from urllib.parse import quote
from random import choice
from string import ascii_lowercase, ascii_uppercase, digits
from shutil import which
from warnings import warn
from hashlib import sha3_224, sha1

import sys
import tarfile
import easywebdav
import pyperclip

from davify.keyring import get_passwords, store_password
from davify.transform import TIME_TO_CHR, VALID_LIFE_TIMES
from davify.config import FILENAME_PATTERN, FILE_URL_PATTERN, HASH_PATTERN, MESSAGE

APPLICATION_NAME = "davify"
TAR_FILE_MODE = "w:xz"
TAR_FILE_EXT = ".txz"
INT_TO_CHR = ascii_lowercase + ascii_uppercase + digits + "_-"


def get_version_suffix():
    """Returns a version suffix based on the current time and date."""
    return strftime("-%d%b-%I%M%p").lower()


def get_file_name_dict(fname, file_lifetime, version_suffix=""):
    """
    :param fname: name of the file to davify
    :param file_lifetime: suggested file lifetime in accordance to \
               the available VALID_LIFE_TIMES.
    :param fname_suffix: optional version_suffix

    :returns: a filename which follows the following pattern \
          rrrrt-fname-suffix.ext

        rrrr   ... random prefix
        t      ... lifetime
        fname  ... filename (without extension)
        suffix ... version suffix
        ext    ... the file extension
    """
    random_prefix = "".join((choice(INT_TO_CHR) for _ in range(4)))
    fname, ext = splitext(basename(fname))

    return {
        "random_prefix": random_prefix,
        "lifetime_str": TIME_TO_CHR[VALID_LIFE_TIMES[file_lifetime]],
        "fname": fname,
        "fname_quoted": quote(fname),
        "version_suffix": version_suffix,
        "ext": ext,
    }


def upload(local_fname, lifetime, webdav_file_pattern, file_url_pattern):
    """Uploads the given file to the webdav server :)

    :param local_fname: file name of the local file
    :param lifetime: suggested lifetime of the uploaded file
    """
    file_storage = get_passwords()[0]
    webdav = easywebdav.connect(
        file_storage.server,
        username=file_storage.username,
        password=file_storage.password,
        protocol=file_storage.protocol,
    )
    file_url_dict = get_file_name_dict(local_fname, lifetime, get_version_suffix())
    file_url_dict["protocol"] = file_storage.protocol
    file_url_dict["file_server"] = file_storage.server
    file_url_dict["file_path"] = file_storage.path
    file_url_dict["lifetime"] = lifetime
    file_url_dict["url"] = file_url_pattern.format(**file_url_dict)

    remote_fname = os_join(
        file_storage.path, quote(webdav_file_pattern.format(**file_url_dict))
    )
    webdav.upload(local_fname, remote_fname)
    return file_url_dict


def print_notification_message(notification_message, file_url_dict):
    """
    Prints the notification message based on the file_url_dict and
    copies the url to the clipboard.

    :param notification_message: the notification message template string
    :param file_url_dict: a dictionary with the filename and url.
    """
    msg = notification_message.format(**file_url_dict).replace("\\n", "\n")
    print(msg)

    # and send it to the clipboard :)
    pyperclip.copy(msg)


def setup_webdav_server(
    default_protocol:str ="https",
    default_server:str ="localhost",
    default_port:int =443,
    default_path: str="/",
    default_username: str=getenv("USER"),
) -> None:
    """
    Setup the webdav server authentification data.
    """
    from getpass import getpass

    print("Setup WebDAV server connection.")
    print("===============================")
    protocol = input(f"Protocol ({default_protocol}) : ") or default_protocol
    server = input(f"WebDAV server name ({default_server}): ") or default_server
    port = input(f"WebDAV server port ({default_port}): ") or default_port
    path = input(f"WebDAV server path ({default_path}): ") or default_path
    username = (
        input(f"WebDAV server username ({default_username}): ") or default_username
    )
    password = getpass("WebDAV server password: ")
    store_password(username, password, protocol, server, port, path)


def archive_files(archive_name:str , file_pattern_list: List[str]):
    """
    Stores all files listed in file_pattern_list in the archive with
    name archive_name.

    :param archive_name: the name of the archive to create
    :param file_pattern_list: a list of file pattern to archive
    """
    with tarfile.open(archive_name, mode=TAR_FILE_MODE) as tar:
        for pattern in file_pattern_list:
            for fname in glob(pattern):
                print("  Adding {} ...".format(fname))
                tar.add(fname, recursive=True)


def get_archive_name(filename: str) -> str:
    """
    Computes the archive name based on the given filename.

    :param directory: directory of the archive file
    :param filename: filename of the input file used to compute \
        the archive name
    """
    filename = filename[:-1] if filename.endswith("/") else filename
    # base result on the first filename matching pattern; this also prevents
    # wildcards in filenames :)
    archive_name = basename(glob(filename)[0])
    return archive_name


def parse_arguments() -> None:
    """prepares the argument parser"""
    parser = ArgumentParser()
    parser.add_argument("fname", help="File(s) to davify.", nargs="*", default=None)
    parser.add_argument(
        "--lifetime",
        help="Suggested file lifetime (default: '1 week'). "
        "'forever' suggests that the file is never "
        "deleted.",
        default="1 week",
    )
    parser.add_argument(
        "--retrieval-url-pattern", help="Pattern to use for the retrieval URL."
    )
    parser.add_argument(
        "--webdav-file-pattern",
        help="Pattern used to create the webdav file.",
        default=FILENAME_PATTERN,
    )
    parser.add_argument(
        "--file-url-pattern",
        help="Patterns used to retrieve the created file",
        default=FILE_URL_PATTERN,
    )
    parser.add_argument(
        "--hash",
        action="store_true",
        default=False,
        help="Add SHA1 and SHA3 checksums to the upload.",
    )
    parser.add_argument(
        "--archive-name", "-n", help="An optional file name for the created archive."
    )
    parser.add_argument("--setup", help="Setup WebDAV connection.", action="store_true")
    return parser.parse_args()


# -----------------------------------------------------------------------------
# The main program
# -----------------------------------------------------------------------------
def cli() -> None:
    args = parse_arguments()

    if not which("xclip"):
        warn(
            "Binary 'xclip' not found. Cannot copy davify URL to clipboard. "
            "Please install 'xlcip' (e.g. with sudo apt install xlip) to "
            "mitigate this problem"
        )

    pyperclip.set_clipboard("xclip")
    if args.setup:
        setup_webdav_server()
    else:
        if args.lifetime not in VALID_LIFE_TIMES:
            print(
                "Invalid lifetime - please refer to the list below for" "valid choices"
            )
            print(
                "-----------------------------------------------------" "--------------"
            )
            for valid_lifetime in VALID_LIFE_TIMES:
                print("*", valid_lifetime)
            sys.exit(-1)

        if not args.fname:
            print("No filename provided.")
            sys.exit(-1)
        elif len(args.fname) == 1 and not isdir(args.fname[0]):
            filename = args.fname[0]
            file_url_dict = upload(
                filename,
                args.lifetime,
                webdav_file_pattern=FILENAME_PATTERN,
                file_url_pattern=FILE_URL_PATTERN,
            )
        else:
            with TemporaryDirectory() as tempdirname:
                filename = os_join(
                    tempdirname,
                    args.archive_name
                    if args.archive_name
                    else get_archive_name(args.fname[0]) + TAR_FILE_EXT,
                )
                archive_files(filename, args.fname)
                file_url_dict = upload(
                    filename,
                    args.lifetime,
                    webdav_file_pattern=FILENAME_PATTERN,
                    file_url_pattern=FILE_URL_PATTERN,
                )

        if args.hash:
            sha1 = sha1(open(filename, "rb").read()).hexdigest()
            sha3 = sha3_224(open(filename, "rb").read()).hexdigest()
            file_url_dict["hash"] = HASH_PATTERN.format(sha1=sha1, sha3=sha3)
        else:
            file_url_dict["hash"] = ""

        print_notification_message(
            notification_message=MESSAGE, file_url_dict=file_url_dict
        )

if __name__ == "__main__":
    cli()
