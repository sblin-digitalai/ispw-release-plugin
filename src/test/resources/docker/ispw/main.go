package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"github.com/gorilla/mux"
)

// Assignment struct used to return json after ReturnAssignmentResponse is called
type Assignment struct {
	AssignmentID string `json:"assignmentId"`
	URL          string `json:"url"`
}

// AssignmentInformation struct used to return json after getAssignmentInformation is called
type AssignmentInformation struct {
	Application   string `json:"application"`
	DefaultPath   string `json:"defaultPath"`
	Description   string `json:"description"`
	Owner         string `json:"owner"`
	ProjectNumber string `json:"projectNumber"`
	RefNumber     string `json:"refNumber"`
	Release       string `json:"release"`
	Stream        string `json:"stream"`
	UserTag       string `json:"userTag"`
}

// Release struct used to return json after createRelease is called
type Release struct {
	ReleaseID string `json:"releaseId"`
	URL       string `json:"url"`
}

// ReleaseInformation struct used to return json after getReleaseInformation is called
type ReleaseInformation struct {
	RelOutputID     string `json:"releaseId"`
	Application     string `json:"application"`
	Stream          string `json:"stream"`
	Description     string `json:"description"`
	Owner           string `json:"owner"`
	ReferenceNumber string `json:"referenceNumber"`
}

// SetInformation struct used to return json after getSetInformation is called
type SetInformation struct {
	SetOutputID              string `json:"setid"`
	Application              string `json:"applicationId"`
	Stream                   string `json:"streamName"`
	Description              string `json:"description"`
	Owner                    string `json:"owner"`
	StartDate                string `json:"startDate"`
	StartTime                string `json:"startTime"`
	DeployActivationDate     string `json:"deployActiveDate"`
	DeployActivationTime     string `json:"deployActiveTime"`
	DeployImplementationDate string `json:"deployImplementationDate"`
	DeployImplementationTime string `json:"deployImplementationTime"`
	State                    string `json:"state"`
}

// Task struct used to define task info in json
type Task struct {
	TaskID string `json:"taskId"`
	UserID string `json:"userId"`
	Stream string `json:"stream"`
}

// Tasks is an array of task items
type Tasks []Task

// TaskList is an array of tasks, with a named json element tasks.
type TaskList struct {
	TaskList Tasks `json:"tasks"`
}

// SetDeploymentInformation struct used to return json after getSetDeploymentInformation is called
type SetDeploymentInformation struct {
	CreateDate  string `json:"createDate"`
	Description string `json:"description"`
	Environment string `json:"environment"`
	Packages    Packages `json:"packages"`
	RequestID   int `json:"requestId"`
	SetOutputID string `json:"setId"`
	State       string `json:"status"`
}

// Packages struct used to define a package in json
type Packages struct {
	PackageID       int `json:"packageId"`
	SubEnvironment  string `json:"subEnvironment"`
	System          string `json:"system"`
	DeploymentItems DeploymentItems `json:"deploymentItems"`
}

// DeploymentItems according to doc, there can be only one.
type DeploymentItems struct {
	Item int `json:"item"`
	Part int `json:"part"`
	Name string `json:"name"`
}

// IspwResponse struct used to return json after regress, promote or deploy is called
type IspwResponse struct {
	SetID   string `json:"setId"`
	Message string `json:"message"`
	URL     string `json:"url"`
}

// Listing struct used to return json after GetReleaseTaskGenerateListing is called.
type Listing struct {
	Listing string `json:"listing"`
}

func main() {
	router := mux.NewRouter().StrictSlash(true)
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

	log.Fatal(http.ListenAndServe(":8080", router))
}

// ReturnAssignmentResponse sends a dummy response back
func ReturnAssignmentResponse(res http.ResponseWriter, req *http.Request) {
	res.Header().Set("Content-Type", "application/json")
	c := Assignment{"assignmentID", "http://ispw:8080/ispw/ispw/assignments/assignmentid"}
	outgoingJSON, err := json.Marshal(c)
	if err != nil {
		log.Println(err.Error())
		http.Error(res, err.Error(), http.StatusInternalServerError)
		return
	}
	res.WriteHeader(http.StatusCreated)
	fmt.Fprint(res, string(outgoingJSON))
}

// GetAssignmentInformation sends a dummy response back
func GetAssignmentInformation(res http.ResponseWriter, req *http.Request) {
	res.Header().Set("Content-Type", "application/json")
	c := AssignmentInformation{"FOO", "DEV1", "ASSIGNMENT FOR FOOBAR", "FOOUSR", "FB000001", "1234", "REL1", "BAR", "USRTAG"}
	outgoingJSON, err := json.Marshal(c)
	if err != nil {
		log.Println(err.Error())
		http.Error(res, err.Error(), http.StatusInternalServerError)
		return
	}
	res.WriteHeader(http.StatusCreated)
	fmt.Fprint(res, string(outgoingJSON))
}

