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
import time
import logging

from ispw.HttpClient import HttpClient
from ispw.Util import check_response

logger = logging.getLogger(__name__)

class AssignmentClient(HttpClient):
    def create_assignment(self, srid, stream, application, default_path, description, owner, assignment_prefix,
                          reference_number, release_id, user_tag, retryInterval, retryLimit):
        context_root = "/ispw/%s/assignments/" % srid
        body = {'stream': stream, 'application': application,
                'defaultPath': default_path,
                'description': description,
                'owner': owner,
                'assignmentPrefix': assignment_prefix,
                'referenceNumber': reference_number,
                'releaseId': release_id,
                'userTag': user_tag}
        if retryLimit == 0: retryLimit = 1
        for x in range(retryLimit):
            response = self._post_request(context_root, json.dumps(body), {'Accept': 'application/json', 'Content-type': 'application/json'})

            if check_response(response, retryInterval, (x >= retryLimit-1), srid, "create assigment"):
                break
            else:
                print("Call for 'create assignment' returned 409(conflict), trying again - %s" % str(x+1))

        return response.json()


    def load_task(self, srid, assignment_id, stream, application, module_name, module_type, current_level, starting_level,
                  generate_sequence, sql, ims, cics, program, retryInterval, retryLimit):
        context_root = "/ispw/%s/assignments/%s/tasks" % (srid, assignment_id)
        body = {'application': application, 'stream': stream,
                'moduleName': module_name,
                'moduleType': module_type,
                'currentLevel': current_level,
                'startingLevel': starting_level,
                'generateSequence': generate_sequence,
                'sql': sql,
                'ims': ims,
                'cics': cics,
                'program': program}
        if retryLimit == 0: retryLimit = 1
        for x in range(retryLimit):
            response = self._post_request(context_root, json.dumps(body), {'Accept': 'application/json', 'Content-type': 'application/json'})

            if check_response(response, retryInterval, (x >= retryLimit-1), srid, "load task"):
                break
            else:
                print("Call for 'load task' returned 409(conflict), trying again - %s" % str(x+1))

        return response.json()


    def get_assignment_information(self, srid, assignment_id, retryInterval, retryLimit):
        context_root = "/ispw/%s/assignments/%s" % (srid, assignment_id)

        if retryLimit == 0: retryLimit = 1
        for x in range(retryLimit):
            response = self._get_request(context_root, {'Accept': 'application/json', 'Content-type': 'application/json'})

            if check_response(response, retryInterval, (x >= retryLimit-1), srid, "get assignment information"):
                break
            else:
                print("Call for 'get assignment information' returned 409(conflict), trying again - %s" % str(x+1))

        return response.json()


    def get_assignment_task_list(self, srid, assignment_id, level, retryInterval, retryLimit):
        context_root = "/ispw/%s/assignments/%s/tasks" % (srid, assignment_id)
        if level:
            context_root += "?level=%s" % level

        if retryLimit == 0: retryLimit = 1
        for x in range(retryLimit):
            response = self._get_request(context_root, {'Accept': 'application/json'})

            if check_response(response, retryInterval, (x >= retryLimit-1), srid, "get assignment task list"):
                break
            else:
                print("Call for 'get assignment task list' returned 409(conflict), trying again - %s" % str(x+1))

        return response.json()


    def get_assignment_task_information(self, srid, assignment_id, task_id, retryInterval, retryLimit):
        context_root = "/ispw/%s/assignments/%s/tasks/%s" % (srid, assignment_id, task_id)

        if retryLimit == 0: retryLimit = 1
        for x in range(retryLimit):
            response = self._get_request(context_root, {'Accept': 'application/json'})

            if check_response(response, retryInterval, (x >= retryLimit-1), srid, "get assignment task information"):
                break
            else:
                print("Call for 'get release task information' returned 409(conflict), trying again - %s" % str(x+1))

        return response.json()


    def generate_tasks_in_assignment(self, srid, assignment_id, level, runtime_configuration, auto_deploy, callback_task_id,
                                  callback_url, callback_username, callback_password, retryInterval, retryLimit):
        context_root = "/ispw/%s/assignments/%s/tasks/generate" % (srid, assignment_id)
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
            response = self._post_request(context_root, json.dumps(body), {'Accept': 'application/json', 'Content-type': 'application/json'})

            if check_response(response, retryInterval, (x >= retryLimit-1), srid, "generate tasks"):
                break
            else:
                print("Call for 'generate tasks' returned 409(conflict), trying again - %s" % str(x+1))

        return response.json()


    def promote_assignment(self, srid, assignment_id, level, change_type, execution_status, runtime_configuration, override, auto_deploy,
                callback_task_id, callback_url, callback_username, callback_password, retryInterval, retryLimit):
        context_root = "/ispw/%s/assignments/%s/tasks/promote?level=%s" % (srid, assignment_id, level)
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
            response = self._post_request(context_root, json.dumps(body), {'Accept': 'application/json', 'Content-type': 'application/json'})

            if check_response(response, retryInterval, (x >= retryLimit-1), srid, "promote assignment"):
                break
            else:
                print("Call for 'promote assignment' returned 409(conflict), trying again - %s" % str(x+1))

        return response.json()


    def deploy_assignment(self, srid, assignment_id, level, change_type, execution_status, runtime_configuration, dpenvlst, system,
               callback_task_id, callback_url, callback_username, callback_password, retryInterval, retryLimit):
        context_root = "/ispw/%s/assignments/%s/tasks/deploy?level=%s" % (srid, assignment_id, level)
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
            response = self._post_request(context_root, json.dumps(body), {'Accept': 'application/json', 'Content-type': 'application/json'})

            if check_response(response, retryInterval, (x >= retryLimit-1), srid, "deploy assignment"):
                break
            else:
                print("Call for 'deploy assignment' returned 409(conflict), trying again - %s" % str(x+1))

        return response.json()


    def regress_assignment(self, srid, assignment_id, level, change_type, execution_status, runtime_configuration, callback_task_id,
                callback_url, callback_username, callback_password, retryInterval, retryLimit):
        context_root = "/ispw/%s/assignments/%s/tasks/regress?level=%s" % (srid, assignment_id, level)
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
            response = self._post_request(context_root, json.dumps(body), {'Accept': 'application/json', 'Content-type': 'application/json'})

            if check_response(response, retryInterval, (x >= retryLimit-1), srid, "regress assignment"):
                break
            else:
                print("Call for 'regress assignment' returned 409(conflict), trying again - %s" % str(x+1))

        return response.json()
