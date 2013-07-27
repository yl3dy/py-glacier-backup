#!/usr/bin/python2

"""Amazon Glacier backup management tool."""

from credentials import *
from argparse import ArgumentParser
from time import strftime
from boto.glacier.layer2 import Layer2
from boto.glacier.concurrent import ConcurrentDownloader

CHUNK_SIZE = 32  # MB
MB = 1024 * 1024

def upload(vault, filename):
    """Upload a file."""
    desc = '{}, uploaded at {}'.format(filename, strftime('%Y-%m-%d'))
    return vault.concurrent_create_archive_from_file(filename, desc,
                                                     part_size=CHUNK_SIZE*MB)

def notify_download(vault, archive_id):
    """Notify Glacier about backup download."""
    return vault.retrieve_archive(archive_id).get_output()

def download(vault, job_id, filename='archive.tar.gz.gpg'):
    """Actually download the archive from Glacier."""
    download_job = vault.get_job(job_id)
    return ConcurrentDownloader(download_job, CHUNK_SIZE*MB).download(filename)

def remove(vault, archive_id):
    """Remove an archive from Glacier."""
    return vault.delete_archive(VAULT_NAME, archive_id)

def list_jobs(vault):
    """List all jobs on Glacier."""
    return vault.list_jobs(VAULT_NAME)

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
    parser.add_argument('--download-to', type=str)
    args = parser.parse_args()

    vault = Layer2(aws_access_key_id=AMAZON_LOGIN,
                   aws_secret_access_key=AMAZON_PASSWORD,
                   region_name='eu-west-1').get_vault(VAULT_NAME)

    if args.notify:
        print('Job {}'.format(notify_download(vault, args.notify)))
    elif args.download:
        print('Download checksum: {}'.format(download(vault,
                                                      args.download,
                                                      args.download_to)))
    elif args.remove:
        remove(vault, args.remove)
        print('Removed archive {}'.format(args.remove))
    elif args.upload:
        print('{}: {}'.format(args.upload, upload(vault, args.upload)))
    else:
        print(list_jobs(vault))

if __name__ == '__main__':
    main()
