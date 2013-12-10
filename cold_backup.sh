#!/bin/bash

# Cold backups using Amazon Glacier
# Arguments: directory_name

if [ -z "$1" ]; then
    echo Not enough arguments
    exit -1
fi

BACKUP_DIR="/mnt/data/$1"
SHORT_NAME="$1"
TMP_DIR=/mnt/data/backup/glacier/tmp
BACKUP_ARCHIVE="${SHORT_NAME}_`date +%Y-%m-%d`.tar.gz"
INVENTORY=/mnt/data/system/backup/glacier/inventory

echo "[`date`] Archiving the directory"
cd $TMP_DIR
tar czf $BACKUP_ARCHIVE $BACKUP_DIR

echo "[`date`] Encrypting the archive"
#gpg --symmetric --force-mdc --sign $BACKUP_ARCHIVE
openssl enc -aes256 -in ${BACKUP_ARCHIVE} -out ${BACKUP_ARCHIVE}.aes

echo "[`date`] Uploading to Glacier"
../glacier_backup.py --upload ${BACKUP_ARCHIVE}.aes >> $INVENTORY

cd -
rm $TMP_DIR/*
echo "[`date`] Done"
