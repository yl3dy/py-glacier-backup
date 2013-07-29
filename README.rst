============================
Amazon Glacier backup script
============================

Features:

* uploading, downloading, removing an archive to/from Amazon Glacier;
* wrapper script to form encrypted archive and upload it.

For uploading an archive to Glacier, use ``cold_backup.sh`` (help in comments).
For retrieval and removal, use ``glacier_backup.py`` directly.

Always remember to save inventory (i.e., IDs of uploaded archives)! By default
``cold_backup.sh`` appends IDs to special file ``$INVENTORY``.

Configuration
-------------

Create ``credentials.py``, where set variables ``AMAZON_LOGIN`` (your Amazon key id),
``AMAZON_PASSWORD`` (Amazon secret key) and ``VAULT_NAME``. Also you're likely to
change paths in ``cold_backup.sh``.

Dependencies
------------

* Python 2.7
* boto
* bash
* GnuPG

Copyleft 2013 by Alexander Kiselyov, license GPLv3+ (http://www.gnu.org/licenses/gpl-3.0.html).
