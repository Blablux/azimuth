#!/usr/bin/env python
import requests
import bs4
from PIL import Image
import os.path
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000


class Dmc:
    """Class aimed at converting images (mostly pixel
    art) to DMC colors for cross stitching."""

    def __init__(self):
        self.table = {}
        self.depth = 128

    def Normalize(self, p):
        """Normalize Unix paths"""
        if str(p[:1]) == '~':
            return os.path.expanduser(p)
        else:
            return os.path.abspath(p)

    def FetchOnline(self):
        """Gets the remote page and load it in BeautifulSoup."""
        res = requests.get('')  # CONFIGURE: Add the URL to fetch
        res.raise_for_status()
        self.content = bs4.BeautifulSoup(res.text)
        for row in self.content.select('table.tableborder tr'):
            try:
                cell = row.select('td')
                self.CreateDict(cell)
            except IndexError:
                pass

    def CreateDict(self, cell):
        """Subtask to create the supported colors palette."""
        self.table[cell[0].get_text()] = {'name': cell[1].get_text(),
                                          'R': cell[2].get_text(),
                                          'G': cell[3].get_text(),
                                          'B': cell[4].get_text(),
                                          'hex': cell[5].get_text()}

    def SaveLocal(self, location):
        """Save color palette to a file for further use"""
        try:
            save = open(self.Normalize(location), 'w')
            save.write(str(self.table))
            save.close()
        except OSError as e:
            print ('Error opening the file ', location)
            print (e)

    def FetchLocal(self, location):
        """Load palette from a previously saved file"""
        with open(self.Normalize(location), 'r') as table:
            self.table = eval(table.read())

    def GetImgColors(self, location):
        """List all colors from an image"""
        try:
            img = Image.open(self.Normalize(location), 'r')
            self.colors = img.getcolors(self.depth)
            while self.colors is None:
                self.depth *= 2
                self.colors = img.getcolors(self.depth)

        except OSError as e:
            print ('Error opening the file ', location)
            print (e)

    def FindColorDelta(self, color):
        closestColor = 255
        n = 0
        for key, values in self.table.items():
            orgColor = sRGBColor(color[0], color[1], color[2], True)
            dmcColor = sRGBColor(int(values['R']),
                                 int(values['G']),
                                 int(values['B']),
                                 True)
            initLab = convert_color(orgColor, LabColor)
            dmcLab = convert_color(dmcColor, LabColor)
            delta = delta_e_cie2000(initLab, dmcLab)
            if delta < closestColor:
                closestColor = delta
                closestValue = values['name']
                closestRGB = (int(values['R']),
                              int(values['G']),
                              int(values['B']))
                n = 0
            elif delta == closestColor:
                # TODO: Handling when we have two or more identical delta
                n += 1
        return closestValue, closestRGB

    def Initiate(self):
        """Launches the full script"""
        self.FetchOnline()
        self.GetImgColors('')  # CONFIGURE: Add image to parse
        print ('Color depth is ' + str(self.depth))
        print ('found ' + str(len(self.colors)) + ' colors')
        for key, value in self.colors:
            color, rgb = self.FindColorDelta(value)
            print('color ' + str(value) + ' matches ' + color + ' ' + str(rgb))


if __name__ == '__main__':
    dmc = Dmc()
    dmc.Initiate()
