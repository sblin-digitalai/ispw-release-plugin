#
# Copyright 2021 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import sys
from array import array
from javax.net.ssl import SSLContext, TrustManager, X509TrustManager

class TrustAllX509TrustManager(X509TrustManager):
    """Define a custom TrustManager which will blindly accept all certificates"""
    def checkClientTrusted(self, chain, auth):
        pass

    def checkServerTrusted(self, chain, auth):
        pass

    def getAcceptedIssuers(self):
        return None

class TrustAllCertificates:

    _blind_trust = False

    def __init__(self):
        pass

    @staticmethod
    def trust_all_certificates():
        """Blindly trusts all certificates; note this is a per-JVM process setting."""
        if not TrustAllCertificates._blind_trust:
            print >> sys.stderr, "Trusting all certificates without verifying them for this process."
            print >> sys.stderr, "It would be best to install certificates in the JVM's trust store."
            print >> sys.stderr, "Currently there is no way to turn this off."
            trust_managers = array(TrustManager, [TrustAllX509TrustManager()])
            trust_all_context = SSLContext.getInstance("SSL")
            trust_all_context.init(None, trust_managers, None)
            SSLContext.setDefault(trust_all_context)
            TrustAllCertificates._blind_trust = True
