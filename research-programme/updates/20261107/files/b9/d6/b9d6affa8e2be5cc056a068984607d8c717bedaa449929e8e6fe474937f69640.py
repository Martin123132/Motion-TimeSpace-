from __future__ import annotations

import urllib.request

from bridge_common import ROOT, COMMIT, modest_process, digest, save


def main():
    modest_process()
    source_paths = {
        'README.md': 'README.md',
        'formalization-267.md': 'lean/docs/267.md',
        'condensation-introduction.tex': 'preprints/Bose-Einstein-condensation-at-positive-temperature-in-the-dilute-hard-sphere-gas-October-5-2026/build/sections/introduction.tex',
        'condensation-setup.tex': 'preprints/Bose-Einstein-condensation-at-positive-temperature-in-the-dilute-hard-sphere-gas-October-5-2026/build/sections/setup.tex',
    }
    folder = ROOT / 'sources/openai-math'
    folder.mkdir(parents=True, exist_ok=False)
    rows = []
    for name, relative in source_paths.items():
        url = 'https://raw.githubusercontent.com/openai/math/' + COMMIT + '/' + relative
        request = urllib.request.Request(url, headers={'User-Agent': 'MTS-source-read-only'})
        with urllib.request.urlopen(request, timeout=30) as response:
            data = response.read(400000)
            assert response.status == 200 and 0 < len(data) < 400000
        data.decode('utf-8')
        path = folder / name
        with path.open('xb') as handle:
            handle.write(data)
        rows.append(dict(repository_path=relative, local_path=str(path), url=url,
            sha256=digest(path), bytes=len(data), executed=False))
    scope = (folder / 'formalization-267.md').read_text(encoding='utf-8')
    assert 'without a positive-temperature assertion' in scope
    save('sources', __file__, dict(commit=COMMIT, source_rows=rows,
        source_code_executed=False, lean_independently_compiled=False,
        scope='Selected paper assumptions and formalization scope only, not an independent proof audit.',
        additional_primary_urls=['https://arxiv.org/abs/1712.00445', 'https://arxiv.org/abs/1806.01898']),
        [folder / name for name in source_paths])
    print(dict(state='complete', downloaded_files=len(rows), total_bytes=sum(row['bytes'] for row in rows)), flush=True)


if __name__ == '__main__':
    main()
