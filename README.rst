=========
 git-nit
=========

A git command for fixing nit-picky changes on gerrit reviews.

git-nit is a tool that helps grabbing existing reviews on gerrit and
layering on a new patch to fix nits.

Installing
==========

Install git-nit with pip::

  $ pip install --user git-nit

Using
=====

To clone a patch to a local working directory, pass the URL of the
patch as the first argument.

::

  $ git nit https://review.openstack.org/#/c/564559/
  release-tools-564559-finish-moving-announce.sh-to-releases-repo-by-deleting-it
  Cloning openstack-infra/release-tools into ./release-tools-564559-finish-moving-announce.sh-to-releases-repo-by-deleting-it
  git clone git://git.openstack.org/openstack-infra/release-tools release-tools-564559-finish-moving-announce.sh-to-releases-repo-by-deleting-it
  Cloning into 'release-tools-564559-finish-moving-announce.sh-to-releases-repo-by-deleting-it'...
  remote: Counting objects: 2320, done.
  remote: Compressing objects: 100% (995/995), done.
  remote: Total 2320 (delta 1491), reused 2109 (delta 1312)
  Receiving objects: 100% (2320/2320), 2.72 MiB | 1.50 MiB/s, done.
  Resolving deltas: 100% (1491/1491), done.
  Checking connectivity... done.

  Configuring git-review
  git review -s
  Creating a git remote called 'gerrit' that maps to:
     ssh://doug-hellmann@review.openstack.org:29418/openstack-infra/release-tools.git

  Downloading https://review.openstack.org/#/c/564559/
  git review -d 564559
  Downloading refs/changes/59/564559/2 from gerrit
  Switched to branch "review/doug_hellmann/announce-script-fixes"

  Updating all remotes
  git remote update
  Fetching origin
  remote: Counting objects: 1501, done.
  remote: Compressing objects: 100% (659/659), done.
  remote: Total 1501 (delta 842), reused 1501 (delta 842)
  Receiving objects: 100% (1501/1501), 218.28 KiB | 0 bytes/s, done.
  Resolving deltas: 100% (842/842), done.
  From git://git.openstack.org/openstack-infra/release-tools
   * [new ref]         refs/notes/review -> refs/notes/review
  Fetching gerrit

  Patch ready in ./release-tools-564559-finish-moving-announce.sh-to-releases-repo-by-deleting-it

The URL argument can use the /#/c "fragment" form or it can use the
simplified form ``https://review.openstack.org/564559/``.

It can also include a patchset number if the goal is to download a
draft older than the most recent patchset.

::

  $ git nit  https://review.openstack.org/#/c/564559/1/
  release-tools-564559-finish-moving-announce.sh-to-releases-repo-by-deleting-it
  Cloning openstack-infra/release-tools into ./release-tools-564559-finish-moving-announce.sh-to-releases-repo-by-deleting-it
  git clone git://git.openstack.org/openstack-infra/release-tools release-tools-564559-finish-moving-announce.sh-to-releases-repo-by-deleting-it
  Cloning into 'release-tools-564559-finish-moving-announce.sh-to-releases-repo-by-deleting-it'...
  remote: Counting objects: 2320, done.
  remote: Compressing objects: 100% (991/991), done.
  remote: Total 2320 (delta 1494), reused 2111 (delta 1316)
  Receiving objects: 100% (2320/2320), 2.72 MiB | 2.23 MiB/s, done.
  Resolving deltas: 100% (1494/1494), done.
  Checking connectivity... done.

  Configuring git-review
  git review -s
  Creating a git remote called 'gerrit' that maps to:
     ssh://doug-hellmann@review.openstack.org:29418/openstack-infra/release-tools.git

  Downloading https://review.openstack.org/#/c/564559/1/
  git review -d 564559,1
  Downloading refs/changes/59/564559/1 from gerrit
  Switched to branch "review/doug_hellmann/announce-script-fixes-patch1"

  Updating all remotes
  git remote update
  Fetching origin
  remote: Counting objects: 1501, done.
  remote: Compressing objects: 100% (659/659), done.
  remote: Total 1501 (delta 842), reused 1501 (delta 842)
  Receiving objects: 100% (1501/1501), 218.18 KiB | 0 bytes/s, done.
  Resolving deltas: 100% (842/842), done.
  From git://git.openstack.org/openstack-infra/release-tools
   * [new ref]         refs/notes/review -> refs/notes/review
  Fetching gerrit

  Patch ready in ./release-tools-564559-finish-moving-announce.sh-to-releases-repo-by-deleting-it

Use the ``--short-name`` (or ``-s``) option to change the default behavior and
name the output directory after the repository without including the
patchset number and subject.

::

  $ git nit -s  https://review.openstack.org/#/c/564559/1/
  Cloning openstack-infra/release-tools into release-tools
  git clone git://git.openstack.org/openstack-infra/release-tools release-tools
  Cloning into 'release-tools'...
  remote: Counting objects: 2320, done.
  remote: Compressing objects: 100% (989/989), done.
  remote: Total 2320 (delta 1493), reused 2115 (delta 1318)
  Receiving objects: 100% (2320/2320), 2.73 MiB | 2.24 MiB/s, done.
  Resolving deltas: 100% (1493/1493), done.
  Checking connectivity... done.

  Configuring git-review
  git review -s
  Creating a git remote called 'gerrit' that maps to:
     ssh://doug-hellmann@review.openstack.org:29418/openstack-infra/release-tools.git

  Downloading https://review.openstack.org/#/c/564559/1/
  git review -d 564559,1
  Downloading refs/changes/59/564559/1 from gerrit
  Switched to branch "review/doug_hellmann/announce-script-fixes-patch1"

  Updating all remotes
  git remote update
  Fetching origin
  remote: Counting objects: 1501, done.
  remote: Compressing objects: 100% (659/659), done.
  remote: Total 1501 (delta 842), reused 1501 (delta 842)
  Receiving objects: 100% (1501/1501), 218.28 KiB | 0 bytes/s, done.
  Resolving deltas: 100% (842/842), done.
  From git://git.openstack.org/openstack-infra/release-tools
   * [new ref]         refs/notes/review -> refs/notes/review
  Fetching gerrit

  Patch ready in release-tools

After the patch has been downloaded, move into the new directory and
make the relevant changes, then use ``git review`` to post the new
patchset. You can update the existing patch with ``git commit
--amend`` or create a new one as a series.

Resources
=========

* Free software: Apache license
* Source: https://github.com/dhellmann/git-nit
* Bugs: https://github.com/dhellmann/git-nit/issues
