from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

import fitz


ROOT = Path(__file__).resolve().parent


def main():
    output = ROOT/'sources'
    output.mkdir(parents=True, exist_ok=False)
    rows = []
    for name, url, pages in [
        ('cardoso-et-al-2017', 'https://arxiv.org/pdf/1701.01116', [3, 19, 21]),
        ('landry-poisson-2015', 'https://arxiv.org/pdf/1504.06606', [6]),
    ]:
        with urlopen(url, timeout=60) as response:
            data = response.read()
        assert data.startswith(b'%PDF')
        path = output/f'{name}.pdf'
        path.write_bytes(data)
        document = fitz.open(path)
        renders = []
        for page in pages:
            target = output/f'{name}-page{page+1}.png'
            document[page].get_pixmap(matrix=fitz.Matrix(1.6, 1.6)).save(target)
            renders.append(str(target))
        rows.append({'path': str(path), 'url': url, 'sha256': hashlib.sha256(data).hexdigest(),
                     'page_count': len(document), 'selected_page_renders': renders})
    source = ROOT.parent/'pn-balance-20261004/sources/banihashemi-vines-2020.pdf'
    rows.append({'path': str(source), 'url': 'https://arxiv.org/pdf/1805.07266',
                 'sha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'role': 'Current and magnetic-tide convention reference, not a new body coefficient.'})
    output.joinpath('provenance.json').write_text(json.dumps({
        'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'retrieved_utc': datetime.now(timezone.utc).isoformat(), 'sources': rows,
        'scope': 'Selected equations/pages inspected, not whole-paper proof audits.'}, indent=2), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'sources': len(rows)}))


if __name__ == '__main__':
    main()
