#!/usr/bin/python2

from credentials import *
from argparse import ArgumentParser
from time import strftime
from boto.glacier.layer1 import Layer1
from boto.glacier.concurrent import ConcurrentUploader
import json

UPLOAD_CHUNK_SIZE = 32  # MB

def upload(connection, filename):
    """Upload a file."""
    desc = '{}, uploaded at {}'.format(filename, strftime('%Y-%m-%d'))
    return ConcurrentUploader(connection, VAULT_NAME,
                              UPLOAD_CHUNK_SIZE*1024*1024).upload(filename,
                                                                  filename)

def notify_download(archive_id):
    """Notify Glacier about backup download."""
    request_info = {'ArchiveId': archive_id, 'Format': 'JSON',
                    'Type': 'archive-retrieval'}
    return str(connection.initiate.job(VAULT_NAME, request_info))

def download(connection, job_id):
    """Actually download an archive from Glacier."""
    return connection.get_job_output(VAULT_NAME, job_id)

def remove(connection, archive_id):
    """Remove an archive from Glacier."""
    return connection.delete_archive(VAULT_NAME, archive_id)

def list_jobs(connection):
    """List all jobs on Glacier."""
    return connection.list_jobs(VAULT_NAME)

def main():
    """Main routine."""
    parser = ArgumentParser(description='Amazon Glacier console backup tool')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--upload', type=str, metavar='FILENAME')
    group.add_argument('--notify', type=str, metavar='ARCHIVE_ID',
                       help='notify Glacier about backup retrieval')
    group.add_argument('--download', type=str, metavar='JOB_ID',
                       help='actually download archive')
    group.add_argument('--remove', type=str, metavar='ARCHIVE_ID')
    args = parser.parse_args()

    #connection = Layer1(aws_access_key=AMAZON_LOGIN,
    #                    aws_secret_access_key=AMAZON_PASSWORD)
    connection = None

    if args.notify:
        print('{}: job {}'.format(args.entity_id,
                                  download(connection, args.entity_id)))
    elif args.download:
        print('Download checksum: {}'.format(download(connection,
                                                      args.entity_id)))
    elif args.remove:
        remove(connection, args.entity_id)
        print('Removed archive {}'.format(args.entity_id))
    elif args.upload:
        print('{}: {}'.format(args.entity_id, upload(connection,
                                                     args.entity_id)))
    else:
        print(list_jobs(connection))

if __name__ == '__main__':
    main()
