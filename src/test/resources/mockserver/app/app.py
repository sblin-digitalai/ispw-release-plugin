#!flask/bin/python
#
# Copyright 2021 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

# Rewritting this project src/test/resources/docker/ispw/main.go as a flask app

from flask import Flask
from flask import request
from flask import make_response
from flask import jsonify
import traceback
import logging
from werkzeug.exceptions import HTTPException, BadRequest, NotFound, Unauthorized
from time import strftime
from logging.handlers import RotatingFileHandler
from functools import wraps
import os, io, json


app = Flask(__name__)
handler = RotatingFileHandler('/var/log/mockserver.log', maxBytes=1000000, backupCount=1)
logger_formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s')
handler.setFormatter(logger_formatter)
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)

# 409 retry testing
return409NumTimes = 0
return409Counter = 0
shouldReturn409 = False

# polling testing
returnBadResponseNumTimes = 0
pollingCounter = 0
shouldTestPolling = False


def getFile( fileName, status="200" ):
     filePath="/mockserver/responses/%s" % fileName
     if not os.path.isfile(filePath):
          app.logger.debug("Cannot find file %s" % fileName)
          raise NotFound({"code": "response_file_not_found", "description": "Unable to load response file"}, 500)

     f = io.open(filePath, "r", encoding="utf-8")
     resp = make_response( (f.read(), status) )
     resp.headers['Content-Type'] = 'application/json; charset=utf-8'
     return resp

# Error handler
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

def requires_auth(f):
    #Determines if the access token is valid
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        if token != "12345678-abcd-efgh-12345678": 
          app.logger.info('bad token: %s' % token)  
          raise Unauthorized()
        return f(*args, **kwargs)
    return decorated

