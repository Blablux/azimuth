#!/usr/bin/env python
import requests
import bs4
import os.path
import errno
import zipfile
import shutil


class MSParser:
    """Class used to parse specific website for comic book auto-download"""

    def __init__(self):
        # DOC: URL of the site to fetch
        self.url = ""
        # DOC: List of the comic books to search.
        self.serials = [""]
        # DOC: Where to store the books
        self.baseLocation = os.path.expanduser('~/books')
        # DOC: Working directory
        self.tmpLocation = '/var/tmp'
        # These variables will be used later
        self.serial = []
        self.serialUrl = []
        self.nextPage = ''
        self.location = ''

    def OpenLocal(self, resource):
        """Used for debugging purpose, when you don't want to hammer the
        remote site"""
        res = open(resource)
        self.content = bs4.BeautifulSoup(res)

    def OpenResource(self, resource):
        """Gets the remote page and load it in BeautifulSoup"""
        res = requests.get(resource)
        res.raise_for_status()
        self.content = bs4.BeautifulSoup(res.text)

    def GetSerials(self):
        """Checks in the front page if there is any comic book
        that we're looking for, and stores their name and URL"""
        for a in self.content.find_all('a', href=True):
            for serial in self.serials:
                if serial in a.get_text() and 'read' in a['href']:
                    self.serialUrl.append(a['href'])
                    self.serial.append(a.strong.previous_element.string
                                       .strip() + ' ' + a.strong.string.strip()
                                       )

    def SetEnv(self):
        """Checks for existing books and creates the directories to store the
        images if the book does not yet exist"""
        for name in self.serial:
            if not os.path.exists(os.path.join(self.baseLocation, name) +
                                  '.cbz'):
                try:
                    os.makedirs(os.path.join(self.tmpLocation, name))
                except OSError as exception:
                    if exception.errno != errno.EEXIST:
                        raise
            else:
                del self.serialUrl[self.serial.index(name)]
                del self.serial[self.serial.index(name)]

    def GetNextPage(self):
        """Parse for the next page or returns nothing"""
        try:
            self.nextPage = self.content.select('.next a')[0]['href']
        except:
            self.nextPage = None

    def GetPage(self):
        """Downloads the image and save it to the temporary folder, then calls
        the next page"""
        self.OpenResource(self.nextPage)
        img = self.content.select('img#manga-page')
        if img == []:
            print('Could not find image.')
        else:
            try:
                imgUri = img[0].get('src')
                # Download the image.
                print('Downloading image %s...' % (imgUri))
                res = requests.get(imgUri)
                res.raise_for_status()
            except requests.exceptions.MissingSchema:
                # skip this page
                print('Image not found here')
                self.GetNextPage()
            # TODO: Do not download uneeded pages
            imageFile = open(os.path.join(self.location,
                             os.path.basename(imgUri)),
                             'wb')
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()
        self.GetNextPage()

    def Initiate(self):
        """Launches the full script"""
        self.OpenResource(self.url)
        self.GetSerials()
        self.SetEnv()
        for name in self.serial:
            self.location = os.path.join(self.tmpLocation, name)
            self.nextPage = self.serialUrl[self.serial.index(name)]
            while self.nextPage:
                self.GetPage()
            self.Compress(name)

    def Compress(self, name):
        """Compress the temporary folder in the base forlder"""
        cbz = zipfile.ZipFile(os.path.join(self.baseLocation, name + '.cbz'),
                              'w')
        for r, d, f in os.walk(self.location):
            for fn in f:
                cbz.write(os.path.join(r, fn), arcname=fn,
                          compress_type=zipfile.ZIP_DEFLATED)
        cbz.close()
        shutil.move(os.path.join(self.tmpLocation, name),
                    os.path.expanduser('~/.local/share/Trash/files'))
