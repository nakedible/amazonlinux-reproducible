# amazonlinux-reproducible

Official Amazon Linux 2 docker images modified to use a repository snapshot for reproducible builds.

## Problem Description

Amazon provides [Official Docker
images](https://hub.docker.com/_/amazonlinux/) for Amazon Linux and
Amazon Linux 2. These images are periodically updated to contain new
packages. However, these images are also updateable, and installing
new packages always installs the latest version of the new package.
This means that even if a Dockerfile references an Amazon Linux 2
image directly by hash:

```
FROM amazonlinux@sha256:95a67046bfeb9fe216d8d48c72db25dd7dc83946ad3b5e57b58496b365441883

RUN yum install less
```

The resulting image will be different if `less` package or its
dependencies have been updated in Amazon Linux repository. This means
that builds utilizing Amazon Linux 2 docker images are not even
loosely reproducible, as they will contain different package versions
on each build.

Luckily, Amazon Linux 2 does provide consistent repository snapshots
that are never modified, even though it does not expose them in an
easy manner. The normal repository URL is in the form of a "mirror
list", which points to a repository snapshot that is not never
modified. Updates happen by changing the URL the mirror list points
to.

Example:

```
Repo-mirrors : http://amazonlinux.default.amazonaws.com/2/core/latest/x86_64/mirror.list
Repo-baseurl : https://cdn.amazonlinux.com/2/core/2.0/x86_64/2d910f9668bcc26ef64a1074915497be9c6fb84984538f74c2b293ca355235f7/
Repo-expire  : 300 second(s) (last: Mon Dec  2 13:57:18 2019)
```

Here `Repo-mirrors` is the stable URL for fetching the latest
repository URL and `Repo-baseurl` is the fetched repository snapshot
that is currently used. In normal installations, `Repo-expiry` is set
to 5 minutes, so that `yum` will re-check the repository snapshot that
often.

If we would be able to keep the `Repo-baseurl` used the same all the
time, we would always use the same repository snapshot and always
install the same versions of packages. This also means that running
`yum update` would always result in installing the same packages, and
not actually install anything newer.

## Solution

The solution is to create derived images from the official Amazon
Linux 2 docker images that modify the `yum` configuration to replace
the `mirrorlist` for each repository with a resolved `baseurl`
directly. This is exactly what is done in this repository.

Since Amazon does not release new images every time there is an update
to the repository, we need to build new images periodically to get
images with updated packages.

