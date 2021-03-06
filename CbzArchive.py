#!/usr/bin/env python
import requests
import bs4
import os
import zipfile
import re


class MSParser:
    """Class used to parse specific website for comic book auto-download"""

    def __init__(self):
        # DOC: URL of the site to fetch
        self.url = ""
        # DOC: List of the comic books to search.
        self.serials = []
        # DOC: Where to store the books
        self.baseLocation = os.path.expanduser('~/books')
        # DOC: Working directory
        self.tmpLocation = '/var/tmp'
        # DOC: These variables will be used later
        self.serialUrl = []
        self.serialNm = []
        self.nextPage = ''
        self.location = ''
        # DOC: some regex to filter pages
        self.credit = re.compile('\d{2,}[a-z]\.(jpg|png)')
        self.end = re.compile('\d{2,}\.jpg')

    def OpenLocal(self, resource):
        """Used for debugging purpose, when you don't want to hammer the
        remote site"""
        res = open(resource)
        self.content = bs4.BeautifulSoup(res, "lxml")

    def OpenResource(self, resource):
        """Gets the remote page and load it in BeautifulSoup"""
        res = requests.get(resource)
        res.raise_for_status()
        self.content = bs4.BeautifulSoup(res.text, "lxml")

    def GetSerials(self):
        """Checks in the front page if there is any comic book
        that we're looking for, and stores their name and URL"""
        for a in self.content.find_all('a', href=True):
            for serial in self.serials:
                if serial in a.get_text() and '/r/' in a['href']:
                    self.serialUrl.append(a['href'])
                    self.serialNm.append(a.strong.previous_element.string
                                         .strip() + ' ' +
                                         a.strong.string.strip()
                                         )
                    # LOG:
                    print('Found ' + a.strong.previous_element.string
                          .strip() + ' ' +
                          a.strong.string.strip())
        self.serial = list(self.serialNm)

    def SetEnv(self):
        """Checks for existing books and creates the directories to store the
        images if the book does not yet exist"""
        for index, name in reversed(list(enumerate(self.serialNm))):
            if not os.path.exists(os.path.join(self.baseLocation, name) +
                                  '.cbz'):
                if not os.path.exists(os.path.join(self.tmpLocation, name)):
                    try:
                        os.makedirs(os.path.join(self.tmpLocation, name))
                    except:
                        raise
            else:
                # LOG:
                print('The file ' + self.serial[index] + ' already exists,'
                      + ' skipping')
                del self.serialUrl[index]
                del self.serial[index]

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
            # DOC: if finished DL, remove last image when it matches 'end'
            if self.end.match(os.path.basename(self.lastimage)):
                os.remove(self.lastimage)
        # DOC: image matching 'credit' are ignored
        elif not self.credit.match(os.path.basename(img[0].get('src'))):
            imgUri = img[0].get('src')
            if not imgUri[:4] == "http":
                if imgUri[:2] == "//":
                    imgUri = "http:" + imgUri
                    # DEBUG:print("imgUri changed to " + imgUri)
                # TODO: Add new cases as they show up
            imgRoot, imgExt = os.path.splitext(imgUri)
            print("imgRoot = " + imgRoot)
            if self.counter < 10:
                filename = '0' + str(self.counter) + imgExt
            else:
                filename = str(self.counter) + imgExt
            try:
                res = requests.get(imgUri)
                res.raise_for_status()
            except requests.exceptions.MissingSchema:
                self.GetNextPage()
            # TODO: Do not download uneeded pages
            imageFile = open(os.path.join(self.location, filename), 'wb')
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()
            self.lastimage = os.path.join(self.location, filename)
            self.counter += 1
        self.GetNextPage()

    def Initiate(self):
        """Launches the full script"""
        self.OpenResource(self.url)
        self.GetSerials()
        self.SetEnv()
        # DEBUG: print '[%s]' % ', '.join(map(str, self.serial))
        for name in self.serial:
            self.counter = 1
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
        # LOG:
        print('The file ' + os.path.join(r, fn) + ' has been created!')

    def __del__(self):
        for name in self.serial:
            if os.path.exists(os.path.join(self.tmpLocation, name)):
                for r, d, f in os.path.join(self.tmpLocation, name):
                    os.remove(os.path.join(r, f))
                    os.rmdir(r)


if __name__ == '__main__':
    cbz = MSParser()
    cbz.Initiate()
