#!/usr/bin/env python3
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
import json
import os
import subprocess
import sys

import pkg_resources
import requests
from six.moves import urllib


def get_version():
    requirement = pkg_resources.Requirement.parse('git-nit')
    provider = pkg_resources.get_provider(requirement)
    return provider.version


def decode_json(raw):
    "Trap JSON decoding failures and provide more detailed errors"

    # Gerrit's REST API prepends a JSON-breaker to avoid XSS vulnerabilities
    if raw.text.startswith(")]}'"):
        trimmed = raw.text[4:]
    else:
        trimmed = raw.text

    decoded = json.loads(trimmed)
    return decoded


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


def get_review_data(review_id):
    "Return what gerrit knows about the review."
    parsed = urllib.parse.urlparse(review_id)
    gerrit_url = '{}://{}'.format(parsed.scheme, parsed.netloc)
    review, patchset = parse_review_id(review_id)
    change_url = '{}/changes/{}'.format(gerrit_url, review)
    response = requests.get(change_url)
    return decode_json(response)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--version',
        action='version',
        version=get_version(),
    )
    parser.add_argument(
        '--short-names', '-s',
        action='store_true',
        default=False,
        help='use the short repo name without the subject',
    )
    parser.add_argument(
        'review',
        help='the URL for the review',
    )
    args = parser.parse_args()

    data = get_review_data(args.review)
    review, patchset = parse_review_id(args.review)

    repo = data.get('project', '')
    short_repo = repo.rsplit('/', 1)[-1]
    if not repo:
        raise ValueError('Could not determine the repository')

    subject = data.get('subject', '')
    for old, new in [(' ', '-'), (':', ''), ("'", ''), ('"', '')]:
        subject = subject.replace(old, new)

    if args.short_names:
        clone_to = short_repo
    else:
        clone_to = '{}-{}-{}'.format(short_repo, review, subject)

    if os.path.exists(clone_to):
        sys.exit('{} already exists'.format(clone_to))

    git_cmd = [
        'git',
        'clone',
        'git://git.openstack.org/{}'.format(repo),
        clone_to,
    ]
    print('Cloning {} into {}'.format(repo, clone_to))
    print(' '.join(git_cmd))
    subprocess.check_call(git_cmd)

    git_cmd = [
        'git',
        'review',
        '-s',
    ]
    print('\nConfiguring git-review')
    print(' '.join(git_cmd))
    subprocess.check_call(git_cmd, cwd=clone_to)

    git_cmd = [
        'git',
        'review',
        '-d',
    ]
    if patchset is not None:
        target = '{},{}'.format(review, patchset)
    else:
        target = review
    git_cmd.append(target)
    print('\nDownloading {}'.format(args.review))
    print(' '.join(git_cmd))
    subprocess.check_call(git_cmd, cwd=clone_to)

    git_cmd = [
        'git',
        'remote',
        'update',
    ]
    print('\nUpdating all remotes')
    print(' '.join(git_cmd))
    subprocess.check_call(git_cmd, cwd=clone_to)

    print('\nPatch ready in {}'.format(clone_to))


if __name__ == '__main__':
    main()
