#!/usr/bin/env python
import requests
import bs4
# import os.path
# import re
# import pprint


class Dmc:
    """Class class aimed at converting images (mostly pixel
    art) to DMC colors for cross stitching."""

    def __init__(self):
        # DOC: URL of the site to fetch
        self.table = {}

    def FetchOnline(self):
        """Gets the remote page and load it in BeautifulSoup"""
        res = requests.get('')
        res.raise_for_status()
        self.content = bs4.BeautifulSoup(res.text)
        for row in self.content.select('table.tableborder tr'):
            print (row)
            try:
                cell = row.select('td')
                self.CreateDict(cell)
            except IndexError:
                pass

    def CreateDict(self, cell):
        self.table[cell[0].get_text()] = {'name': cell[1].get_text(),
                                          'R': cell[2].get_text(),
                                          'G': cell[2].get_text(),
                                          'B': cell[3].get_text(),
                                          'hex': cell[4].get_text()}

    def SaveLocal(self, location):
        self.FetchOnline()
        try:
            save = open(location, 'rw')
            save.write(self.table)
            save.close()
        except OSError as e:
            if isinstance(e, FileNotFoundError):
                pass
            else:
                return False

    def Initiate(self):
        """Launches the full script"""
        self.FetchOnline()


if __name__ == '__main__':
    dmc = Dmc()
    dmc.Initiate()
    # print dmc.content
    # pprint.pprint(dmc.table)
