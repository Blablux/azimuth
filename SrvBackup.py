#!/usr/bin/env python
import os
import time
from sh import rsync


class SrvBackup:
    """Class for maintaing a complete server backup"""

    def __init__(self, path):
        self.hostname = os.uname()[1]
        self.backupdir = self.Normalize(os.path.join(path, self.hostname))
        if not os.path.exists(self.backupdir):
            try:
                os.makedirs(self.backupdir)
            except:
                raise

    def Normalize(p):
        """Normalize Unix paths"""
        if str(p[:1]) == '~':
            return os.path.expanduser(p)
        else:
            return os.path.abspath(p)

    def DbDump(self, user, password, database, host="localhost"):
        """Do a mysqldump of a database and store it as an archive"""
        filestamp = time.strftime('%Y-%m-%d-%I:%M')
        os.popen("mysqldump -u %s -p%s -h %s -e --opt -c %s | gzip -c > %s.gz"
                 % (user, password, host, database,
                    os.path.join(self.backupdir, database + "_" + filestamp)
                    )
                 )
        print "dumped file in " + database + "_" + filestamp + ".gz"

    def Rsync(self, directories):
        """Syncing directories (supplied as a list) to the backupdir"""
        for directory in directories:
            if not os.path.exists(self.Normalize(directory)):
                print()
            else:
                rsync("-av", self.Normalize(directory), self.backupdir)

    def ReadCfg(self, cfgfile):
        with open(self.Normalize(cfgfile), 'r') as config:
            return eval(config.read())


if __name__ == "__main__":
    process = SrvBackup('/nfs/backup')
    process.DbDump()
