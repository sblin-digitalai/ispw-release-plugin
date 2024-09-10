#
# Copyright 2021 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


import os
import json


class ItestConf(object):
    def __init__(self):
        file_location = os.getenv('itest_conf_file')
        if not file_location:
            raise Exception("No environment variable named 'itest_conf_file' set." +
                            " This variable should point to the file containing connection info.")

        with open(file_location) as data_file:
            data = json.load(data_file)
        self.settings = {o['name']: o for o in data}

    def apply_settings(self, name, target, expects_params):
        if name not in self.settings:
            raise Exception("'%s' is not found in the itest_conf_file" % name)
        settings = self.settings[name]
        for k, v in settings.items():
            target.__dict__[k] = v
        for p in expects_params:
            if target.__dict__[p] is None:
                raise Exception("%s is a required property missing from '%s' in the itest_conf_file" % (p, name))


itest_conf = ItestConf()


class CiStub(object):
    def getProperty(self, name):
        return self.__dict__[name]

    def setProperty(self, name, value):
        self.__dict__[name] = value

    def __getitem__(self, key):
        return self.__dict__[key]


class ISPWServerCi(CiStub):
    def __init__(self):
        itest_conf.apply_settings("ispw_server", self, ["url", "cesToken", "proxyHost", "enableSslVerification"])
        self.name = "ispw"
        self.id = "Configuration/Custom/%s" % self.name
        self.type = "ispwServices.Server"
        self.title = self.name
