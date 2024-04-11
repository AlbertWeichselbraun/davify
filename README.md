## davify 
Uploads files to a WebDAV server for retrieval via https.

## The problem davify solves
Sending document versions to collaborators is often quite cumbersome. 
Davify (i) uploads files to your WebDAV server (multiple files and directories are put into a .txz archive prior to uploading), (ii) provides a publicly available download link, and (iii) copies this information
into the clipboard.

In addition it keeps track of a file's lifetime and provides scripts for automatically removing files once their lifetime has expired.

## Setup and configuration files:

### Installation

```bash
pipx install davify
```

### Client configuration:
Setup the WebDAV client with
```bash
davify --setup
```
Davify's configuration resides in `~/.davify` and the WebDAV server credentials are stored in your system's keystore. Please find below an example configuration file.

```
[default]
filename_pattern = {random_prefix}{lifetime_str}-{fname}{version_suffix}{ext}
file_url_pattern = {protocol}://example.net/{random_prefix}{lifetime_str}-{fname_quoted}{version_suffix}{ext}
notification_message = {url}\n(Note the file will be available for {lifetime}.)`
```

### Server configuration
Calling `clean-davify-directory` on the server removes expired files. Note that you need to provide the full path to the `clean-davify-directory` binary (use `which clean-davify-directory` to obtain the path).

Example crontab entry:
```cron
# clean davify directory
15 00   * * *   www-data  /root/.local/bin/clean-davify-directory /var/www/davify
```
## Command line parameters
```bash
usage: davify [-h] [--lifetime LIFETIME]
                   [--retrieval-url-pattern RETRIEVAL_URL_PATTERN]
                   [--webdav-file-pattern WEBDAV_FILE_PATTERN]
                   [--file-url-pattern FILE_URL_PATTERN] 
                   [--archive-name ARCHIVE_NAME] [--setup]
                   [fname [fname ...]]

positional arguments:
  fname                 File(s) to davify or directory to upload.

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
  --archive-name ARCHIVE_NAME, -n ARCHIVE_NAME
                        An optional file name for the created archive.
  --setup               Setup WebDAV connection.
```

## Example call: 

```
albert@myhost:~$ davify transform.py
https://example.net/qOMvcO/transform-15dez-0201.py
(Note the file will be available for 1 week.)
```

