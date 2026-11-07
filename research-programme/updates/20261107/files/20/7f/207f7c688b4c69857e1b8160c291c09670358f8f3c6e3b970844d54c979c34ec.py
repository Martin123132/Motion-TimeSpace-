from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import fitz
import psutil


ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    source = ROOT.parent/'pn-balance-20261004/sources/banihashemi-vines-2020.pdf'
    output = ROOT/'sources'
    output.mkdir(parents=True, exist_ok=False)
    document = fitz.open(source)
    for number in [8, 9]:
        page = document[number-1]
        page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5)).save(output/f'BV-page{number}.png')
        (output/f'BV-page{number}.txt').write_text(page.get_text(), encoding='utf-8')
    report = {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(),
              'script_sha256': digest(__file__), 'path': str(source), 'sha256': digest(source),
              'url': 'https://arxiv.org/pdf/1805.07266', 'doi': '10.1103/PhysRevD.101.064003',
              'title': 'Gravitomagnetic tidal effects in gravitational waves from neutron star binaries',
              'authors': 'Batoul Banihashemi and Justin Vines', 'preprint_year': 2018, 'publication_year': 2020,
              'page_count': len(document), 'pdf_pages_rendered': [8, 9],
              'role': 'Independent leading magnetic action/energy comparison, not a coefficient input to the source-overlap derivation.',
              'output_sha256': {path.name: digest(path) for path in sorted(output.glob('*'))}}
    (output/'provenance.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'source_sha256': report['sha256']}))


if __name__ == '__main__':
    main()
