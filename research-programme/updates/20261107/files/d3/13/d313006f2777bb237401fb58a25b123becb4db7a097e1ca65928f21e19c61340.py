from __future__ import annotations

import hashlib
import json
from pathlib import Path
import urllib.request

import fitz
import psutil


ROOT = Path(__file__).resolve().parent


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'sources'
    output.mkdir(exist_ok=False)
    rows = []
    for name, url, pages in [('martel-poisson-2005', 'https://arxiv.org/pdf/gr-qc/0502028', [4, 5, 8]),
                              ('martel-2004', 'https://arxiv.org/pdf/gr-qc/0311017', [15, 16])]:
        request = urllib.request.Request(url, headers={'User-Agent': 'MTS-private-research/1.0'})
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = response.read()
        assert payload.startswith(b'%PDF')
        path = output/(name+'.pdf')
        path.write_bytes(payload)
        document = fitz.open(path)
        for page in pages:
            document[page].get_pixmap(matrix=fitz.Matrix(1.7, 1.7)).save(output/f'{name}-page{page+1}.png')
        rows.append({'path': str(path), 'url': url, 'sha256': hashlib.sha256(payload).hexdigest(),
                     'pages': len(document), 'rendered_pages_one_based': [page+1 for page in pages]})
    report = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'retrieved_utc_date': '2026-10-04', 'sources': rows}
    (output/'provenance.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
