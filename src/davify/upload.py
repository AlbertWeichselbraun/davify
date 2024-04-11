#!/usr/bin/env python

"""
Upload files to a WebDAV server.
"""

from requests import put
from requests.exceptions import RequestException

HEADERS = {"Content-Type": "application/octet-stream"}


def upload_to_webdav(data: bytes, url: str, username: str, password: str) -> None:
    response = put(url, data=data, headers=HEADERS, auth=(username, password))
    if response.status_code != 201:
        raise RequestException(
            f"Failed to upload file. Status code: {response.status_code}"
            f"Response: {response.text}"
        )
