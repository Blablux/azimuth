#!/usr/bin/env python

"""Create ``.pls`` playlists from music filenames.

Specify a path to be recursively searched for music files.
"""

from itertools import ifilter
import os.path
import re
import argparse

parser = argparse.ArgumentParser(
    description=__doc__)

parser.add_argument("source", help="Specify the file / directory to add.")
parser.add_argument("output",
                    help="Specify the file to write the playlist in.")
parser.add_argument("-a", "--absolute",
                    help="Write absolute paths instead of relatives.",
                    action="store_true")

args = parser.parse_args()

PATTERN = re.compile('\.(mp3|ogg|flac)$', re.I)

def find_files(path):
    # Return all matching files beneath the path.
    for r, d, f in os.walk(os.path.abspath(path)):
        for fn in ifilter(PATTERN.search, f):
            yield os.path.join(r, fn)

def create_playlist(filenames):
    # Create a PLS playlist from filenames.
    yield '[playlist]\n\n'
    num = 0

    entry = (
        'File%d=%s\n'
        'Title%d=%s\n'
        'Length%d=-1\n\n') # TODO: get length
    for filename in filenames:
        num += 1
        title = os.path.splitext(os.path.basename(filename))[0]
        yield entry % (num, filename, num, title, num)

    yield (
        'NumberOfEntries=%d\n'
        'Version=2\n') % num

if __name__ == '__main__':
    filenames = find_files(args.source)

    playlist = open(args.output,"w")

    map(playlist.write, create_playlist(filenames))

    playlist.close()
