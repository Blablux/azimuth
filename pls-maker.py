#!/usr/bin/env python

"""Create ``.pls`` playlists from music filenames.

Specify a path to be recursively searched for music files.
"""

from itertools import ifilter
import os.path
import re
import argparse
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis
from mutagen.mp3 import MP3
from mutagen.id3 import ID3

parser = argparse.ArgumentParser(description=__doc__, version='0.1')

parser.add_argument("source", help="Specify the file / directory to add.")
parser.add_argument("output",
                    help="Specify the file to write the playlist in.")
parser.add_argument("-a", "--absolute",
                    help="Write absolute paths instead of relatives.",
                    action="store_true")

args = parser.parse_args()

pattern = re.compile('\.(mp3|ogg|flac)$', re.I)

def find_files(path):
    # Return all matching files beneath the path.
    for r, d, f in os.walk(os.path.abspath(path)):
        for fn in ifilter(pattern.search, f):
            yield os.path.join(r, fn)

def create_playlist(filenames):
    # Create a PLS playlist from filenames.
    yield '[playlist]\n\n'
    num = 0
    entry = (
        'File%d=%s\n'
        'Title%d=%s\n'
        'Length%d=%s\n\n')
    for filename in filenames:
        num += 1
        title, length = get_file_info(filename)
        yield entry % (num, filename, num, title, num, length)

    yield (
        'NumberOfEntries=%d\n'
        'Version=2\n') % num

def get_file_info(filename):
    # Get needed information from file
    name, ext = os.path.splitext(os.path.basename(filename))
    if ext.lower() == '.mp3':
        track = MP3(filename)
        data = ID3(filename)
        title = data["TIT2"].text[0]
    elif ext.lower() == '.ogg':
        track = OggVorbis(filename)
        title = str(track.get("title")).strip('[u"]')
    elif ext.lower() == '.flac':
        track = FLAC(filename)
        title = str(track.get("title")).strip('[u"]')
    return title, int(track.info.length)

if __name__ == '__main__':

    if str(args.source[:1]) == '~':
        source = os.path.expanduser(args.source)
    else:
        source = os.path.abspath(args.source)
    if os.path.isfile(args.source):
        path = os.path.dirname(source)
    else:
        path = source

    filenames = find_files(args.source)

    playlist = open(args.output,"w")

    map(playlist.write, create_playlist(filenames))

    playlist.close()
