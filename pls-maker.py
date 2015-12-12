#!/usr/bin/env python

"""Create ``.pls`` playlists from music filenames.

Specify a path to be recursively searched for music files.
"""

from itertools import ifilter
import os.path # TODO : Use pathlib ?
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
    for r, d, f in os.walk(normalize(path)):
        for fn in ifilter(pattern.search, f):
            yield os.path.join(r, fn)

def create_playlist(f, p, a):
    # Create a PLS playlist from filenames.
    playlist = '[playlist]\n\n'
    num = 0
    # if playlist already exists, add it to the content
    if os.path.isfile(p):
        pls = open(normalize(p), "r")
        content = pls.read().split('\n\n')
        pls.close()
        del content[0]
        del content[-1]
        for e in content:
            playlist += str(e + '\n\n')
            num+=1
    entry = (
        'File%d=%s\n'
        'Title%d=%s\n'
        'Length%d=%s\n\n')
    for filename in f:
        num += 1
        title, length = get_file_info(filename)
        if a == True:
            filepath = normalize(filename)
        else:
            filepath = os.path.relpath(normalize(filename), normalize(os.path.dirname(p)))
        playlist += entry % (num, filepath, num, title, num, length)
    playlist += (
        'NumberOfEntries=%d\n'
        'Version=2\n') % num
    return playlist

def get_file_info(f):
    # Get needed information from file
    name, ext = os.path.splitext(os.path.basename(f))
    if ext.lower() == '.mp3':
        track = MP3(f)
        data = ID3(f)
        title = data["TIT2"].text[0]
    elif ext.lower() == '.ogg':
        track = OggVorbis(f)
        title = str(track.get("title")).strip('[u"\']')
    elif ext.lower() == '.flac':
        track = FLAC(f)
        title = str(track.get("title")).strip('[u"\']')
    return title, int(track.info.length)

def normalize(p):
    if str(p[:1]) == '~':
        return os.path.expanduser(p)
    else:
        return os.path.abspath(p)

if __name__ == '__main__':
    if os.path.isdir(args.source):
        filenames = find_files(args.source)
    elif os.path.isfile(args.source):
        filenames = [args.source]
    else:
        exit('Error: invalid music path provided')
    # create the playlist BEFORE opening the file in write mode!
    content = create_playlist(filenames, args.output, args.absolute)
    playlist = open(args.output,"w")
    playlist.write(content)
    playlist.close()