// CreateRelease sends a dummy response back
func CreateRelease(res http.ResponseWriter, req *http.Request) {
	res.Header().Set("Content-Type", "application/json")
	c := Release{"relid", "http://ispw:8080/ispw/ispw/releases/relid"}
	outgoingJSON, err := json.Marshal(c)
	if err != nil {
		log.Println(err.Error())
		http.Error(res, err.Error(), http.StatusInternalServerError)
		return
	}
	res.WriteHeader(http.StatusCreated)
	fmt.Fprint(res, string(outgoingJSON))
}

// GetReleaseInformation sends a dummy response back
func GetReleaseInformation(res http.ResponseWriter, req *http.Request) {
	res.Header().Set("Content-Type", "application/json")
	c := ReleaseInformation{"relid", "app", "stream", "something", "xebia", "1234"}
	outgoingJSON, err := json.Marshal(c)
	if err != nil {
		log.Println(err.Error())
		http.Error(res, err.Error(), http.StatusInternalServerError)
		return
	}
	res.WriteHeader(http.StatusCreated)
	fmt.Fprint(res, string(outgoingJSON))
}

// GetTaskInformation sends a dummy response back
func GetTaskInformation(res http.ResponseWriter, req *http.Request) {
	res.Header().Set("Content-Type", "application/json")
	c := Task{"7E12E3B57A02", "FOOUSER", "BAR"}
	outgoingJSON, err := json.Marshal(c)
	if err != nil {
		log.Println(err.Error())
		http.Error(res, err.Error(), http.StatusInternalServerError)
		return
	}
	res.WriteHeader(http.StatusCreated)
	fmt.Fprint(res, string(outgoingJSON))
}

// GetReleaseTaskGenerateListing sends a dummy response back
func GetReleaseTaskGenerateListing(res http.ResponseWriter, req *http.Request) {
	res.Header().Set("Content-Type", "application/json")
	c := Listing{"Somelisting"}
	outgoingJSON, err := json.Marshal(c)
	if err != nil {
		log.Println(err.Error())
		http.Error(res, err.Error(), http.StatusInternalServerError)
		return
	}
	res.WriteHeader(http.StatusCreated)
	fmt.Fprint(res, string(outgoingJSON))
}

// ReturnIspwResponse sends a dummy response back
func ReturnIspwResponse(res http.ResponseWriter, req *http.Request) {
	res.Header().Set("Content-Type", "application/json")
	c := IspwResponse{"ISPW2345", "This worked", "http://foobarsoft.com/ispw/w3t/sets/s0123456"}
	outgoingJSON, err := json.Marshal(c)
	if err != nil {
		log.Println(err.Error())
		http.Error(res, err.Error(), http.StatusInternalServerError)
		return
	}
	res.WriteHeader(http.StatusCreated)
	fmt.Fprint(res, string(outgoingJSON))

}

// GetSetInformation sends a dummy response back
func GetSetInformation(res http.ResponseWriter, req *http.Request) {
	res.Header().Set("Content-Type", "application/json")
	c := SetInformation{"someId", "app", "stream", "something", "xebia", "08/10", "11am", "09/10", "11am", "10/10", "11am", "DONE"}
	outgoingJSON, err := json.Marshal(c)
	if err != nil {
		log.Println(err.Error())
		http.Error(res, err.Error(), http.StatusInternalServerError)
		return
	}
	res.WriteHeader(http.StatusCreated)
	fmt.Fprint(res, string(outgoingJSON))
}

// GetTaskList sends a dummy response back
func GetTaskList(res http.ResponseWriter, req *http.Request) {
	res.Header().Set("Content-Type", "application/json")
	tasks := Tasks{Task{"7E12E3B57A02", "FOOUSER", "BAR"}, Task{"7E12E3B59441", "FOOUSER", "BAR"}}
	c := TaskList{tasks}
	outgoingJSON, err := json.Marshal(c)
	if err != nil {
		log.Println(err.Error())
		http.Error(res, err.Error(), http.StatusInternalServerError)
		return
	}
	res.WriteHeader(http.StatusCreated)
	fmt.Fprint(res, string(outgoingJSON))
}

// GetSetDeploymentInformation sends a dummy response back
func GetSetDeploymentInformation(res http.ResponseWriter, req *http.Request) {
	res.Header().Set("Content-Type", "application/json")
	dItem := DeploymentItems{1, 5161, "TSUBR05"}
	packages := Packages{1, "DEVL", "MP3000", dItem}
	c := SetDeploymentInformation{"2017-08-18", "MyGen", "FOOENV", packages, 3193, "S0000009884", "Completed"}
	outgoingJSON, err := json.Marshal(c)
	if err != nil {
		log.Println(err.Error())
		http.Error(res, err.Error(), http.StatusInternalServerError)
		return
	}
	res.WriteHeader(http.StatusCreated)
	fmt.Fprint(res, string(outgoingJSON))
}
