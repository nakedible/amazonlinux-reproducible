#!/usr/bin/python

import yum, re, os
yb = yum.YumBase()
for name, repo in yb.repos.repos.iteritems():
    if not repo.mirrorlist: continue
    with open(repo.repofile, 'r+') as f:
        data = f.read()
        data = re.sub(r'(\[{}\].*?)^mirrorlist=.*?$'.format(name), r'\1baseurl={}'.format(" ".join(repo.urls)), data, flags=re.MULTILINE|re.DOTALL)
        f.seek(0)
        f.write(data)
        f.truncate()
