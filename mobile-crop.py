#!/usr/bin/python
"""This script is used to crop mobile screenshots from their upper and lower
    margin, leaving only the application visible. Require modules `PIL`,
    `argparse` and `os`.

"""
from PIL import Image
import os.path, argparse

parser = argparse.ArgumentParser(description=__doc__, version='0.1')
parser.add_argument('image', nargs='+')
parser.add_argument('-u', '--upper', default=75, type=int,
                    help='Set the height of the notification area (defaults to 75)')
parser.add_argument('-l', '--lower', default=144, type=int,
                    help='Set the height of the virtual buttons area (defaults to 144)')
parser.add_argument('-i', '--ignore', choices=['up', 'down', 'both', 'none'],
                    default='none',
                    help='Ignore none, upper, lower or both margins (overrides custom heights)')
args = parser.parse_args()

# Check if an image (jpg or png for the sake of simplicity) is provided
for f, e in enumerate(args.image):
    if os.path.isfile(e) is False:
        parser.error("The file %s does not exist!" % e)
        exit(1)
    name, ext = os.path.splitext(e)
    if ext != '.png' and ext != '.jpg':
        parser.error("The file %s is not an image!" % e)
        exit(1)

    # Calculating cropping box
    if args.ignore:
        if args.ignore == 'up' or args.ignore == 'both':
            print "ignoring upper margin"
            u = 0
        else:
            u = args.upper
        if args.ignore == 'down' or args.ignore == 'both':
            print "ignoring lower margin"
            l = 0
        else:
            l = args.lower

    # Cropping image
    im = Image.open(e)

    # HINT: crop(left,up,right,down)
    r = im.crop( (0,u,im.size[0],im.size[1] - l) )
    newfilename = name + '.cropped' + ext
    r.save(newfilename)
    # DEBUG:
    # print "new filename :" + newfilename
    # print "boxed : 0 " + str(u) + " " + str(im.size[0]) + " " + str(im.size[1] - l)
