## davify 
- uploads files to a webdav server for retrieval via https

## The problem davify solves
Sending document versions to collaborators is often quite cumbersome. 
Davify (i) uploads files to your webdav server, (ii) provides a publicly available download link, and (iii) copies this information
into the clipboard.

In addition it keeps track of a file's lifetime and provides scripts for automatically removing files once their lifetime has expired.


## Example call: 

```
albert@myhost:~$ python __init__.py transform.py
https://mydav.net/qOMvcO/transform-15dez-0201.py
(Note the file will be available for 168 hours.)
```

