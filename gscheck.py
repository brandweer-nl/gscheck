#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tools for GeoServer

This class uses the GeoServer API to implement a number of methods.
"""

import configparser
import urllib.parse
import requests

__author__ = "Guido Legemaate"
__copyright__ = "Copyright 2020, brandweer Amsterdam-Amstelland"
__credits__ = ["Gert-Jan van der Weijden"]
__license__ = "MIT"
__version__ = "0.0.5"
__maintainer__ = "Guido Legemaate"
__email__ = "g.legemaate@brandweeraa.nl"
__status__ = "Development"

class GSCheck():
    """
    Class with tools for GeoServer
    """

    def __init__(self, profile):
        self._config = configparser.ConfigParser()
        self._config.read("config.ini")
        self._headers = {"Content-Type": "application/json",
                         "Accept": "application/json"}
        self._baseurl = self._config[profile]["url"].rstrip("/")
        self._user = self._config[profile]["user"]
        self.__pswd = self._config[profile]["password"]
        self.__auth = (self._user, self.__pswd)

    def retrieve(self, *args):
        """
        Return data (as json/dict) from a geoserver instance using a REST API

        Keyword arguments:
        *args -- a dynamic amount of arguments
        """  
        url = "{}".format(self._baseurl)
        for arg in args:
            url+="/{}".format(urllib.parse.quote(arg))
        try:
            res = requests.get(url, headers=self._headers, auth=self.__auth)
            res.raise_for_status()
        except requests.exceptions.HTTPError as msg:
            print("Er is een probleem met de server gedetecteerd: {}.".format(msg))
            result = {"error": "{}".format(msg)}
        else:
            result = res.json()
        return args, result