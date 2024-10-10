#
# Copyright 2021 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import json
import logging
import time
import sys

from ispw.HttpClient import HttpClient
from ispw.Util import check_response

logger = logging.getLogger(__name__)

class ContainerClient(HttpClient):

    def get_container_list(self, srid, userId, containerId, containerType, application, owner, description,
                           refNumber, releaseId, stream, defaultPath, tag, includeClosedContainers, retryInterval, retryLimit):
        context_root = "/ispw/%s/containers/list?" % srid

        if userId: context_root += "userId=%s&" % userId
        if containerId: context_root += "containerId=%s&" % containerId
        if containerType: context_root += "containerType=%s&" % containerType
        if stream: context_root += "stream=%s&" % stream
        if application: context_root += "application=%s&" % application
        if defaultPath: context_root += "path=%s&" % defaultPath
        if owner: context_root += "owner=%s&" % owner
        if description: context_root += "description=%s&" % description
        if refNumber: context_root += "refNumber=%s&" % refNumber
        if releaseId: context_root += "releaseId=%s&" % releaseId
        if tag: context_root += "tag=%s&" % tag
        if includeClosedContainers: context_root += "includeClosedContainers=%s&" % includeClosedContainers

        if retryLimit == 0: retryLimit = 1
        for x in range(retryLimit):
            response = self._get_request(context_root, {'Accept': 'application/json'})

            if check_response(response, retryInterval, (x >= retryLimit-1), srid, "get containers list"):
                break
            else:
                print("Call for 'get containers list' returned 409(conflict), trying again - %s" % str(x+1))
        return response.getResponse()