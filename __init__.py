"""
This is more or less copied directly from Daniel Schauenberg's InstapaperLib to use the same concepts with Pocket.
"""

from pocketlib import Pocket

__author__ = "Samuel Kordik"
__version__ = "0.1.0"
__license__ = "MIT"


def auth():
    return Pocket.auth()


def add_item(url=None, title=None, selection=None, jsonp=None, redirect=None, response_info=False):
        return Pocket.add_item(url, title=title, selection=selection, jsonp=jsonp, redirect=redirect, response_info=response_info)
