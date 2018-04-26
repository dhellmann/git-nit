#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from git_nit import cmd

import testscenarios.testcase
import testtools


class ParseReviewIDTest(testscenarios.testcase.WithScenarios,
                        testtools.TestCase):

    scenarios = [
        ('fragment with patchset', {
            'url': 'https://review.openstack.org/#/c/564559/5/',
            'review': '564559',
            'patchset': '5',
        }),
        ('fragment with patchset, no trailing slash', {
            'url': 'https://review.openstack.org/#/c/564559/5',
            'review': '564559',
            'patchset': '5',
        }),
        ('fragment without patchset', {
            'url': 'https://review.openstack.org/#/c/564559/',
            'review': '564559',
            'patchset': None,
        }),
        ('fragment without patchset, no trailing slash', {
            'url': 'https://review.openstack.org/#/c/564559',
            'review': '564559',
            'patchset': None,
        }),
        ('path with patchset', {
            'url': 'https://review.openstack.org/564559/5/',
            'review': '564559',
            'patchset': '5',
        }),
        ('path with patchset, no trailing slash', {
            'url': 'https://review.openstack.org/564559/5',
            'review': '564559',
            'patchset': '5',
        }),
        ('path without patchset', {
            'url': 'https://review.openstack.org/564559/',
            'review': '564559',
            'patchset': None,
        }),
        ('path without patchset, no trailing slash', {
            'url': 'https://review.openstack.org/564559',
            'review': '564559',
            'patchset': None,
        }),
    ]

    def test(self):
        review, patchset = cmd.parse_review_id(self.url)
        self.assertEqual(
            (self.review, self.patchset),
            (review, patchset),
        )
