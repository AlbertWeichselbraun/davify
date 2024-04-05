#!/usr/bin/env python

"""
Handles access to the WebDAV's server creditentials.
"""

from collections import namedtuple

import secretstorage

APPLICATION_NAME = "davify"
FileStorage = namedtuple("FileStorage", "username password protocol server port path")


def get_secret_storage():
    bus = secretstorage.dbus_init()
    return secretstorage.get_default_collection(bus)


def store_password(username, pwd, protocol, server, port, path):
    """
    stores the given password in the gnome keyring
    """
    secret_storage = get_secret_storage()
    attrs = {
        "application": APPLICATION_NAME,
        "username": username,
        "server": server,
        "protocol": protocol,
        "port": str(port),
        "path": path,
    }
    description = (
        f"davify WebDAV password for <{protocol}://{username}@"
        "{server}:{port}/{path}>"
    )
    secret_storage.create_item(description, attrs, pwd.encode("utf-8"))


def get_passwords():
    """
    retrieves the stored login data from the keyring
    """
    secret_storage = get_secret_storage()
    if secret_storage.is_locked():
        secret_storage.unlock()

    items = [
        _parse_item(item)
        for item in secret_storage.search_items({"application": APPLICATION_NAME})
    ]

    return items


def _parse_item(item):
    item_attr = item.get_attributes()
    return FileStorage(
        username=item_attr["username"],
        password=item.get_secret().decode("utf-8"),
        protocol=item_attr["protocol"],
        server=item_attr["server"],
        port=item_attr["port"],
        path=item_attr["path"],
    )


if __name__ == "__main__":
    print(get_passwords())
