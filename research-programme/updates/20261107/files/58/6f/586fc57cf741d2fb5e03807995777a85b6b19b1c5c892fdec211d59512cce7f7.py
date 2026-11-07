from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import urllib.request

import fitz


ROOT = Path(__file__).resolve().parent
DESTINATION = ROOT/'sources'
DESTINATION.mkdir(exist_ok=True)
url = 'https://arxiv.org/pdf/1307.4812'
pdf_path = DESTINATION/'macedo-pani-cardoso-crispino-2013.pdf'
if not pdf_path.exists():
    request = urllib.request.Request(url, headers={'User-Agent': 'MTS-local-research-source-check/1.0'})
    with urllib.request.urlopen(request, timeout=90) as response:
        data = response.read()
    assert data.startswith(b'%PDF')
    pdf_path.write_bytes(data)
document = fitz.open(pdf_path)
renders = []
for page_number in [3]:
    target = DESTINATION/f'macedo-2013-page{page_number+1}.png'
    document[page_number].get_pixmap(matrix=fitz.Matrix(1.6, 1.6)).save(target)
    renders.append(str(target))
report = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'retrieved_utc': datetime.now(timezone.utc).isoformat(), 'path': str(pdf_path),
          'sha256': hashlib.sha256(pdf_path.read_bytes()).hexdigest(), 'url': url,
          'landing_url': 'https://arxiv.org/abs/1307.4812', 'doi': '10.1103/PhysRevD.88.064046',
          'role': 'Same-theory literature cross-check for the independently expanded axial Einstein equations, Eqs24-27.',
          'selected_page_renders': renders}
with (DESTINATION/'provenance.json').open('x', encoding='utf-8') as handle:
    json.dump(report, handle, indent=2)
print(json.dumps({'state': 'complete', 'pages': len(document), 'sha256': report['sha256']}))
