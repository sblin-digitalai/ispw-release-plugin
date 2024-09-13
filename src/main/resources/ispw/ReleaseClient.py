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
from ispw.HttpClient import HttpClient
from ispw.Util import check_response

logger = logging.getLogger(__name__)

class ReleaseClient(HttpClient):
    def create_release(self, srid, application, stream, description, release_id, release_prefix, owner,
                       reference_number, retryInterval, retryLimit):
        context_root = "/ispw/%s/releases/" % srid
        body = {'application': application, 'stream': stream, 'description': description, 'releaseId': release_id,
                'releasePrefix': release_prefix, 'owner': owner, 'referenceNumber': reference_number}

        if retryLimit == 0: retryLimit = 1
        for x in range(retryLimit):
            response = self._post_request(context_root, json.dumps(body),
                                        {'Accept': 'application/json', 'Content-type': 'application/json'})
            if check_response(response, retryInterval, (x >= retryLimit-1), srid, "create release"):
                break
            else:
                print("Call for 'create release' returned 409(conflict), trying again - %s" % str(x+1))
        return response.getResponse()

    def get_release_information(self, srid, release_id, retryInterval, retryLimit):
        context_root = "/ispw/%s/releases/%s" % (srid, release_id)
        
        if retryLimit == 0: retryLimit = 1
        for x in range(retryLimit):
            response = self._get_request(context_root, {'Accept': 'application/json'})
            logger.debug("isLastCall? - %s, x - %d, retryLimt - %d " % ((x >= retryLimit-1), x, retryLimit))
            logger.debug("response returned - %s, %s, about to run check response" % (str(response.getStatus()), str(response.errorDump())))
            if check_response(response, retryInterval, (x >= retryLimit-1), srid, "get release"):
                logger.debug("About to break, check response was true")
                break
            else:
                logger.debug("in for loop, check reponse returned false, about to try again, range is %s" % str(range(retryLimit)))
                print("Call for 'get release' returned 409(conflict), trying again - %s" % str(x+1))

        return response.getResponse()

    def get_release_task_list(self, srid, release_id, level, retryInterval, retryLimit):
        context_root = "/ispw/%s/releases/%s/tasks" % (srid, release_id)
        if level:
            context_root += "?level=%s" % level

        if retryLimit == 0: retryLimit = 1
        for x in range(retryLimit):
            response = self._get_request(context_root, {'Accept': 'application/json'})
            if check_response(response, retryInterval, (x >= retryLimit-1), srid, "get release task list"):
                break
            else:
                print("Call for 'get release task list' returned 409(conflict), trying again - %s" % str(x+1))

        return response.getResponse()


    def get_release_task_information(self, srid, release_id, task_id, retryInterval, retryLimit):
        context_root = "/ispw/%s/releases/%s/tasks/%s" % (srid, release_id, task_id)
        
        if retryLimit == 0: retryLimit = 1
        for x in range(retryLimit):
            response = self._get_request(context_root, {'Accept': 'application/json'})

            if check_response(response, retryInterval, (x >= retryLimit-1), srid, "get release task information"):
                break
            else:
                print("Call for 'get release task information' returned 409(conflict), trying again - %s" % str(x+1))

        return response.getResponse()
    
    def promotion_analysis(self, srid, release_id, retryInterval, retryLimit):
        context_root = "/ispw/%s/releases/%s/tasks/promotionAnalysis" % (srid, release_id)
        body = {}
        if retryLimit == 0: retryLimit = 1
        for x in range(retryLimit):
            response = self._post_request(context_root, json.dumps(body),
                                        {'Accept': 'application/json', 'Content-type': 'application/json'})
            if check_response(response, retryInterval, (x >= retryLimit-1), srid, "promotion analysis"):
                break
            else:
                print("Call for 'promotion analysis' returned 409(conflict), trying again - %s" % str(x+1))

        return response.getResponse()
    
    def fallback_release(self, srid, relId, retryInterval, retryLimit):
        context_root = "/ispw/%s/releases/%s/tasks/fallback" % (srid, relId)
        body = {}
        if retryLimit == 0: retryLimit = 1
        for x in range(retryLimit):
            response = self._post_request(context_root, json.dumps(body),
                                        {'Accept': 'application/json', 'Content-type': 'application/json'})
            if check_response(response, retryInterval, (x >= retryLimit-1), srid, "fallback release"):
                break
            else:
                print("Call for 'fallback release' returned 409(conflict), trying again - %s" % str(x+1))

        return response.getResponse()


    def generate_tasks_in_release(self, srid, release_id, level, runtime_configuration, auto_deploy, callback_task_id,
                                  callback_url, callback_username, callback_password, retryInterval, retryLimit):
        context_root = "/ispw/%s/releases/%s/tasks/generate" % (srid, release_id)
        if level:
            context_root += "?level=%s" % level
        body = {'runtimeConfiguration': runtime_configuration,
                'autoDeploy': auto_deploy,
                'httpHeaders': [{'name': 'Content-type', 'value': 'application/json'}],
                'credentials': {'username': callback_username, 'password': callback_password}, 'events': [
                {"name": "completed", "url": "%s/api/v1/tasks/%s/complete" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Task generation completed by ISPW\"}"},
                {"name": "failed", "url": "%s/api/v1/tasks/%s/fail" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Task generation failed by ISPW\"}"},
                {"name": "terminated", "url": "%s/api/v1/tasks/%s/fail" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Task generation terminated by ISPW\"}"},
                {"name": "deleted", "url": "%s/api/v1/tasks/%s/fail" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Task generation deleted by ISPW\"}"}]}

        if retryLimit == 0: retryLimit = 1
        for x in range(retryLimit):
            response = self._post_request(context_root, json.dumps(body),
                                        {'Accept': 'application/json', 'Content-type': 'application/json'})

            if check_response(response, retryInterval, (x >= retryLimit-1), srid, "generate tasks for release"):
                break
            else:
                print("Call for 'generate tasks for release' returned 409(conflict), trying again - %s" % str(x+1))
            
        return response.getResponse()


    def get_release_task_generate_listing(self, srid, release_id, task_id, retryInterval, retryLimit):
        context_root = "/ispw/%s/releases/%s/tasks/%s/listing" % (srid, release_id, task_id)
        
        if retryLimit == 0: retryLimit = 1
        for x in range(retryLimit):
            response = self._get_request(context_root, {'Accept': 'application/json'})

            if check_response(response, retryInterval, (x >= retryLimit-1), srid, "get release tasks generate listing"):
                break
            else:
                print("Call for 'get release tasks generate listing' returned 409(conflict), trying again - %s" % str(x+1))

        return response.getResponse()


    def promote(self, srid, release_id, level, change_type, execution_status, runtime_configuration, override, auto_deploy,
                callback_task_id,
                callback_url, callback_username, callback_password, retryInterval, retryLimit):
        context_root = "/ispw/%s/releases/%s/tasks/promote?level=%s" % (srid, release_id, level)
        body = {'changeType': change_type, 'executionStatus': execution_status,
                'runtimeConfiguration': runtime_configuration,
                'override': override,
                'autoDeploy': auto_deploy,
                'httpHeaders': [{'name': 'Content-type', 'value': 'application/json'}],
                'credentials': {'username': callback_username, 'password': callback_password}, 'events': [
                {"name": "completed", "url": "%s/api/v1/tasks/%s/complete" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Promotion completed by ISPW\"}"},
                {"name": "failed", "url": "%s/api/v1/tasks/%s/fail" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Promotion failed by ISPW\"}"},
                {"name": "terminated", "url": "%s/api/v1/tasks/%s/fail" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Promotion terminated by ISPW\"}"},
                {"name": "deleted", "url": "%s/api/v1/tasks/%s/fail" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Promotion deleted by ISPW\"}"}]}

        if retryLimit == 0: retryLimit = 1
        for x in range(retryLimit):
            response = self._post_request(context_root, json.dumps(body),
                                        {'Accept': 'application/json', 'Content-type': 'application/json'})

            if check_response(response, retryInterval, (x >= retryLimit-1), srid, "promote release"):
                break
            else:
                print("Call for 'promote release' returned 409(conflict), trying again - %s" % str(x+1))

        return response.getResponse()

    def deploy(self, srid, release_id, level, change_type, execution_status, runtime_configuration, dpenvlst, system,
               callback_task_id, callback_url, callback_username, callback_password, retryInterval, retryLimit):
        context_root = "/ispw/%s/releases/%s/tasks/deploy?level=%s" % (srid, release_id, level)
        body = {'changeType': change_type, 'executionStatus': execution_status,
                'runtimeConfiguration': runtime_configuration,
                'dpenvlst': dpenvlst, 'system': system,
                'httpHeaders': [{'name': 'Content-type', 'value': 'application/json'}],
                'credentials': {'username': callback_username, 'password': callback_password}, 'events': [
                {"name": "completed", "url": "%s/api/v1/tasks/%s/complete" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Deploy completed by ISPW\"}"},
                {"name": "failed", "url": "%s/api/v1/tasks/%s/fail" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Deploy failed by ISPW\"}"},
                {"name": "terminated", "url": "%s/api/v1/tasks/%s/fail" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Deploy terminated by ISPW\"}"},
                {"name": "deleted", "url": "%s/api/v1/tasks/%s/fail" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Deploy deleted by ISPW\"}"}]}

        if retryLimit == 0: retryLimit = 1
        for x in range(retryLimit):
            response = self._post_request(context_root, json.dumps(body),
                                        {'Accept': 'application/json', 'Content-type': 'application/json'})

            if check_response(response, retryInterval, (x >= retryLimit-1), srid, "deploy release"):
                break
            else:
                print("Call for 'deploy release' returned 409(conflict), trying again - %s" % str(x+1))

        return response.getResponse()


    def regress(self, srid, release_id, level, change_type, execution_status, runtime_configuration, callback_task_id,
                callback_url, callback_username, callback_password, retryInterval, retryLimit):
        context_root = "/ispw/%s/releases/%s/tasks/regress?level=%s" % (srid, release_id, level)
        body = {'changeType': change_type, 'executionStatus': execution_status,
                'runtimeConfiguration': runtime_configuration,
                'httpHeaders': [{'name': 'Content-type', 'value': 'application/json'}],
                'credentials': {'username': callback_username, 'password': callback_password}, 'events': [
                {"name": "completed", "url": "%s/api/v1/tasks/%s/complete" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Regression completed by ISPW\"}"},
                {"name": "failed", "url": "%s/api/v1/tasks/%s/fail" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Regression failed by ISPW\"}"},
                {"name": "terminated", "url": "%s/api/v1/tasks/%s/fail" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Regression terminated by ISPW\"}"},
                {"name": "deleted", "url": "%s/api/v1/tasks/%s/fail" % (callback_url, callback_task_id),
                 "body": "{\"comment\":\"Regression deleted by ISPW\"}"}]}

        if retryLimit == 0: retryLimit = 1
        for x in range(retryLimit):
            response = self._post_request(context_root, json.dumps(body),
                                        {'Accept': 'application/json', 'Content-type': 'application/json'})

            if check_response(response, retryInterval, (x >= retryLimit-1), srid, "regress release"):
                break
            else:
                print("Call for 'regress release' returned 409(conflict), trying again - %s" % str(x+1))

        return response.getResponse()
