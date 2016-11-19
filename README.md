## davify 
Uploads files to a WebDAV server for retrieval via https.

## The problem davify solves
Sending document versions to collaborators is often quite cumbersome. 
Davify (i) uploads files to your webdav server, (ii) provides a publicly available download link, and (iii) copies this information
into the clipboard.

In addition it keeps track of a file's lifetime and provides scripts for automatically removing files once their lifetime has expired.

## Command line paramters
```bash
usage: __init__.py [-h] [--lifetime LIFETIME]
                   [--retrieval-url-pattern RETRIEVAL_URL_PATTERN]
                   [--webdav-file-pattern WEBDAV_FILE_PATTERN]
                   [--file-url-pattern FILE_URL_PATTERN] [--clean-directory]
                   [--setup]
                   [fname [fname ...]]

positional arguments:
  fname                 File to davify or directory to clean.

optional arguments:
  -h, --help            show this help message and exit
  --lifetime LIFETIME   Suggested file lifetime in hours (default: 1 week).
                        Zero suggests that the file is never deleted.
  --retrieval-url-pattern RETRIEVAL_URL_PATTERN
                        Pattern to use for the retrieval URL.
  --webdav-file-pattern WEBDAV_FILE_PATTERN
                        Pattern used to create the webdav file.
  --file-url-pattern FILE_URL_PATTERN
                        Patterns used to retrieve the created file
  --clean-directory     Remove outdated files from the given directory.
  --setup               Setup WebDAV connection.
```

## Example call: 

```
albert@myhost:~$ python __init__.py transform.py
https://mydav.net/qOMvcO/transform-15dez-0201.py
(Note the file will be available for 168 hours.)
```

## Setup and configuration files:
Setup the WebDAV server with
```bash
python3 __init__.py --sestup
```

Davify's configuration resides in `~/.davify`. Please find below an example configuration file.

```
[default]
filename_pattern = {random_prefix}{lifetime_str}-{fname}{version_suffix}{ext}
extract_lifetime_str = \w{4}(\w{2})-.*
file_url_pattern = {protocol}://example.net/{random_prefix}{lifetime_str}-{fname_quoted}{version_suffix}{ext}
notification_message = {url}\n(Note the file will be available for {hours} hours.)`
```
