/*
 * Copyright 2021 XEBIALABS
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

'use strict';

(function () {

    var ISPWTileController = function ($scope, ReleasesService, XlrTileHelper) {
        var vm = this;
        if ($scope.xlrDashboard) {
            // summary page
            vm.release = $scope.xlrDashboard.release;
            vm.tile = $scope.xlrTile.tile;
            vm.config = vm.tile.properties;
        } else {
            // details page
            vm.release = $scope.xlrTileDetailsCtrl.release;
            vm.tile = $scope.xlrTileDetailsCtrl.tile;
            vm.config = vm.tile.properties;
        }


        function load() {
            vm.allISPWTasks = getAllISPWTasks(vm.release, vm.config);
            vm.counts = XlrTileHelper.countTasksByStatus(vm.allISPWTasks);
            vm.totalCount = vm.allISPWTasks.length;
            vm.gridOptions = getGridOptions(vm.allISPWTasks);
            if(vm.config.action){
                vm.chartOptions = XlrTileHelper.getChartOptions({
                    label: vm.config.action,
                    total: vm.totalCount
                });
            } else {
                vm.chartOptions = XlrTileHelper.getChartOptions({
                    label: "ispw task",
                    total: vm.totalCount
                });
            }
            
        
        }

        function getAllISPWTasks(release) {
            var allTasks = ReleasesService.getLeafTasks(release)
            return _(ReleasesService.getLeafTasks(release))
                .filter(function (task) {
                    var shouldInclude = false;
                    if (task.scriptDefinitionType && (task.scriptDefinitionType).startsWith("ispwServices.")){
                        if (!_.isEmpty(vm.config.action)){
                            if (vm.config.action.length > 1 && vm.config.action.includes("*")) {
                                var match = vm.config.action.replace("*", "");
                                shouldInclude = task.scriptDefinitionType.toLowerCase().includes(match.toLowerCase());
                            } else {
                                shouldInclude = (task.scriptDefinitionType == "ispwServices." + vm.config.action);
                            }
                        } else {
                            shouldInclude = true; 
                        }
                    }
                    return shouldInclude;
                })
                .map(function (task) {
                    var theId = task.inputProperties.relId ? task.inputProperties.relId : 
                                    task.inputProperties.assignmentId ? task.inputProperties.assignmentId : 
                                    task.inputProperties.setId ? task.inputProperties.setId : 
                                    task.inputProperties.taskId ? task.inputProperties.taskId : "";
                    var theType = task.scriptDefinitionType ? task.scriptDefinitionType.replace("ispwServices.", ""): "";
                    return {
                        taskName: task.title,
                        taskType: theType,
                        srId: task.inputProperties.srid,
                        application: task.inputProperties.appl,
                        relId: theId,
                        taskStatus: task.status,
                        taskStatusCategory: XlrTileHelper.getCategoryByTaskStatus(task.status)
                    };
                })
                .value();
        }


        function getGridOptions(allISPWTasks) {
            var columnDefs = [
                {
                    displayName: "Task",
                    field: "taskName",
                    cellTemplate: "static/@project.version@/include/ISPWServicesTile/grid/ispw-name-cell-template.html",
                    //filterHeaderTemplate: "<div data-ng-include=\"'partials/releases/grid/templates/name-filter-template.html'\"></div>",
                    enableColumnMenu: false,
                    width: '20%'
                },
                {
                    displayName: "Task Type",
                    field: "taskType",
                    cellTemplate: "static/@project.version@/include/ISPWServicesTile/grid/ispw-type-cell-template.html",
                    //filterHeaderTemplate: "<div data-ng-include=\"'partials/releases/grid/templates/name-filter-template.html'\"></div>",
                    enableColumnMenu: false,
                    width: '20%'
                },
                {
                    displayName: "SR ID",
                    field: "srId",
                    cellTemplate: "static/@project.version@/include/ISPWServicesTile/grid/ispw-srid-cell-template.html",
                    //filterHeaderTemplate: "<div data-ng-include=\"'partials/releases/grid/templates/name-filter-template.html'\"></div>",
                    enableColumnMenu: false,
                    width: '20%'
                },
                {
                    displayName: "Request - Release, Assign, Set or Task ID",
                    field: "relId",
                    cellTemplate: "static/@project.version@/include/ISPWServicesTile/grid/ispw-relid-cell-template.html",
                    //filterHeaderTemplate: "<div data-ng-include=\"'partials/releases/grid/templates/name-filter-template.html'\"></div>",
                    enableColumnMenu: false,
                    width: '20%'
                },
                {
                    displayName: "Status",
                    field: "taskStatusCategory",
                    cellTemplate: "static/@project.version@/include/ISPWServicesTile/grid/ispw-status-cell-template.html",
                    //filterHeaderTemplate: "<div data-ng-include=\"'partials/releases/grid/templates/name-filter-template.html'\"></div>",
                    enableColumnMenu: false,
                    width: '20%'
                }
            ];
            return XlrTileHelper.getGridOptions(allISPWTasks, columnDefs);
        }

        load();

    };
    ISPWTileController.$inject = ['$scope', 'ReleasesService', 'XlrTileHelper'];

    angular.module('xlrelease.ISPWServices.tile', []);
    angular.module('xlrelease.ISPWServices.tile').controller('ispwServices.ISPWTileController', ISPWTileController);

})();
