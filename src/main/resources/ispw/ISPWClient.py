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
from ispw.AssignmentClient import AssignmentClient
from ispw.ReleaseClient import ReleaseClient
from ispw.SetClient import SetClient
from ispw.TestConnectionClient import TestConnectionClient


class ISPWClient(object):
    def __init__(self, http_connection, ces_token=None):
        self.set_client = SetClient(http_connection, ces_token)
        self.release_client = ReleaseClient(http_connection, ces_token)
        self.assignment_client = AssignmentClient(http_connection, ces_token)
        self.test_connection_client = TestConnectionClient(http_connection)

    @staticmethod
    def create_client(http_connection, ces_token=None):
        return ISPWClient(http_connection, ces_token)

    def ispwservices_createassignment(self, variables):
        result = self.assignment_client.create_assignment(srid=variables['srid'], stream=variables['stream'],
                                                          application=variables['application'],
                                                          default_path=variables['defaultPath'],
                                                          description=variables['description'],
                                                          owner=variables['owner'],
                                                          assignment_prefix=variables['assignmentPrefix'],
                                                          reference_number=variables['referenceNumber'],
                                                          release_id=variables['relId'], user_tag=variables['userTag'],
                                                          retryInterval=variables['retryInterval'],
                                                          retryLimit=variables['retryLimit'])
        variables['assignmentId'] = result["assignmentId"]
        variables['url'] = result["url"]

    def ispwservices_loadtask(self, variables):
        result = self.assignment_client.load_task(srid=variables['srid'], assignment_id=variables['assignmentId'],
                                                  stream=variables['stream'],
                                                  application=variables['application'],
                                                  module_name=variables['moduleName'],
                                                  module_type=variables['moduleType'],
                                                  current_level=variables['currentLevel'],
                                                  starting_level=variables['startingLevel'],
                                                  generate_sequence=variables['generateSequence'],
                                                  sql=variables['sql'], ims=variables['ims'],
                                                  cics=variables['cics'], program=variables['program'],
                                                  retryInterval=variables['retryInterval'],
                                                  retryLimit=variables['retryLimit'])
        for key, value in result.iteritems():
            variables[key] = value

    def ispwservices_getassignmentinformation(self, variables):
        result = self.assignment_client.get_assignment_information(srid=variables['srid'], assignment_id=variables['assignmentId'],
                                             retryInterval=variables['retryInterval'],
                                             retryLimit=variables['retryLimit'])
        for key, value in result.iteritems():
            variables[key] = value

    def ispwservices_getassignmenttasklist(self, variables):
        result = self.assignment_client.get_assignment_task_list(srid=variables['srid'], assignment_id=variables['assignmentId'],
                                                               level=variables['level'],
                                                               retryInterval=variables['retryInterval'],
                                                               retryLimit=variables['retryLimit'])
        processed_result = {}
        for item in result["tasks"]:
            task_id = item['taskId']
            processed_result[task_id] = json.dumps(item)
        variables['tasks'] = processed_result

    def ispwservices_getassignmenttaskinformation(self, variables):
        result = self.assignment_client.get_assignment_task_information(srid=variables['srid'], assignment_id=variables['assignmentId'],
                                                                  task_id=variables['taskId'],
                                                                  retryInterval=variables['retryInterval'],
                                                                  retryLimit=variables['retryLimit'])
        for key, value in result.iteritems():
            if key == "taskId":
                variables["taskOutputId"] = value
            elif key == "type":
                variables["taskType"] = value
            else:
                variables[key] = value

    def ispwservices_generatetasksinassignment(self, variables):
        result = self.assignment_client.generate_tasks_in_assignment(srid=variables['srid'], assignment_id=variables['assignmentId'],
                                                               level=variables['level'],
                                                               runtime_configuration=variables['runtimeConfiguration'],
                                                               auto_deploy=variables['autoDeploy'],
                                                               callback_task_id=variables['callbackTaskId'],
                                                               callback_url=variables['callbackUrl'],
                                                               callback_username=variables['callbackUsername'],
                                                               callback_password=variables['callbackPassword'],
                                                               retryInterval=variables['retryInterval'],
                                                               retryLimit=variables['retryLimit'])
        variables['setId'] = result["setId"]
        variables['url'] = result["url"]

    def ispwservices_promoteassignment(self, variables):
        result = self.assignment_client.promote_assignment(srid=variables['srid'], assignment_id=variables['assignmentId'],
                                             level=variables['level'],
                                             change_type=variables['changeType'],
                                             execution_status=variables['executionStatus'],
                                             runtime_configuration=variables['runtimeConfiguration'],
                                             override=variables['override'],
                                             auto_deploy=variables['autoDeploy'],
                                             callback_task_id=variables['callbackTaskId'],
                                             callback_url=variables['callbackUrl'],
                                             callback_username=variables['callbackUsername'],
                                             callback_password=variables['callbackPassword'],
                                             retryInterval=variables['retryInterval'],
                                             retryLimit=variables['retryLimit'])
        variables['setId'] = result["setId"]
        variables['url'] = result["url"]

    def ispwservices_deployassignment(self, variables):
        result = self.assignment_client.deploy_assignment(srid=variables['srid'], assignment_id=variables['assignmentId'],
                                            level=variables['level'],
                                            change_type=variables['changeType'],
                                            execution_status=variables['executionStatus'],
                                            runtime_configuration=variables['runtimeConfiguration'],
                                            dpenvlst=variables['dpenvlst'],
                                            system=variables['system'],
                                            callback_task_id=variables['callbackTaskId'],
                                            callback_url=variables['callbackUrl'],
                                            callback_username=variables['callbackUsername'],
                                            callback_password=variables['callbackPassword'],
                                            retryInterval=variables['retryInterval'],
                                            retryLimit=variables['retryLimit'])
        variables['setId'] = result["setId"]
        variables['url'] = result["url"]

    def ispwservices_regressassignment(self, variables):
        result = self.assignment_client.regress_assignment(srid=variables['srid'], assignment_id=variables['assignmentId'],
                                             level=variables['level'],
                                             change_type=variables['changeType'],
                                             execution_status=variables['executionStatus'],
                                             runtime_configuration=variables['runtimeConfiguration'],
                                             callback_task_id=variables['callbackTaskId'],
                                             callback_url=variables['callbackUrl'],
                                             callback_username=variables['callbackUsername'],
                                             callback_password=variables['callbackPassword'],
                                             retryInterval=variables['retryInterval'],
                                             retryLimit=variables['retryLimit'])
        variables['setId'] = result["setId"]
        variables['url'] = result["url"]


    def ispwservices_createrelease(self, variables):
        result = self.release_client.create_release(srid=variables['srid'], application=variables['application'],
                                                    stream=variables['stream'],
                                                    description=variables['description'], release_id=variables['relId'],
                                                    release_prefix=variables['relPrefix'],
                                                    owner=variables['owner'],
                                                    reference_number=variables['referenceNumber'],
                                                    retryInterval=variables['retryInterval'],
                                                    retryLimit=variables['retryLimit'])
        variables['relOutputId'] = result["releaseId"]
        variables['url'] = result["url"]

    def ispwservices_getreleaseinformation(self, variables):
        result = self.release_client.get_release_information(srid=variables['srid'], release_id=variables['relId'],
                                             retryInterval=variables['retryInterval'],
                                             retryLimit=variables['retryLimit'])
        variables['relOutputId'] = result["releaseId"]
        variables['application'] = result["application"]
        variables['stream'] = result["stream"]
        variables['description'] = result["description"]
        variables['owner'] = result["owner"]
        variables['referenceNumber'] = result['referenceNumber']

    def ispwservices_getreleasetasklist(self, variables):
        result = self.release_client.get_release_task_list(srid=variables['srid'], release_id=variables['relId'],
                                                           level=variables['level'],
                                                           retryInterval=variables['retryInterval'],
                                                           retryLimit=variables['retryLimit'])
        processed_result = {}
        for item in result["tasks"]:
            task_id = item['taskId']
            processed_result[task_id] = json.dumps(item)
        variables['tasks'] = processed_result

    def ispwservices_getreleasetaskinformation(self, variables):
        result = self.release_client.get_release_task_information(srid=variables['srid'], release_id=variables['relId'],
                                                                  task_id=variables['taskId'],
                                                                  retryInterval=variables['retryInterval'],
                                                                  retryLimit=variables['retryLimit'])
        for key, value in result.iteritems():
            if key == "taskId":
                variables["taskOutputId"] = value
            elif key == "type":
                variables["taskType"] = value
            else:
                variables[key] = value

    def ispwservices_generatetasksinrelease(self, variables):
        result = self.release_client.generate_tasks_in_release(srid=variables['srid'], release_id=variables['relId'],
                                                               level=variables['level'],
                                                               runtime_configuration=variables['runtimeConfiguration'],
                                                               auto_deploy=variables['autoDeploy'],
                                                               callback_task_id=variables['callbackTaskId'],
                                                               callback_url=variables['callbackUrl'],
                                                               callback_username=variables['callbackUsername'],
                                                               callback_password=variables['callbackPassword'],
                                                               retryInterval=variables['retryInterval'],
                                                               retryLimit=variables['retryLimit'])
        variables['setId'] = result["setId"]
        variables['url'] = result["url"]

    def ispwservices_getreleasetaskgeneratelisting(self, variables):
        result = self.release_client.get_release_task_generate_listing(srid=variables['srid'],
                                                                       release_id=variables['relId'],
                                                                       task_id=variables['taskId'],
                                                                       retryInterval=variables['retryInterval'],
                                                                       retryLimit=variables['retryLimit'])
        variables['listing'] = result["listing"]

    def ispwservices_promote(self, variables):
        result = self.release_client.promote(srid=variables['srid'], release_id=variables['relId'],
                                             level=variables['level'],
                                             change_type=variables['changeType'],
                                             execution_status=variables['executionStatus'],
                                             runtime_configuration=variables['runtimeConfiguration'],
                                             override=variables['override'],
                                             auto_deploy=variables['autoDeploy'],
                                             callback_task_id=variables['callbackTaskId'],
                                             callback_url=variables['callbackUrl'],
                                             callback_username=variables['callbackUsername'],
                                             callback_password=variables['callbackPassword'],
                                             retryInterval=variables['retryInterval'],
                                             retryLimit=variables['retryLimit'])
        variables['setId'] = result["setId"]
        variables['url'] = result["url"]

    def ispwservices_deploy(self, variables):
        result = self.release_client.deploy(srid=variables['srid'], release_id=variables['relId'],
                                            level=variables['level'],
                                            change_type=variables['changeType'],
                                            execution_status=variables['executionStatus'],
                                            runtime_configuration=variables['runtimeConfiguration'],
                                            dpenvlst=variables['dpenvlst'],
                                            system=variables['system'],
                                            callback_task_id=variables['callbackTaskId'],
                                            callback_url=variables['callbackUrl'],
                                            callback_username=variables['callbackUsername'],
                                            callback_password=variables['callbackPassword'],
                                             retryInterval=variables['retryInterval'],
                                             retryLimit=variables['retryLimit'])
        variables['setId'] = result["setId"]
        variables['url'] = result["url"]

    def ispwservices_regress(self, variables):
        result = self.release_client.regress(srid=variables['srid'], release_id=variables['relId'],
                                             level=variables['level'],
                                             change_type=variables['changeType'],
                                             execution_status=variables['executionStatus'],
                                             runtime_configuration=variables['runtimeConfiguration'],
                                             callback_task_id=variables['callbackTaskId'],
                                             callback_url=variables['callbackUrl'],
                                             callback_username=variables['callbackUsername'],
                                             callback_password=variables['callbackPassword'],
                                             retryInterval=variables['retryInterval'],
                                             retryLimit=variables['retryLimit'])
        variables['setId'] = result["setId"]
        variables['url'] = result["url"]

    def ispwservices_getsetinformation(self, variables):
        result = self.set_client.get_set_information(srid=variables['srid'], set_id=variables['setId'],
                                             retryInterval=variables['retryInterval'],
                                             retryLimit=variables['retryLimit'])
        variables['setOutputId'] = result["setid"]
        variables['application'] = result["applicationId"]
        variables['stream'] = result["streamName"]
        variables['description'] = result["description"]
        variables['owner'] = result["owner"]
        variables['startDate'] = result["startDate"]
        variables['startTime'] = result["startTime"]
        variables['deployActivationDate'] = result["deployActiveDate"]
        variables['deployActivationTime'] = result["deployActiveTime"]
        variables['deployImplementationDate'] = result["deployImplementationDate"]
        variables['deployImplementationTime'] = result["deployImplementationTime"]
        variables['state'] = result["state"]

    def ispwservices_pollgetsetinformation(self, variables):
        result = self.set_client.poll_get_set_information(srid=variables['srid'], set_id=variables['setId'],
                                             poll_interval=variables['pollInterval'],
                                             poll_timeout_count=variables['pollTimeoutCount'],
                                             status_field_name=variables['statusFieldName'],
                                             expected_status_list=variables['expectedStatusList'])

        variables['statusResult'] = result["status"]

    def ispwservices_getsettasklist(self, variables):
        result = self.set_client.get_set_task_list(srid=variables['srid'], set_id=variables['setId'],
                                             retryInterval=variables['retryInterval'],
                                             retryLimit=variables['retryLimit'])
        processed_result = {}
        for item in result["tasks"]:
            task_id = item['taskId']
            processed_result[task_id] = json.dumps(item)
        variables['tasks'] = processed_result

    def ispwservices_getsetdeploymentinformation(self, variables):
        result = self.set_client.get_set_deployment_information(srid=variables['srid'], set_id=variables['setId'],
                                             retryInterval=variables['retryInterval'],
                                             retryLimit=variables['retryLimit'])
        variables["createDate"] = result["createDate"]
        variables['description'] = result["description"]
        variables['environment'] = result["environment"]
        variables['packages'] = result["packages"]
        variables['requestId'] = result["requestId"]
        variables['setOutputId'] = result["setId"]
        variables['state'] = result["status"]

    def ispwservices_pollgetsetdeploymentinformation(self, variables):
        result = self.set_client.poll_get_set_deployment_information(srid=variables['srid'], set_id=variables['setId'],
                                             poll_interval=variables['pollInterval'],
                                             poll_timeout_count=variables['pollTimeoutCount'],
                                             status_field_name=variables['statusFieldName'],
                                             expected_status_list=variables['expectedStatusList'])

        variables['statusResult'] = result["status"]

    def ispwservices_fallbackset(self, variables):
        result = self.set_client.fallback_set(srid=variables['srid'], set_id=variables['setId'],
                                              change_type=variables['changeType'],
                                              execution_status=variables['executionStatus'],
                                              runtime_configuration=variables['runtimeConfiguration'],
                                              callback_task_id=variables['callbackTaskId'],
                                              callback_url=variables['callbackUrl'],
                                              callback_username=variables['callbackUsername'],
                                              callback_password=variables['callbackPassword'],
                                              retryInterval=variables['retryInterval'],
                                              retryLimit=variables['retryLimit'])
        variables['setOutputId'] = result["setId"]
        variables['url'] = result["url"]
