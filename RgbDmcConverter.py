#!/usr/bin/env python
import requests
import bs4
from PIL import Image
import os.path
# DEBUG:
import pprint


class Dmc:
    """Class class aimed at converting images (mostly pixel
    art) to DMC colors for cross stitching."""

    def __init__(self):
        # DOC: URL of the site to fetch
        self.table = {}

    def Normalize(self, p):
        """Normalize Unix paths"""
        if str(p[:1]) == '~':
            return os.path.expanduser(p)
        else:
            return os.path.abspath(p)

    def FetchOnline(self):
        """Gets the remote page and load it in BeautifulSoup."""
        res = requests.get()
        res.raise_for_status()
        self.content = bs4.BeautifulSoup(res.text)
        for row in self.content.select('table.tableborder tr'):
            # DEBUG: print (row)
            try:
                cell = row.select('td')
                self.CreateDict(cell)
            except IndexError:
                pass

    def CreateDict(self, cell):
        """Subtask to create the supported colors table."""
        self.table[cell[0].get_text()] = {'name': cell[1].get_text(),
                                          'R': cell[2].get_text(),
                                          'G': cell[2].get_text(),
                                          'B': cell[3].get_text(),
                                          'hex': cell[4].get_text()}

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
            self.colors = img.getcolors(256)
        except OSError as e:
            print ('Error opening the file ', location)
            print (e)

    def Initiate(self):
        """Launches the full script"""
        self.GetImgColors()
        pprint.pprint(self.colors)


if __name__ == '__main__':
    dmc = Dmc()
    dmc.Initiate()
