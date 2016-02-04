#!/usr/bin/env python
import requests
import bs4
import os.path
import re


class MSParser:
    """Class class aimed at converting images (mostly pixel
    art) to DMC colors for cross stitching."""

    def __init__(self):
        # DOC: URL of the site to fetch
        self.url = ""
