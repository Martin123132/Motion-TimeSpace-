from __future__ import annotations

import requests
from transport_common import *


def main():
    modest()
    folder=ROOT/'sources'
    folder.mkdir(parents=True,exist_ok=False)
    records=[]
    for name,url in [('transfer-variables.html','https://camb.readthedocs.io/en/latest/transfer_variables.html'),
        ('gauge-conventions.html','https://camb.readthedocs.io/en/latest/variables_guide.html')]:
        response=requests.get(url,timeout=45)
        response.raise_for_status()
        assert b'<html' in response.content.lower() and b'CAMB' in response.content
        path=folder/name;path.write_bytes(response.content)
        records.append(dict(path=str(path),url=url,final_url=response.url,sha256=digest(path),bytes=len(response.content)))
    local=[NATIVE/'fortran/equations.f90',NATIVE/'fortran/camb_python.f90',NATIVE/'camb/symbolic.py']
    finish(folder,dict(records=records,local_authority=[dict(path=str(path),sha256=digest(path)) for path in local],
        scope='Official docs corroborate conventions; the sealed local native source owns exact implemented equations and output precision.'),
        __file__,[Path(record['path']) for record in records])
    print(json.dumps(records,indent=2))


if __name__=='__main__':
    main()
