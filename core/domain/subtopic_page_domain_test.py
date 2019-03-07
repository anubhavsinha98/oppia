# coding: utf-8
#
# Copyright 2018 The Oppia Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for subtopic page domain objects."""

from constants import constants
from core.domain import state_domain
from core.domain import subtopic_page_domain
from core.tests import test_utils
import utils


class SubtopicPageChangeDomainUnitTests(test_utils.GenericTestBase):
    """Tests for subtopic page change domain objects."""
    user_id = 'user_id'
    topic_id = 'topic_id'
    subtopic_id = 1

    def setUp(self):
        super(SubtopicPageChangeDomainUnitTests, self).setUp()
        self.subtopic_page_change = subtopic_page_domain.SubtopicPageChange({
            'cmd': subtopic_page_domain.CMD_UPDATE_SUBTOPIC_PAGE_PROPERTY,
            'subtopic_id': 1,
            'property_name': 'page_contents_html',
            'new_value': 'a',
            'old_value': 'b'
            })

    def test_init_cmdnotindict_raisesexception(self):
        with self.assertRaisesRegexp(Exception, 'Invalid change_dict *'):
            subtopic_page_domain.SubtopicPageChange({
                'subtopic_id': 1,
                'property_name': 'page_contents_html',
                'new_value': 'a',
                'old_value': 'b'
            })

    def test_init_invalidpropertyname_raisesexception(self):
        with self.assertRaisesRegexp(Exception, 'Invalid change_dict *'):
            subtopic_page_domain.SubtopicPageChange({
                'cmd': subtopic_page_domain.CMD_UPDATE_SUBTOPIC_PAGE_PROPERTY,
                'subtopic_id': 1,
                'property_name': 'not in subtopic page properties',
                'new_value': 'a',
                'old_value': 'b'
            })

    def test_init_withinvalidcmd_raisesexception(self):
        with self.assertRaisesRegexp(Exception, 'Invalid change_dict *'):
            subtopic_page_domain.SubtopicPageChange({
                'cmd': 'subtopic changed',
                'subtopic_id': 1,
                'property_name': 'page_contents_html',
                'new_value': 'a',
                'old_value': 'b'
            })

    def test_init_cmdcreatenew_notraisesexception(self):
        subtopic_page_change = subtopic_page_domain.SubtopicPageChange({
            'cmd': subtopic_page_domain.CMD_CREATE_NEW,
            'subtopic_id': 1,
            'topic_id': self.topic_id,
            'property_name': 'page_contents_html',
            'new_value': 'a',
            'old_value': 'b'
        })
        expected_subtopic_page_change_dict = {
            'cmd': subtopic_page_domain.CMD_CREATE_NEW,
            'topic_id': self.topic_id
        }
        self.assertEqual(
            expected_subtopic_page_change_dict,
            subtopic_page_change.to_dict())

    def test_to_dict(self):
        expected_subtopic_page_change_dict = {
            'cmd': subtopic_page_domain.CMD_UPDATE_SUBTOPIC_PAGE_PROPERTY,
            'property_name': 'page_contents_html',
            'new_value': 'a',
            'old_value': 'b'
        }
        self.assertEqual(
            expected_subtopic_page_change_dict,
            self.subtopic_page_change.to_dict())


class SubtopicPageDomainUnitTests(test_utils.GenericTestBase):
    """Tests for subtopic page domain objects."""
    topic_id = 'topic_id'
    subtopic_id = 1

    def setUp(self):
        super(SubtopicPageDomainUnitTests, self).setUp()
        self.subtopic_page = (
            subtopic_page_domain.SubtopicPage.create_default_subtopic_page(
                self.subtopic_id, self.topic_id))

    def test_to_dict(self):
        expected_subtopic_page_dict = {
            'id': 'topic_id-1',
            'topic_id': 'topic_id',
            'page_contents': {
                'subtitled_html': {
                    'html': '',
                    'content_id': 'content'
                },
                'content_ids_to_audio_translations': {
                    'content': {}
                },
            },
            'language_code': constants.DEFAULT_LANGUAGE_CODE,
            'version': 0
        }
        self.assertEqual(self.subtopic_page.to_dict(),
                         expected_subtopic_page_dict)

    def test_create_default_subtopic_page(self):
        """Tests the create_default_topic() function."""
        subtopic_page = (
            subtopic_page_domain.SubtopicPage.create_default_subtopic_page(
                self.subtopic_id, self.topic_id))

        expected_subtopic_page_dict = {
            'id': 'topic_id-1',
            'topic_id': 'topic_id',
            'page_contents': {
                'subtitled_html': {
                    'html': '',
                    'content_id': 'content'
                },
                'content_ids_to_audio_translations': {
                    'content': {}
                },
            },
            'language_code': constants.DEFAULT_LANGUAGE_CODE,
            'version': 0
        }
        self.assertEqual(subtopic_page.to_dict(), expected_subtopic_page_dict)

    def test_get_subtopic_page_id(self):
        self.assertEqual(
            subtopic_page_domain.SubtopicPage.get_subtopic_page_id('abc', 1),
            'abc-1')

    def test_get_subtopic_id_from_subtopic_page_id(self):
        self.assertEqual(
            self.subtopic_page.get_subtopic_id_from_subtopic_page_id(), 1)

    def _assert_validation_error(self, expected_error_substring):
        """Checks that the topic passes strict validation."""
        with self.assertRaisesRegexp(
            utils.ValidationError, expected_error_substring):
            self.subtopic_page.validate()

    def test_subtopic_page_validation(self):
        self.subtopic_page.version = 'a'
        self._assert_validation_error('Expected version number')

    def test_subtopic_topic_id_validation(self):
        self.subtopic_page.topic_id = 1
        self._assert_validation_error('Expected topic_id to be a string')

    def test_language_code_validation(self):
        self.subtopic_page.language_code = 0
        self._assert_validation_error('Expected language code to be a string')

        self.subtopic_page.language_code = 'xz'
        self._assert_validation_error('Invalid language code')

    def test_update_audio(self):
        content_ids_to_audio_translations_dict = {
            'content': {
                'en': {
                    'filename': 'test.mp3',
                    'file_size_bytes': 100,
                    'needs_update': False
                }
            }
        }
        expected_subtopic_page_dict = {
            'id': 'topic_id-1',
            'topic_id': 'topic_id',
            'page_contents': {
                'subtitled_html': {
                    'html': '',
                    'content_id': 'content'
                },
                'content_ids_to_audio_translations':
                    content_ids_to_audio_translations_dict,
            },
            'language_code': constants.DEFAULT_LANGUAGE_CODE,
            'version': 0
        }
        self.subtopic_page.update_page_contents_audio(
            content_ids_to_audio_translations_dict)
        self.assertEqual(self.subtopic_page.to_dict(),
                         expected_subtopic_page_dict)

    def test_update_html(self):
        expected_subtopic_page_dict = {
            'id': 'topic_id-1',
            'topic_id': 'topic_id',
            'page_contents': {
                'subtitled_html': {
                    'html': 'hello world',
                    'content_id': 'content'
                },
                'content_ids_to_audio_translations': {
                    'content': {}
                }
            },
            'language_code': constants.DEFAULT_LANGUAGE_CODE,
            'version': 0
        }
        self.subtopic_page.update_page_contents_html({
            'html': 'hello world',
            'content_id': 'content'
        })
        self.assertEqual(self.subtopic_page.to_dict(),
                         expected_subtopic_page_dict)


