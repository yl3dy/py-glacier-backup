#!/usr/bin/python2

from credentials import *
from argparse import ArgumentParser
from boto.glacier.layer1 import Layer1
from time import strftime

def upload(filename):
    """Upload a file."""
    desc = '{}, uploaded at {}'.format(filename, strftime('%Y-%m-%d'))
    return desc

def notify_download(idnum):
    """Notify Glacier about backup download."""
    pass

def download(job_id):
    """Actually download an archive from Glacier."""
    pass

def remove(idnum):
    """Remove an archive from Glacier."""
    pass

def main():
    """Main routine."""
    parser = ArgumentParser(description='Amazon Glacier console backup tool')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-u', '--upload', action='store_true')
    group.add_argument('-n', '--notify', action='store_true',
                       help='notify Glacier about backup retrieval')
    group.add_argument('-d', '--download', action='store_true',
                       help='actually download archive')
    group.add_argument('-r', '--remove', action='store_true')
    parser.add_argument('entity_id', type=str,
                        help='file to backup/archive id/job id')
    args = parser.parse_args()
    if args.notify:
        print('Download of archive {}: job {}'.format(args.entity_id,
                                                     download(args.entity_id)))
    elif args.download:
        print(download(args.entity_id))
    elif args.remove:
        remove(args.entity_id)
        print('Removed archive {}'.format(args.entity_id))
    else:           # Upload is the default action
        print('{}: {}'.format(args.entity_id, upload(args.entity_id)))

if __name__ == '__main__':
    main()
