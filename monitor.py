#!/usr/bin/env python
"""
A simple app to monitor Jenkins builds.

Usage:
    ./monitor.py url [port]

    url - the URL to the Jenkins job.
    port - the port to run the webserver on. Defaults to 8080

"""

import sys
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

import requests
from django.template import Template, Context
from django.conf import settings

settings.configure(TEMPLATE_DEBUG=True, TEMPLATE_DIRS=())

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        content = display(report(base_url))
        self.wfile.write(content)
        self.wfile.close()

def get(url):
    r = requests.get(url + '/api/json')
    if r.ok:
        return r.json
    else:
        raise IOError("HTTP Error {0}: {1} ({2})".format(r.status_code,
                r.reason, r.url))

def report(base_url):
    """ Get the info about the most recent build.
    """
    info = get(base_url)
    last_url = "{0}/{1}".format(base_url, info['lastCompletedBuild']['number'])
    last = get(last_url)
    return last

def display(reports, template="display.html"):
    """ Render the report from the given template file. """
    with open(template, 'rU') as f:
        t = Template(f.read())
        c = Context(reports)
        return t.render(c)

if __name__ == '__main__':
    base_url = sys.argv[1]
    port = int(sys.argv[2]) if sys.argv[2:] else 8080
    HTTPServer(('', port), Handler).serve_forever()