def get_token_auth_header():
    """
    Obtains the access token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description": "Authorization header is expected"}, 401)
    else:
        app.logger.info('Authorization from the header: %s' % auth)
    return auth

@app.route('/')
def index():
     logRequest(request)
     return "Hello, World!"

@app.route('/exampleResponse/<exampleVariable>')
@requires_auth
def get_exampleResponse(exampleVariable):
     logRequest(request)
     app.logger.debug("The Example Variable is %s" % exampleVariable)
     return getFile("exampleResponse.json")

@app.route('/exampleFileNotFound')
@requires_auth
def get_exampleFileNotFound(exampleVariable):
     logRequest(request)
     return getFile("exampleResponseNotFound.json")

####### ISPW Specific

#### Utility Methods

# set set the polling variables
# if this route is called with 0, then 'shouldTestPolling' is turned off - i.e. /setPolling/0
# if it is called with >0 then return409 is turned on
@app.route('/setPolling/<setReturnBadResponseNumTimes>')
def setPolling(setReturnBadResponseNumTimes):
     global pollingCounter
     global shouldTestPolling
     global returnBadResponseNumTimes 
     logRequest(request)
     returnBadResponseNumTimes = int(setReturnBadResponseNumTimes)
     pollingCounter = 0
     if returnBadResponseNumTimes > 0:
        shouldTestPolling = True
     else:
        shouldTestPolling = False
     return ("shouldTestPolling is %s and number of times is set to %s" % (str(shouldTestPolling), str(returnBadResponseNumTimes)))

# set return409
# if this route is called with 0, then 'return409' is turned off - i.e. /setReturn409/0
# if it is called with >0 then return409 is turned on
@app.route('/setReturn409/<setReturn409NumTimes>')
def setReturn409(setReturn409NumTimes):
    global return409NumTimes
    global return409Counter
    global shouldReturn409
    logRequest(request)
    return409NumTimes = int(setReturn409NumTimes)
    return409Counter = 0
    if return409NumTimes > 0:
        shouldReturn409 = True
    else:
        shouldReturn409 = False

    return ("return409 is %s and number of times is set to %s" % (str(shouldReturn409), str(return409NumTimes)))

# For 409 Response testing
def createAndReturn409():
    global return409NumTimes
    global return409Counter
    global shouldReturn409
    if return409Counter == return409NumTimes:
        shouldReturn409 = False
        return409Counter = 0
        return409NumTimes = 0
    else:
        return409Counter += 1 

    response = jsonify("Conflict")
    response.status_code = 409
    return response

# For Polling Testing
def createAndReturnBadResponse(badResponseFile):
    global returnBadResponseNumTimes
    global pollingCounter
    global shouldTestPolling
    if pollingCounter == returnBadResponseNumTimes:
        shouldTestPolling = False
        pollingCounter = 0
        returnBadResponseNumTimes = 0
    else:
        pollingCounter += 1 

    return getFile(badResponseFile, "201")


### ISPW Mockserver Methods

'''
From this project src/test/resources/docker/ispw/main.go
As necessary, we will implement these tests in the Flask test mockserver instead of the go test server
    router.HandleFunc("/ispw/ispw/assignments/", ReturnAssignmentResponse).Methods("POST")
	router.HandleFunc("/ispw/ispw/assignments/{assignment_id}/tasks", ReturnAssignmentResponse).Methods("POST")
	router.HandleFunc("/ispw/ispw/assignments/{assignment_id}", GetAssignmentInformation).Methods("GET")
	router.HandleFunc("/ispw/ispw/assignments/{assignment_id}/tasks", GetTaskList).Methods("GET").Queries("level", "{[a-z]*?}")
	router.HandleFunc("/ispw/ispw/assignments/{assignment_id}/tasks/{task_id}", GetTaskInformation).Methods("GET")
	router.HandleFunc("/ispw/ispw/assignments/{assignment_id}/tasks/generate", ReturnIspwResponse).Methods("POST").Queries("level", "{[a-z]*?}")
	router.HandleFunc("/ispw/ispw/assignments/{assignment_id}/tasks/promote", ReturnIspwResponse).Methods("POST").Queries("level", "{[a-z]*?}")
	router.HandleFunc("/ispw/ispw/assignments/{assignment_id}/tasks/deploy", ReturnIspwResponse).Methods("POST").Queries("level", "{[a-z]*?}")
	router.HandleFunc("/ispw/ispw/assignments/{assignment_id}/tasks/regress", ReturnIspwResponse).Methods("POST").Queries("level", "{[a-z]*?}")

	router.HandleFunc("/ispw/ispw/releases/", CreateRelease).Methods("POST")
	router.HandleFunc("/ispw/ispw/releases/{release_id}", GetReleaseInformation).Methods("GET")
	router.HandleFunc("/ispw/ispw/releases/{release_id}/tasks", GetTaskList).Methods("GET").Queries("level", "{[a-z]*?}")
	router.HandleFunc("/ispw/ispw/releases/{release_id}/tasks/{task_id}", GetTaskInformation).Methods("GET")
	router.HandleFunc("/ispw/ispw/releases/{release_id}/tasks/generate", ReturnIspwResponse).Methods("POST").Queries("level", "{[a-z]*?}")
	router.HandleFunc("/ispw/ispw/releases/{release_id}/tasks/{task_id}/listing", GetReleaseTaskGenerateListing).Methods("GET")
	router.HandleFunc("/ispw/ispw/releases/{release_id}/tasks/promote", ReturnIspwResponse).Methods("POST").Queries("level", "{[a-z]*?}")
	router.HandleFunc("/ispw/ispw/releases/{release_id}/tasks/deploy", ReturnIspwResponse).Methods("POST").Queries("level", "{[a-z]*?}")
	router.HandleFunc("/ispw/ispw/releases/{release_id}/tasks/regress", ReturnIspwResponse).Methods("POST").Queries("level", "{[a-z]*?}")

	router.HandleFunc("/ispw/ispw/sets/{set_id}", GetSetInformation).Methods("GET")
	router.HandleFunc("/ispw/ispw/sets/{set_id}/tasks", GetTaskList).Methods("GET")
	router.HandleFunc("/ispw/ispw/sets/{set_id}/deployment", GetSetDeploymentInformation).Methods("GET")
	router.HandleFunc("/ispw/ispw/sets/{set_id}/tasks/fallback", ReturnIspwResponse).Methods("POST")
    '''
# SETS
# GetSetInformation
@app.route('/ispw/ispwMock/sets/<set_id>')
@requires_auth
def get_setInformation(set_id):
    global shouldReturn409
    global return409NumTimes
    global return409Counter
    global shouldTestPolling
    global returnBadResponseNumTimes
    global pollingCounter
    logRequest(request)
    app.logger.debug("The set_id is %s, shouldReturn409 is %s, return409NumTimes is %s, return409Counter is %s" % (set_id, str(shouldReturn409), str(return409NumTimes), str(return409Counter)))
    app.logger.debug("The set_id is %s, shouldTestPolling is %s, returnBadResponseNumTimes is %s, pollingCounter is %s" % (set_id, str(shouldTestPolling), str(returnBadResponseNumTimes), str(pollingCounter)))
    if shouldReturn409:
        return createAndReturn409()
    elif shouldTestPolling:
        return createAndReturnBadResponse("pollingBadResponseSetInfo.json")
    else:
        return getFile("getSetInfo.json", "201")

# GetSetDeploymentInformation
@app.route('/ispw/ispwMock/sets/<set_id>/deployment')
@requires_auth
def get_setDeployInformation(set_id):
    global shouldReturn409
    global return409NumTimes
    global return409Counter
    global shouldTestPolling
    global returnBadResponseNumTimes
    global pollingCounter
    logRequest(request)
    app.logger.debug("The set_id is %s, shouldReturn409 is %s, return409NumTimes is %s, return409Counter is %s" % (set_id, str(shouldReturn409), str(return409NumTimes), str(return409Counter)))
    app.logger.debug("The set_id is %s, shouldTestPolling is %s, returnBadResponseNumTimes is %s, pollingCounter is %s" % (set_id, str(shouldTestPolling), str(returnBadResponseNumTimes), str(pollingCounter)))
    if shouldReturn409:
        return createAndReturn409()
    elif shouldTestPolling:
        return createAndReturnBadResponse("pollingBadResponseSetDeployInfo.json")
    else:
        return getFile("getSetDeployInfo.json", "201")

# RELEASES
# GetReleaseInformation
@app.route('/ispw/ispwMock/releases/<release_id>')
@requires_auth
def get_releaseInformation(release_id):
    global shouldReturn409
    logRequest(request)
    app.logger.debug("The release_id is %s, shouldReturn is %s, numTimes is %s, counter is %s" % (release_id, str(shouldReturn409), str(return409NumTimes), str(return409Counter)))
    if shouldReturn409:
        return createAndReturn409()
    else:
        return getFile("getReleaseInformation.json", "201")

# ASSIGNMENTS
# router.HandleFunc("/ispw/ispw/assignments/{assignment_id}/tasks/promote", ReturnIspwResponse).Methods("POST").Queries("level", "{[a-z]*?}")
@app.route('/ispw/ispwMock/assignments/<assignment_id>/tasks/promote', methods=['POST'])
@requires_auth
def promote_assignment(assignment_id):
    global shouldReturn409
    logRequest(request)
    app.logger.debug("The release_id is %s, shouldReturn is %s, numTimes is %s, counter is %s" % (assignment_id, str(shouldReturn409), str(return409NumTimes), str(return409Counter)))
    content = request.json
    if shouldReturn409:
        return createAndReturn409()
    else:
        return getFile("postIspwResponse.json", "201")  



# Use for detailed request debug
def logRequest(request):
     app.logger.debug("**************** LOGGING REQUEST")
     app.logger.debug("request.url=%s" % request.url)
     app.logger.debug("request.headers=%s" % request.headers )
     if request.json:
          app.logger.debug("request.json=%s" % request.json)
     else:
          app.logger.debug("request.data=%s" % request.data)
     app.logger.debug("request.form=%s" % request.form)
     app.logger.debug("****************")

# Added for debug purposes - logging all requests
@app.route("/json")
def get_json():
    data = {"Name":"Some Name","Books":"[Book1, Book2, Book3]"}
    return jsonify(data_WRONG) # INTENTIONAL ERROR FOR TRACEBACK EVENT

@app.after_request
def after_request(response):
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    app.logger.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
    return response

@app.errorhandler(Exception)
def exceptions(e):
    tb = traceback.format_exc()
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    app.logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, tb)
    return e


if __name__ == '__main__':
     app.run()
