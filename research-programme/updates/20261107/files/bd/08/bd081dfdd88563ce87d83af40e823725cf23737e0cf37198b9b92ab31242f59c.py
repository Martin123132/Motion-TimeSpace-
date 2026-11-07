from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import urllib.request

ROOT=Path(__file__).resolve().parent
BASE='https://fbeutler.github.io/hub/'


def main():
    folder=ROOT/'sources'
    folder.mkdir(parents=True,exist_ok=False)
    records=[]

    def fetch(url,name):
        request=urllib.request.Request(url,headers={'User-Agent':'MTS-private-research-source-acquisition/1.0'})
        with urllib.request.urlopen(request,timeout=90) as response:
            payload=response.read(80*1024*1024+1)
            assert len(payload)<=80*1024*1024
            final=response.url
        (folder/name).write_bytes(payload)
        records.append(dict(url=url,final_url=final,local_file=name,bytes=len(payload),
            sha256=hashlib.sha256(payload).hexdigest(),acquired_utc=datetime.now(timezone.utc).isoformat()))
        (folder/'manifest.json').write_text(json.dumps(dict(state='acquiring',records=records),indent=2))
        print(name,len(payload),flush=True)
        return payload

    landing=fetch(BASE+'deconv_paper.html','author-data-page.html').decode()
    links=re.findall(r'href=[\"\x27]([^\"\x27]+)',landing)
    for cap in ['NGC','SGC']:
        names=[f'M_BOSS_DR12_{cap}_z1_V6C_1_1_1_1_1_1200_2000.matrix.gz',
            f'W_BOSS_DR12_{cap}_z1_V6C_1_1_1_1_1_10_200_2000_averaged_v1.matrix.gz',
            f'C_2048_BOSS_DR12_{cap}_z1_V6C_1_1_1_1_1_10_200_200_prerecon.matrix.gz']
        candidates=[link for link in links if f'ps1D_BOSS_DR12_{cap}_z1_' in link and 'post' not in link.lower()]
        assert len(candidates)==1,candidates
        names+=candidates
        for name in names:
            assert name in links,name
            fetch(BASE+name,name)
    commit=json.loads(fetch('https://api.github.com/repos/fbeutler/pk_tools/commits/master','pk-tools-commit.json'))['sha']
    fetch(f'https://raw.githubusercontent.com/fbeutler/pk_tools/{commit}/pk_tools.py','pk_tools.py')
    fetch('https://arxiv.org/pdf/2106.06324v2','Beutler-McDonald-2021.pdf')
    report=dict(state='complete',records=records,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        dataset='BOSS DR12 z1 NGC and SGC pre-reconstruction; Beutler and McDonald 2021 release',
        landing_url=BASE+'deconv_paper.html',pk_tools_commit=commit)
    (folder/'manifest.json').write_text(json.dumps(report,indent=2))
    (folder/'COMPLETE').write_text('complete\n')


if __name__=='__main__':
    main()
