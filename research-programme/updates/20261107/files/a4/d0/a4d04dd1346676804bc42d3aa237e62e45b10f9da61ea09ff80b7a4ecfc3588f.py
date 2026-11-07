from __future__ import annotations

import urllib.request
from velocity_common import *


def main():
    modest()
    folder=ROOT/'sources'
    folder.mkdir(parents=True,exist_ok=False)
    records=[]
    for name,url in [('Scoccimarro-2004.html','https://arxiv.org/abs/astro-ph/0407214v2'),
            ('Desjacques-Jeong-Schmidt-2019.html','https://arxiv.org/abs/1611.09787v5')]:
        with urllib.request.urlopen(url,timeout=60) as response:
            payload=response.read(2*1024*1024)
            final=response.url
        path=folder/name
        path.write_bytes(payload)
        records.append(dict(path=str(path),url=url,final_url=final,bytes=len(payload),sha256=digest(path)))
    finish(folder,dict(records=records,scope='Primary reference metadata/abstracts; derivation and assumptions written explicitly in this stage.'),
        __file__,[Path(row['path']) for row in records])


if __name__=='__main__':
    main()
