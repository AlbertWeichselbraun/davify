#!/usr/bin/env python

import gnomekeyring as gk
from glib import set_application_name
from urlparse import urlparse
from collections import namedtuple

APPLICATION_NAME = 'davify'
set_application_name(APPLICATION_NAME)

FileStorage = namedtuple('FileStorage', 'username password protocol server port path')


def store_password(username, pwd, protocol, server, service, port, path, application_name):
    '''
    stores the given password in the gnome keyring
    '''
    if application_name not in gk.list_keyring_names_sync():
        gk.create_sync(application_name, application_name)

    atts = {'application': application_name,
            'username': username,
            'server': server,
            'protocol': protocol,
            'service': service,
            'port': str(port),
            'path': path,
           }
    description = '%(protocol)s://%(username)s@%(server)s:%(port)s/%(path)s' % (atts)
    gk.item_create_sync(application_name, gk.ITEM_GENERIC_SECRET,
            description, atts, pwd, True)

def get_passwords(application_name):
    '''
    retrieves the stored login data from the keyring
    '''
    gk.unlock_sync(application_name, application_name)
    results = []
    for item_no in gk.list_item_ids_sync(application_name):
        item_info = gk.item_get_info_sync(application_name, item_no)
        results.append(_parse_item_info(item_info))

    gk.lock_sync(application_name)
    return results

def _parse_item_info(item_info):
    url_info = urlparse(item_info.get_display_name())
    user, server = url_info.netloc.split('@')
    server, port = server.split(':')
    return FileStorage(username=user, password=item_info.get_secret(), 
        protocol=url_info.scheme, server=server, port=port, path=url_info.path)



if __name__ == '__main__':
    #store_password('albert-davify', 'test', 'https', 'cloud.weichselbraun.net',
    #               'webdav', '443', 'dav/davify', APPLICATION_NAME)
    print(get_passwords(APPLICATION_NAME))
