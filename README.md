# Faustus

Faustus is a small python script to automatically crop mobile screenshots to
remove the notification bar and the virtual buttons.

The script doesn't do much right now, as it is more a sandbox for (re)learning
Python programming.

## Required modules

+ PIL
+ sys
+ os.path
+ argparse

## Usage

__Usage:__

    crop.py [-h] [-v] [-u U] [-l L] image

__Positional arguments:__

    image

__Optional arguments:__

    -h, --help     show this help message and exit  
    -v, --version  show program's version number and exit  
    -u U           height of the notification area  
    -l L           height of the virtual buttons area

## Side Note

Faustus is minor NPC from the video game _Legacy of Kain_.
