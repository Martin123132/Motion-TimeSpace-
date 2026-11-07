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
    output.mkdir(exist_ok=False)
    records = []
    for stem, identifier, pages, purpose in [
        ('vines-flanagan-hinderer-2011', '1101.1673', [3, 5], 'Independent leading tidal energy, flux and phase; test-mass first-PN conservative energy coefficient.'),
        ('fujita-et-al-2017', '1612.02504', [1, 2], 'Conservative half-retarded plus half-advanced prescription and mass-ratio-order cautions; not a full-paper audit.')]:
        url = 'https://arxiv.org/pdf/'+identifier
        with urlopen(url, timeout=45) as response:
            data = response.read()
        assert data.startswith(b'%PDF')
        path = output/(stem+'.pdf')
        path.write_bytes(data)
        document = fitz.open(path)
        renders = []
        for page in pages:
            target = output/(stem+f'-page{page+1}.png')
            document[page].get_pixmap(matrix=fitz.Matrix(1.5, 1.5)).save(target)
            renders.append(str(target))
        records.append({'url': url, 'abstract_url': 'https://arxiv.org/abs/'+identifier, 'path': str(path),
                        'sha256': hashlib.sha256(data).hexdigest(), 'page_count': len(document),
                        'selected_page_renders': renders, 'purpose': purpose})
    report = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'retrieved_utc': datetime.now(timezone.utc).isoformat(), 'sources': records,
              'distribution': 'Private reference copies only; no GitHub/publication action.'}
    (output/'provenance.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'sources': len(records)}))


if __name__ == '__main__':
    main()
