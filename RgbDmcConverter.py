#!/usr/bin/env python
import requests
import bs4
# import os.path
# import re
# import pprint


class DMCConverter:
    """Class class aimed at converting images (mostly pixel
    art) to DMC colors for cross stitching."""

    def __init__(self):
        # DOC: URL of the site to fetch
        self.url = ""
        self.table = {}

    def OpenResource(self, resource):
        """Gets the remote page and load it in BeautifulSoup"""
        res = requests.get(resource)
        res.raise_for_status()
        self.content = bs4.BeautifulSoup(res.text)

    def FetchColors(self):
        """Extracts the colors from the content and saves them in an
        attribute"""
        for row in self.content.select('table.tableborder tr'):
            print (row)
            cell = row.select('td')
            self.table[cell[0].get_text()] = {'name': cell[1].get_text(),
                                              'R': cell[2].get_text(),
                                              'G': cell[2].get_text(),
                                              'B': cell[3].get_text(),
                                              'hex': cell[4].get_text()}

    def Initiate(self):
        """Launches the full script"""
        self.OpenResource(self.url)


if __name__ == '__main__':
    dmc = DMCConverter()
    dmc.Initiate()
    # print dmc.content
    # pprint.pprint(dmc.table)
