#!/usr/bin/python

# This script is used to crop mobile screenshots from their upper and lower
# margin, leaving only the application visible.
# Required modules: Image (for obvious reasons), argparse for arguments parsing
# and os for filename manipulation.
from PIL import Image
import os.path, argparse

parser = argparse.ArgumentParser(version='0.1')
parser.add_argument('image', nargs='+')
parser.add_argument('-u', default=75, type=int,
                    help='height of the notification area')
parser.add_argument('-l', default=144, type=int,
                    help='height of the virtual buttons area')
results = parser.parse_args()

# Check if an image (jpg or png for the sake of simplicity) is provided
for filename, elem in enumerate(results.image):
    if os.path.isfile(elem) is False:
        parser.error("The file %s does not exist!" % elem)
    name, ext = os.path.splitext(elem)
    if ext != '.png' and ext != '.jpg':
        parser.error("The file %s is not an image!" % elem)

    # Cropping image
    im = Image.open(elem)
    # HINT: crop(left,up,right,down)
    region = im.crop( (0,results.u,im.size[0],im.size[1] - results.l) )
    newfilename = name + '.cropped' + ext
    region.save(newfilename)
    #DEBUG:
    #print "new filename " + newfilename
