#!/usr/bin/env python
import os
import time


class SrvBackup:
    """Class for maintaing a complete server backup"""

    def __init__(self, path):
        self.backupdir = path

    def DbDump(user, password, database, host="localhost"):
        filestamp = time.strftime('%Y-%m-%d-%I:%M')
        os.popen("mysqldump -u %s -p%s -h %s -e --opt -c %s | gzip -c > %s.gz"
                 % (user, password, host, database, database + "_" +
                    filestamp))
        print "dump file in " + database + "_" + filestamp + ".gz --"

if __name__ == "__main__":
    process = SrvBackup('/')
    process.DbDump()
