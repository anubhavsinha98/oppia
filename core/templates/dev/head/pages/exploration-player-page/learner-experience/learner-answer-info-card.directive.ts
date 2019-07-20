// Copyright 2019 The Oppia Authors. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS-IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/**
 * @fileoverview Directive for navigation in the conversation skin.
 */

require('domain/utilities/UrlInterpolationService.ts');
require('pages/exploration-player-page/services/learner-answer-info.service.ts')

var oppia = require('AppInit.ts').module;

oppia.directive('learnerAnswerInfoCard', [
  'UrlInterpolationService', function(UrlInterpolationService) {
    return {
      restrict: 'E',
      scope: {
        submitAnswer: '&submitAnswer'
      },
      templateUrl: UrlInterpolationService.getDirectiveTemplateUrl(
        '/pages/exploration-player-page/learner-experience/' +
        'learner-answer-info-card.directive.html'),
      controller: [
        '$scope', 'LearnerAnswerInfoService',
        function($scope, LearnerAnswerInfoService) {
          $scope.answerDetails = null;
          $scope.submitLearnerAnswerInfo = function() {
            LearnerAnswerInfoService.recordLearnerAnswerInfo(
              $scope.answerDetails);
            $scope.submitAnswer()(
              LearnerAnswerInfoService.getCurrentAnswer(),
              LearnerAnswerInfoService.getCurrentInteractionRulesService());
          };
        }
      ]
    };
  }
]
);
