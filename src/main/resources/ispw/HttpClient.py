#
# Copyright 2021 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from xlrelease.HttpRequest import HttpRequest

class HttpClient(object):
    def __init__(self, http_connection, ces_token=None):
        self.http_connection = http_connection
        self.url = http_connection['url']
        self.ces_token = None
        if ces_token:
            self.token = ces_token
        else:
            self.token = http_connection['cesToken']
        self.proxy = None
        if http_connection['proxyHost']:
            self.proxy = {'http': '%s:%s' % (http_connection['proxyHost'], http_connection['proxyPort'])}
        self.verify_ssl = http_connection['enableSslVerification']
        if not self.verify_ssl:
            from trustmanager.all_truster import TrustAllCertificates
            TrustAllCertificates.trust_all_certificates()

    def _get_request(self, context_root, additional_headers=None):
        headers = {'Authorization': '%s' % self.token}
        headers.update(additional_headers)
        params = {'url':self.url, 'type': 'application/json'}
        return HttpRequest(params).get(context_root, contentType='application/json', headers=headers)

    def _post_request(self, context_root, content, additional_headers=None):
        params = {'url':self.url, 'type': 'application/json'}
        headers = {'Authorization': '%s' % self.token}
        headers.update(additional_headers)
        return HttpRequest(params).post(context_root,content=content, contentType='application/json', headers=headers)
