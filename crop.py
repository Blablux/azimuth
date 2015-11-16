#!/usr/bin/python

# This script is used to crop mobile screenshots from their upper and lower
# margin, leaving only the application visible.
# Required modules: Image (for obvious reasons), sys for arguments parsing
# and os for filename manipulation.
from PIL import Image
import sys, os.path, argparse

# Check if an image (jpg or png for the sake of simplicity) is provided
if os.path.isfile(sys.argv[-1]) is False:
    print 'No file provided'
    exit()
    # TODO: Do not exit > help
name, ext = os.path.splitext(sys.argv[-1])
if ext != '.png' and ext != '.jpg':
    print 'File provided is not an image'
    exit()

# Parse other arguments
if len(sys.argv) > 2:
    # DEBUG:
    print 'Found ' + str(len(sys.argv) - 2) + ' parameters.'
    param_list = list(sys.argv[1:-1])
    print str(param_list)
else:
    print 'Found no parameters'

# HINT: Default margin values.
upper_margin = 75
lower_margin = im.size[1] - 144

# Cropping image
im = Image.open(sys.argv[-1])
# HINT: crop(left,up,right,down)
#region = im.crop( (0,upper_margin,im.size[0],lower_margin) )
newfilename = name + '.cropped' + ext
#region.save(newfilename)
