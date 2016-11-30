from configparser import ConfigParser

from os.path import expanduser

CONFIG = ConfigParser()
CONFIG.read(expanduser('~/.davify'))

_g = lambda option, default: CONFIG.get(section='default', option=option) \
        if CONFIG.has_option(section='default', option=option) else default

FILENAME_PATTERN = _g('filename_pattern', '{random_prefix}{lifetime_str}-{fname}{version_suffix}{ext}')
FILE_URL_PATTERN = _g('file_url_pattern', '{protocol}://{file_server}{file_path}{random_prefix}{lifetime_str}-{fname}{version_suffix}{ext}')
MESSAGE = _g('notification_message', '{url}\n(Note: The file will be availalbe for {lifetime}.)')
EXTRACT_LIFETIME_STR = _g('extract_lifetime_str', r'\w{4}(\w{1})-.*')
