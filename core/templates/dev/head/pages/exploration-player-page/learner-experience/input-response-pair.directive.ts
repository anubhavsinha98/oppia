// Copyright 2017 The Oppia Authors. All Rights Reserved.
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
 * @fileoverview Directive for an input/response pair in the learner view.
 */

require(
  'pages/exploration-player-page/services/' +
  'audio-translation-manager.service.ts');
require('pages/exploration-player-page/services/exploration-engine.service.ts');
require(
  'pages/exploration-player-page/services/exploration-player-state.service.ts');
require('pages/exploration-player-page/services/player-position.service.ts');
require('pages/exploration-player-page/services/player-transcript.service.ts');
require('services/AudioPlayerService.ts');
require('services/AutogeneratedAudioPlayerService.ts');
require('services/ExplorationHtmlFormatterService.ts');

require('pages/interaction-specs.constants.ajs.ts');

angular.module('oppia').directive('inputResponsePair', [
  'UrlInterpolationService', function(UrlInterpolationService) {
    return {
      restrict: 'E',
      scope: {
        data: '=',
        oppiaAvatarImageUrl: '&',
        profilePicture: '&',
        getInputResponsePairId: '&inputResponsePairId',
        isLastPair: '&',
      },
      templateUrl: UrlInterpolationService.getDirectiveTemplateUrl(
        '/pages/exploration-player-page/learner-experience/' +
        'input-response-pair.directive.html'),
      controller: [
        '$scope', 'ExplorationEngineService', 'PlayerTranscriptService',
        'ExplorationHtmlFormatterService', 'INTERACTION_SPECS',
        'PlayerPositionService', 'COMPONENT_NAME_FEEDBACK',
        'AudioTranslationManagerService', 'AudioPlayerService',
        'AutogeneratedAudioPlayerService', 'AUDIO_HIGHLIGHT_CSS_CLASS',
        'ExplorationPlayerStateService',
        function(
            $scope, ExplorationEngineService, PlayerTranscriptService,
            ExplorationHtmlFormatterService, INTERACTION_SPECS,
            PlayerPositionService, COMPONENT_NAME_FEEDBACK,
            AudioTranslationManagerService, AudioPlayerService,
            AutogeneratedAudioPlayerService, AUDIO_HIGHLIGHT_CSS_CLASS,
            ExplorationPlayerStateService) {
          $scope.getAnswerPopoverUrl = function() {
            return UrlInterpolationService.getDirectiveTemplateUrl(
              '/pages/exploration-player-page/templates/' +
              'answer-popup-container.template.html');
          };

          $scope.isCurrentCardAtEndOfTranscript = function() {
            return PlayerTranscriptService.isLastCard(
              PlayerPositionService.getDisplayedCardIndex());
          };

          $scope.getAnswerHtml = function() {
            var displayedCard = PlayerTranscriptService.getCard(
              PlayerPositionService.getDisplayedCardIndex());
            var interaction = displayedCard.getInteraction();
            if ($scope.data) {
              return ExplorationHtmlFormatterService.getAnswerHtml(
                $scope.data.learnerInput, interaction.id,
                interaction.customizationArgs);
            }
          };

          // Returns a HTML string representing a short summary of the answer
          // , or null if the answer does not have to be summarized.
          $scope.getShortAnswerHtml = function() {
            var displayedCard = PlayerTranscriptService.getCard(
              PlayerPositionService.getDisplayedCardIndex());
            var interaction = displayedCard.getInteraction();
            var shortAnswerHtml = '';
            if ($scope.data.learnerInput.answerDetails) {
              shortAnswerHtml = $scope.data.learnerInput.answerDetails;
            } else if ($scope.data && interaction.id &&
                INTERACTION_SPECS[interaction.id].needs_summary) {
              shortAnswerHtml = (
                ExplorationHtmlFormatterService.getShortAnswerHtml(
                  $scope.data.learnerInput, interaction.id,
                  interaction.customizationArgs));
            }
            return shortAnswerHtml;
          };

          $scope.getFeedbackAudioHighlightClass = function() {
            if (!$scope.isLastPair) {
              return '';
            }
            if (AudioTranslationManagerService
              .getCurrentComponentName() ===
              COMPONENT_NAME_FEEDBACK &&
              (AudioPlayerService.isPlaying() ||
              AutogeneratedAudioPlayerService.isPlaying())) {
              return AUDIO_HIGHLIGHT_CSS_CLASS;
            }
          };
        }
      ]
    };
  }]);
