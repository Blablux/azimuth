#!/usr/bin/env python

"""Create ``.cbz`` zip files from multiple directories.

Specify a path to be recursively searched for files.
"""

from itertools import ifilter
import os
import re
import argparse
import zipfile
import shutil

parser = argparse.ArgumentParser(description=__doc__, version='0.1')

parser.add_argument("source", help="Specify the directory to search.")
parser.add_argument("-z", "--zip",
                    help="Keep zip extension.",
                    action="store_true")
args = parser.parse_args()
pattern = re.compile('\.(png|jpg)$', re.I)


def compress_files(name, mode):
    arc = name + '.cbz' if not mode else name + '.zip'
    cbz = zipfile.ZipFile(arc, 'w')
    for r, d, f in os.walk(name):
        for fn in ifilter(pattern.search, f):
            cbz.write(os.path.join(r, fn), arcname=fn,
                      compress_type=zipfile.ZIP_DEFLATED)
    cbz.close()
    shutil.move('./' + name, os.path.expanduser('~/.local/share/Trash/files'))

if __name__ == '__main__':
    mode = True if args.zip else False
    os.chdir(args.source)
    for r, d, f in os.walk(args.source):
        for z in d:
            archive = compress_files(z, mode)
