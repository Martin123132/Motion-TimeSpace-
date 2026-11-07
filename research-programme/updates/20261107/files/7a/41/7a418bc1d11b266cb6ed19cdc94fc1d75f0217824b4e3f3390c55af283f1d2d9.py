from __future__ import annotations

import io
import urllib.request

from radiation_common import *


def fetch(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'MTS-private-source-verification'})
    with urllib.request.urlopen(request, timeout=40) as response:
        assert response.status == 200
        return response.read()


def main():
    modest_process()
    folder = ROOT / 'sources/desi-dr2'
    folder.mkdir(parents=True, exist_ok=False)
    commit_url = 'https://api.github.com/repos/CobayaSampler/bao_data/commits/master'
    commit = json.loads(fetch(commit_url))['sha']
    assert len(commit) == 40
    rows = []
    for original in [BAO_MEAN, BAO_COV]:
        url = 'https://raw.githubusercontent.com/CobayaSampler/bao_data/' + commit + '/desi_bao_dr2/' + original.name
        raw = fetch(url)
        path = folder / original.name
        with path.open('xb') as handle:
            handle.write(raw)
        if original == BAO_MEAN:
            remote = np.loadtxt(io.StringIO(raw.decode('utf-8')), dtype=str)
            local = np.loadtxt(original, dtype=str)
            equal = np.array_equal(remote, local)
        else:
            equal = np.array_equal(np.loadtxt(io.BytesIO(raw)), np.loadtxt(original))
        assert equal, original
        rows.append(dict(url=url, local_snapshot=str(path), snapshot_sha256=digest(path),
            inherited_file=str(original), inherited_sha256=digest(original), values_identical=equal))
    save('sources', __file__, dict(commit=commit, commit_lookup_url=commit_url,
        data_rows=rows, all_inherited_values_verified=True, inherited_data_modified=False),
        [Path(row['local_snapshot']) for row in rows])
    print(dict(state='complete', identical_files=len(rows), commit=commit), flush=True)


if __name__ == '__main__':
    main()

