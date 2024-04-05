from configparser import ConfigParser

from os.path import expanduser

CONFIG = ConfigParser()
CONFIG.read(expanduser("~/.davify"))

_g = (
    lambda option, default: CONFIG.get(section="default", option=option)
    if CONFIG.has_option(section="default", option=option)
    else default
)

FILENAME_PATTERN = _g(
    "filename_pattern", "{random_prefix}{lifetime_str}-{fname}{version_suffix}{ext}"
)
FILE_URL_PATTERN = _g(
    "file_url_pattern",
    "{protocol}://{file_server}{file_path}{random_prefix}{lifetime_str}-{fname}{version_suffix}{ext}",
)
HASH_PATTERN = _g("hash_pattern", "Hash (SHA1): {sha1}\nHash (SHA3): {sha3}\n")
MESSAGE = _g(
    "notification_message",
    "{url}\n{hash}(Note: The file will be availalbe for {lifetime}.)",
)
EXTRACT_LIFETIME_STR = _g("extract_lifetime_str", r"[a-zA-Z0-9_-]{4}([a-zA-Z0-9_-])-.*")
