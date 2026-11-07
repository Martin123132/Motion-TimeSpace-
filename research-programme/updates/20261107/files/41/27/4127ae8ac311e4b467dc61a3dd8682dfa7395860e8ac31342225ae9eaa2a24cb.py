from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parent


def main():
    output = ROOT/'sources'
    output.mkdir(parents=True, exist_ok=False)
    records = []
    for relative, url, pages in [
        ('pn-balance-20261004/sources/banihashemi-vines-2020.pdf', 'https://arxiv.org/pdf/1805.07266', [8, 9]),
        ('orbital-backreaction-20261004/sources/vines-flanagan-hinderer-2011.pdf', 'https://arxiv.org/pdf/1101.1673', [])
    ]:
        source = ROOT.parent/relative
        document = fitz.open(source)
        renders = []
        for page in pages:
            path = output/f'{source.stem}-page{page+1}.png'
            document[page].get_pixmap(matrix=fitz.Matrix(1.6, 1.6)).save(path)
            renders.append(str(path))
        records.append({'path': str(source), 'sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                        'url': url, 'selected_page_renders': renders, 'role': 'Retained GR source/multipole matching, not a fitted body coefficient.'})
    report = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'retrieved_utc': datetime.now(timezone.utc).isoformat(), 'sources': records}
    (output/'provenance.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'sources': len(records)}))


if __name__ == '__main__':
    main()
