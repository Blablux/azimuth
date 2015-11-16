#!/usr/bin/python

# This script is used to crop mobile screenshots from their upper and lower
# margin, leaving only the application visible.
# Required modules: Image (for obvious reasons), sys for arguments parsing
# and os for filename manipulation.
from PIL import Image
import os.path, argparse

parser = argparse.ArgumentParser(version='0.1')
parser.add_argument('image')
parser.add_argument('-u', default=75, help='height of the notification area')
parser.add_argument('-l', default=144, help='height of the virtual buttons area')
results = parser.parse_args()

# Check if an image (jpg or png for the sake of simplicity) is provided
if os.path.isfile(results.image) is False:
    parser.error("The file %s does not exist!" % results.image)
name, ext = os.path.splitext(results.image)
if ext != '.png' and ext != '.jpg':
    parser.error("The file %s is not an image!" % results.image)

# Cropping image
im = Image.open(results.image)
lower_margin = im.size[1] - results.l
# HINT: crop(left,up,right,down)
region = im.crop( (0,results.u,im.size[0],lower_margin) )
newfilename = name + '.cropped' + ext
region.save(newfilename)
