#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import json
import requests
from sseclient import SSEClient
import xml.etree.ElementTree as ET
import logging

logger = logging.getLogger(__name__)

class API(object):
    def __init__(self, url=None, format='raw', user=None, key=None):
        self.available_formats = ['json', 'xml', 'raw']
        self._setup_requests(url=url, user=user, key=key)
        self.format = format

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self.lastUpdate = 0
        self._url = value;

    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, value):
        if value not in self.available_formats:
            logger.warning('Unknown API format {}. Using raw instead'.format(value))
            self._format = 'raw'
        else:
            self._format = value


    def _setup_requests(self, url, user=None, key=None, rateLimit=3600, api_suffix=''):
        """
        Setup the request parameters.

        This should be called once within __init__

        Parametes
        ---------
        url: string
            The URL for the requests library.
        user : string, optional
            username for HTTPBasicAuth
        key : string, optional
            key or password for HTTPBasicAuth
        rateLimit : integer, optional
            How many seconds to wait betrween two requests. 3600s default.
        api_suffix : string, optional
            String to append to the URL for the request. Example: '&page=1'

        """
        self.url = url
        self.rateLimit = rateLimit
        self.api_suffix = ''
        self.request_url = ''
        self.status = False
        self._auth = requests.auth.HTTPBasicAuth(user, key) if user and key else None

    def preQuery(self):
        """
        This is called before the requests methods.

        The self.query() will use the self.request_url. It can be modified here.

        """
        self.request_url = self.url
        pass

    def postQuery(self):
        """
        This is called after a successfull reuqest and before the end of the
        query() methodself.

        The data from the requests lies in self.response. This method can be
        used to check the data for validity. self.query() sets self.status to
        True before callig this and returns it after this. If the data check
        fails set self.status to false.

        """
        pass

    def stream(self):
        try:
            response = requests.get(self.request_url, auth=self._auth, stream=True)
        except Excpetion as e:
            logger.warning(e)
            pass
        if response.status_code == 200:
            self.content = None
            self.sseclient = SSEClient(response)

    def query(self, url=False):
        """
        Perfom a GET-Request on the URL in self.request_url.

        Returns
        -------
        bool
            True if successfull, False otherwise.

            True means that new data was fetched from the URL. False means the
            request has failed or it hits the rate limit.

        """
        if time.time() - self.lastUpdate > self.rateLimit or url:
            # Ignore rate limit if manual url
            self.status = False
            self.preQuery()
            try:
                response = requests.get(url or self.request_url, auth=self._auth)
            except Exception as e:
                logger.warning(e)
                return self.status
            self.lastUpdate += 5 if response.status_code == 202 else 0
            if response.status_code == 200:
                self._handle_response(response)
                self.postQuery()
                self.lastUpdate = time.time()
                self.status = True
            else:
                pass
        else:
            self.postQuery()
        return self.status

    def _handle_response(self, response):
        if self.format == 'json':
            self.content = response.json()
        elif self.format == 'xml':
            self.content = ET.fromstring(response.content)
        else:
            self.content = response.content

    def update(self):
        pass

    def check_connection(self, url='https://1.1.1.1', timeout=5):
        logger.info('Performing selftest with {}'.format(url))
        if self.query(url):
            logger.info('Connected to the internet.')
            return True
        else:
            logger.warning('Not connected to the internet.')
            return False

    def speedtest(self, url='http://speedtest.belwue.net/100M'):
        logger.info('Performing speedtest with {}'.format(url))
        now = time.time()
        if self.query(url):
            self.connectionSpeed = int(len(self.content) / (time.time() - now))
            logger.info('Connection speed is {}/s'.format(human_readable(self.connectionSpeed)))
            return self.connectionSpeed
        else:
            return False

# Source https://stackoverflow.com/a/43750422
def human_readable(bytes, units=[' bytes','kB','MB','GB','TB', 'PB', 'EB']):
    """ Returns a human readable string reprentation of bytes"""
    return str(bytes) + units[0] if bytes < 1024 else human_readable(bytes>>10, units[1:])
