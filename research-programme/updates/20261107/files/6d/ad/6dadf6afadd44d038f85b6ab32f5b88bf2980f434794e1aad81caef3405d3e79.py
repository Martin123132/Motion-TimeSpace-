from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

import fitz


ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent/'orbital-backreaction-20261004'


def main():
    output = ROOT/'sources'
    output.mkdir(parents=True, exist_ok=False)
    records = []
    path = PARENT/'sources/vines-flanagan-hinderer-2011.pdf'
    document = fitz.open(path)
    renders = []
    for page in [2, 4]:
        target = output/f'vines-flanagan-hinderer-2011-page{page+1}.png'
        document[page].get_pixmap(matrix=fitz.Matrix(1.7, 1.7)).save(target)
        renders.append(str(target))
    records.append({'path': str(path), 'url': 'https://arxiv.org/pdf/1101.1673',
                    'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'page_count': len(document), 'renders': renders,
                    'role': 'Retained GR 1PN matching input, uncontracted multipoles/action; final circular formulas are same-source algebra checks, not independent evidence.'})
    url = 'https://arxiv.org/pdf/1009.4919'
    with urlopen(url, timeout=60) as response:
        data = response.read()
    assert data.startswith(b'%PDF')
    path = output/'vines-flanagan-2013.pdf'
    path.write_bytes(data)
    document = fitz.open(path)
    records.append({'path': str(path), 'url': url, 'sha256': hashlib.sha256(data).hexdigest(),
                    'page_count': len(document), 'role': 'Underlying stress/multipole action and spin consistency reference; selected sections only, not a full proof audit.'})
    report = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'retrieved_utc': datetime.now(timezone.utc).isoformat(), 'sources': records,
              'scope': 'Private source copies and selected-page renders only.'}
    (output/'provenance.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'sources': len(records)}))


if __name__ == '__main__':
    main()
