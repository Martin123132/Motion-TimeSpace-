from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import urllib.request

import fitz
import psutil


ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'sources'
    output.mkdir(parents=True, exist_ok=False)
    url = 'https://www2.iap.fr/users/blanchet/images/0004-637X_635_1_508.pdf'
    request = urllib.request.Request(url, headers={'User-Agent': 'MTS-private-research-source-check/1.0'})
    with urllib.request.urlopen(request, timeout=45) as response:
        payload = response.read()
    assert payload.startswith(b'%PDF')
    path = output/'blanchet-qusailah-will-2005.pdf'
    path.write_bytes(payload)
    document = fitz.open(path)
    pages = [3]
    for number in pages:
        page = document[number-1]
        page.get_pixmap(matrix=fitz.Matrix(1.7, 1.7)).save(output/f'current-tail-page{number}.png')
        (output/f'current-tail-page{number}.txt').write_text(page.get_text(), encoding='utf-8')
    report = {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(),
              'script_sha256': digest(__file__), 'path': str(path), 'sha256': digest(path),
              'url': url, 'title': 'Gravitational Recoil of Inspiraling Black Hole Binaries to Second Post-Newtonian Order',
              'authors': 'Luc Blanchet, Mohd S. S. Qusailah, Clifford M. Will', 'year': 2005,
              'page_count': len(document), 'pdf_pages_rendered': pages,
              'role': 'Retained GR current-quadrupole hereditary kernel; not a condensate-derived gravity law.',
              'output_sha256': {item.name: digest(item) for item in sorted(output.glob('*'))}}
    (output/'provenance.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'pages': len(document), 'sha256': report['sha256']}))


if __name__ == '__main__':
    main()
