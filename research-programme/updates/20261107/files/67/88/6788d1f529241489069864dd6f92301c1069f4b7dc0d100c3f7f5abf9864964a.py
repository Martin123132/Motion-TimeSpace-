from __future__ import annotations

import requests
import fitz
from pypdf import PdfReader
from streaming_common import *


def main():
    modest()
    folder=ROOT/'sources'
    folder.mkdir(parents=True,exist_ok=True)
    assert not (folder/'COMPLETE').exists()
    records=[]
    for name,url in [('Scoccimarro-2004-v2.pdf','https://arxiv.org/pdf/astro-ph/0407214v2'),
        ('Reid-White-2011.html','https://arxiv.org/abs/1105.4165')]:
        response=requests.get(url,timeout=60)
        response.raise_for_status()
        path=folder/name
        if path.exists():
            assert path.read_bytes()==response.content,'Existing source changed; preserve and investigate'
        else:
            path.write_bytes(response.content)
        record=dict(path=str(path),url=url,final_url=response.url,sha256=digest(path),bytes=len(response.content))
        if name.endswith('.pdf'):
            assert response.content.startswith(b'%PDF')
            reader=PdfReader(path)
            assert len(reader.pages)==25
            record['pages']=25
            document=fitz.open(path)
            for page_number in [8,10]:
                document[page_number].get_pixmap(matrix=fitz.Matrix(1.2,1.2)).save(folder/f'Scoccimarro-page-{page_number+1}.png')
        else:
            assert b'<html' in response.content.lower() and b'Reid' in response.content
        records.append(record)
    finish(folder,dict(records=records,prior_acquisition_failure='Publisher HTML HTTP403; arXiv primary preprint metadata used instead, existing PDF preserved.',
        scope='Established Gaussian streaming identity checked against Scoccimarro Eq32/44/45; no MTS validation inferred from literature.'),
        __file__,[Path(record['path']) for record in records])
    print(json.dumps(records,indent=2))


if __name__=='__main__':
    main()
