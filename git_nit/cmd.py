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

from __future__ import print_function

import argparse
import os

import pkg_resources
from six.moves import urllib


def get_version():
    requirement = pkg_resources.Requirement.parse('git-nit')
    provider = pkg_resources.get_provider(requirement)
    return provider.version


def parse_review_id(review_id):
    "Given a review URL or ID return the review number and PS number, if any."
    parsed = urllib.parse.urlparse(review_id)
    if parsed.fragment:
        # https://review.openstack.org/#/c/564559/ style
        parts = [
            p
            for p in parsed.fragment.split('/')
            if p and p != 'c'
        ]
    else:
        # https://review.openstack.org/564559/ style
        parts = [
            p
            for p in parsed.path.split('/')
            if p
        ]
    if not parts:
        raise ValueError('Could not parse review ID {!r}'.format(review_id))
    review = parts[0]
    if len(parts) > 1:
        patchset = parts[1]
    else:
        patchset = None
    return (review, patchset)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--version',
        action='version',
        version=get_version(),
    )
    parser.add_argument(
        '--project-dir',
        default=os.environ.get('PROJECT_DIR', '.'),
        help=(
            'parent directory for creating a new project, '
            'defaults to $PROJECT_DIR or "."'),
    )
    parser.add_argument(
        'review',
        help='the URL for the review',
    )
    args = parser.parse_args()

    review, patchset = parse_review_id(args.review)
    print(review, patchset)

if __name__ == '__main__':
    main()
