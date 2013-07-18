"""
 pocketlib.py -- simple library to add items to Pocket
"""

import ConfigParser
import httplib2
import json
import webbrowser
import os


class Pocket:
    """ Structure for connection object. """
    def __init__(self):
        # Load config items
        config = ConfigParser.ConfigParser()
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        config.read(os.path.join(__location__, 'config.ini'))

        if config.has_option('POCKET_API', 'username') is False:
            self.access_token = None
            self.username = None
        else:
            self.access_token = config.get('POCKET_API', 'access_token')
            self.username = config.get('POCKET_API', 'username')
        self.consumer_key = config.get('POCKET_API', 'consumer_key')
        self.request_token_url = config.get('POCKET_API', 'request_token_url')
        self.authorize_url = config.get('POCKET_API', 'authorize_url')
        self.redirect_url = config.get('POCKET_API', 'redirect_url')
        self.access_token_url = config.get('POCKET_API', 'access_token_url')
        self.add_item_url = config.get('POCKET_API', 'add_item_url')

    def is_authed(self):
        return (self.access_token is not None)

    def add_item(self, url, title=None, tags=None):
        """
        Method to add new item to Pocket account

        Parameters: url -> URL to add
                    title -> optional title for URL (will be ignored if page has one)
        Returns: (status as int, status error message)
        """
        parameters = {
            'url': url
        }
        if title is not None:
            parameters['title'] = title
        if tags is not None:
            parameters['tags'] = tags

        status, statustxt = self._query(self.add_item_url, parameters)
        return (int(status), statustxt)

    def auth(self):
        """ Authenticates with Pocket services
            Stores the access_token and username in the config.ini file

            Returns: (status as int, status error message)
        """
        # Obtain request token
        body = "consumer_key=%s&redirect_uri=%s" % (self.consumer_key, self.redirect_url)
        h = httplib2.Http()
        headers = {}
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        resp, content = h.request(self.request_token_url, method="POST", body=body, headers=headers)
        if resp['status'] != '200':
            print resp['x-error']
            exit()
        request_token = content.split("=")

        # Redirect to provider
        print "Go to the following link in your browser and then come back here."
        print "%s?request_token=%s&redirect_uri=%s" % (self.authorize_url, request_token[1], self.redirect_url)
        print
        webbrowser.open("%s?request_token=%s&redirect_uri=%s" % (self.authorize_url, request_token[1], self.redirect_url))
        accepted = 'n'
        while accepted.lower() == 'n':
            accepted = raw_input('Have you authorized me? (y/n) ')
        # Obtain access token
        body = "consumer_key=%s&code=%s" % (self.consumer_key, request_token[1])
        h = httplib2.Http()
        headers = {}
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        resp, content = h.request(self.access_token_url, method="POST", body=body, headers=headers)
        if resp['status'] != '200':
            print resp['x-error']
            exit()
        content_final = content.split("&")
        access_token = content_final[0].split("=")
        username = content_final[1].split("=")
        print "You've been authorized successfully."
        print "Username: %s" % username[1]

        config = ConfigParser.ConfigParser()
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        config.read(os.path.join(__location__, 'config.ini'))
        config.set('POCKET_API', 'username', username[1])
        config.set('POCKET_API', 'access_token', access_token[1])
        with open(os.path.join(__location__, 'config.ini'), 'w') as configfile:
            config.write(configfile)

    def _query(self, url=None, params=""):
        """ method to query a URL with the given parameters

            Parameters:
                url -> URL to query
                params -> dictionary with parameter values

            Returns: HTTP response code, headers
                     If an exception occurred, headers fields are None
        """
        if url is None:
            raise Exception("No URL was provided.")
        headers = {}
        headers['Content-Type'] = 'application/json'

        if not isinstance(params, dict):
            params = {}
        params['consumer_key'] = self.consumer_key
        params['access_token'] = self.access_token

        h = httplib2.Http()
        resp, content = h.request(self.add_item_url, method="POST", body=json.dumps(params), headers=headers)
        status = resp['status']
        if resp['status'] != '200':
            statustxt = resp['x-error']
        else:
            statustxt = 'All good.'

        return (status, statustxt)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
