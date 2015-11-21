# Faustus

Faustus is a small python script to automatically crop mobile screenshots to
remove the notification bar and the virtual buttons.

The script doesn't do much right now, as it is more a sandbox for me to
(re)learn Python programming.

## Required modules

+ PIL
+ os.path
+ argparse

## Usage

__Usage:__

usage: crop.py [-h] [-v] [-u UPPER] [-l LOWER] [-i {up,down,both,none}]
               image [image ...]

__Positional arguments:__

    image

__Optional arguments:__

-h, --help            show this help message and exit
-v, --version         show program's version number and exit
-u UPPER, --upper UPPER
                      Set the height of the notification area (defaults to
                      75)
-l LOWER, --lower LOWER
                      Set the height of the virtual buttons area (defaults
                      to 144)
-i {up,down,both,none}, --ignore {up,down,both,none}
                      Ignore none, upper, lower or both margins (overrides
                      custom heights)

## Side Note

Faustus is minor NPC from the video games
[Legacy of Kain](https://en.wikipedia.org/wiki/Legacy_of_Kain).