class SubtopicPageContentsDomainUnitTests(test_utils.GenericTestBase):
    def setUp(self):
        super(SubtopicPageContentsDomainUnitTests, self).setUp()
        self.subtopic_page_contents = (
            subtopic_page_domain.SubtopicPageContents
            .create_default_subtopic_page_contents())

    def _assert_validation_error(self, expected_error_substring):
        """Checks that the topic passes strict validation."""
        with self.assertRaisesRegexp(
            utils.ValidationError, expected_error_substring):
            self.subtopic_page_contents.validate()

    def test_create_default_subtopic_page(self):
        subtopic_page_contents = (
            subtopic_page_domain.SubtopicPageContents
            .create_default_subtopic_page_contents())
        expected_subtopic_page_contents_dict = {
            'subtitled_html': {
                'html': '',
                'content_id': 'content'
            },
            'content_ids_to_audio_translations': {
                'content': {}
            }
        }
        self.assertEqual(subtopic_page_contents.to_dict(),
                         expected_subtopic_page_contents_dict)

    def test_content_ids_to_audio_translations_validation(self):
        # When the content_ids_to_audio_translations is not of dict type.
        self.subtopic_page_contents.content_ids_to_audio_translations = 1
        self._assert_validation_error(
            'Expected content_ids_to_audio_translations to be a dict')

        # When the content_ids_to_audio_translations contains the content_jd
        # not present in subtopic page.
        self.subtopic_page_contents.subtitled_html = (
            state_domain.SubtitledHtml('1', '<p>Test</p>'))
        self.subtopic_page_contents.content_ids_to_audio_translations = {
            'content_id_3': {}
        }
        self._assert_validation_error(
            'Expected content_ids_to_audio_translations to contain '
            'only content_ids in the subtopic page.')

        # When the content_ids_to_audio_translations contains content_id not
        # of basestring type.
        self.subtopic_page_contents.content_ids_to_audio_translations = {
            1: {}}
        self._assert_validation_error(
            'Expected content_id to be a string, received: 1')

        # When the content_ids_to_audio_translations contains
        # audio_translations is not of dict type.
        self.subtopic_page_contents.content_ids_to_audio_translations = {
            'content_id': 1
        }
        self._assert_validation_error(
            'Expected audio_translations to be a dict, received 1')

        # When the content_ids_to_audio_translations has audio translations
        #  whose language code is not of string type.
        self.subtopic_page_contents.content_ids_to_audio_translations = {
            'content': {
                1: {}
            }
        }
        self._assert_validation_error(
            'Expected language code to be a string, received: 1')

        # When the content_ids_to_audio_translations has audio translations
        # whose language code in unrecognized.
        self.subtopic_page_contents.content_ids_to_audio_translations = {
            'content': {
                'a': {}
            }
        }
        self._assert_validation_error('Unrecognized language code: a')

    def test_to_and_from_dict(self):
        subtopic_page_contents_dict = {
            'subtitled_html': {
                'html': 'test',
                'content_id': 'content'
            },
            'content_ids_to_audio_translations': {
                'content': {
                    'en': {
                        'filename': 'test.mp3',
                        'file_size_bytes': 100,
                        'needs_update': False
                    }
                }
            }
        }
        subtopic_page_contents = (
            subtopic_page_domain.SubtopicPageContents.from_dict(
                subtopic_page_contents_dict))
        self.assertEqual(subtopic_page_contents.to_dict(),
                         subtopic_page_contents_dict)
