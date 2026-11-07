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
    source = ROOT.parent/'companion-source-20261004/sources/martel-poisson-2005.pdf'
    output = ROOT/'sources'
    output.mkdir(parents=True, exist_ok=True)
    pages = [6, 7, 9, 16]
    document = fitz.open(source)
    for number in pages:
        page = document[number-1]
        page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5)).save(output/f'martel-poisson-page{number}.png')
        (output/f'martel-poisson-page{number}.txt').write_text(page.get_text(), encoding='utf-8')
    report = {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(),
              'script_sha256': digest(__file__), 'path': str(source), 'sha256': digest(source),
              'url': 'https://arxiv.org/pdf/gr-qc/0502028', 'doi': '10.1103/PhysRevD.71.104003',
              'title': 'Gravitational perturbations of the Schwarzschild spacetime: A practical covariant and gauge-invariant formalism',
              'authors': 'Karl Martel and Eric Poisson', 'year': 2005,
              'acquisition': 'Read-only reuse of sealed stage19 primary PDF; web URL checked during this stage.',
              'pdf_pages_rendered': pages, 'output_sha256': {path.name: digest(path) for path in sorted(output.glob('*'))}}
    (output/'provenance.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'pages': pages, 'source_sha256': report['sha256']}))


if __name__ == '__main__':
    main()
