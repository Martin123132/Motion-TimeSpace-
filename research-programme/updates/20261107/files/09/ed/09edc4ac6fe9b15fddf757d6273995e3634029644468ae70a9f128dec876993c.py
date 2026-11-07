from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

import fitz


ROOT = Path(__file__).resolve().parent


def main():
    records = []
    sources = [
        ('blanchet-2006', 'https://www2.iap.fr/users/blanchet/images/lrr-2006-4BW.pdf', [38],
         'Universal GR mass-quadrupole hereditary tail, Eq97; only selected page inspected.'),
        ('banihashemi-vines-2020', 'https://arxiv.org/pdf/1805.07266', [1],
         'Scope check: independent gravitomagnetic body response enters at relative one PN above electric tides.')
    ]
    for name, url, pages, role in sources:
        target = ROOT/'sources'/f'{name}.pdf'
        assert not target.exists()
        with urlopen(url, timeout=60) as response:
            data = response.read()
        assert data.startswith(b'%PDF')
        target.write_bytes(data)
        document = fitz.open(target)
        renders = []
        for page in pages:
            render = ROOT/'sources'/f'{name}-page{page+1}.png'
            document[page].get_pixmap(matrix=fitz.Matrix(1.5, 1.5)).save(render)
            renders.append(str(render))
        records.append({'path': str(target), 'url': url, 'sha256': hashlib.sha256(data).hexdigest(),
                        'page_count': len(document), 'renders': renders, 'role': role})
    output = ROOT/'sources/tail-provenance.json'
    assert not output.exists()
    output.write_text(json.dumps({'state': 'complete',
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'retrieved_utc': datetime.now(timezone.utc).isoformat(), 'sources': records}, indent=2), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'sources': len(records)}))


if __name__ == '__main__':
    main()
