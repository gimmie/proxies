'use strict'

/* Controllers */

function EventsListCtrl($scope) {

  $scope.events = [];
  $scope.triggerEvent = function (eventName) {

    GimmieWidget.API.triggerEvent(eventName, function () {
      GimmieWidget.updatePoints();
    });

  }

  var interval = setInterval(function () {

    if (window.GimmieWidget) {
      clearInterval(interval);

      GimmieWidget.API.loadEvents([], function (data) {

        var response = data.response;
        if (response.success) {
          $scope.events = response.events;
          $scope.$apply();
        }
      });

    }

  }, 1000);

}
