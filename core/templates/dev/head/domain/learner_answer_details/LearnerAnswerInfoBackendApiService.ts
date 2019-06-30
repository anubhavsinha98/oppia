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
 * @fileoverview Service to record learner answer info.
 */

require('domain/utilities/UrlInterpolationService.ts');

require('domain/learner_answer_details/learner-answer-info.constants.ts');

oppia.factory('LearnerAnswerInfoBackendApiService', [
  '$http', 'UrlInterpolationService', 'SUBMIT_LEARNER_ANSWER_INFO_URL',
  function($http, UrlInterpolationService, SUBMIT_LEARNER_ANSWER_INFO_URL) {
    return {
      recordLearnerAnswerInfo: function(expId, stateName, interactionId,
          learnerAnswerInfo) {
        var recordLearnerAnswerInfoUrl = UrlInterpolationService.interpolateUrl(
          SUBMIT_LEARNER_ANSWER_INFO_URL, {
            exploration_id: expId
          });
        $http.post(recordLearnerAnswerInfoUrl, {
          state_name: stateName,
          interaction_id: interactionId,
          answer: learnerAnswerInfo.answer,
          answer_details: learnerAnswerInfo.answerDetails
        });
      }
    };
  }
]);
