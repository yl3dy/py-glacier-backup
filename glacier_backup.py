#!/usr/bin/python

from credentials import *
from argparse import ArgumentParser
from boto.glacier.layer2 import Layer2
from time import strftime

#MY_VAULT = Layer2(aws_access_key_id=AMAZON_LOGIN,
                  #aws_secret_access_key=AMAZON_PASSWORD).get_vault(VAULT_NAME)

def upload(filename):
    """Upload a file."""
    desc = '{}, uploaded at {}'.format(filename, strftime('%Y-%m-%d'))
    #return MY_VAULT.concurrent_create_archive_from_file(filename, desc)
    return desc

def download(idnum):
    """Notify Glacier about backup download."""
    pass

def main():
    """Main routine."""
    parser = ArgumentParser(description='Amazon Glacier console backup tool')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-u', '--upload', action='store_true')
    group.add_argument('-d', '--download', action='store_true')
    parser.add_argument('filename', type=str,
                        help='name of file to backup/restore')
    args = parser.parse_args()
    if not args.download:
        print('{}: {}'.format(args.filename, upload(args.filename)))
    else:
        download(args.filename)

if __name__ == '__main__':
    main()
