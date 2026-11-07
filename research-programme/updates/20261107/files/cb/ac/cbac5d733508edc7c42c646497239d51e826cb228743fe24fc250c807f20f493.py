import urllib.request
from observer_common import *


def main():
    modest()
    folder = ROOT / 'results/primary-sources'
    folder.mkdir(parents=True, exist_ok=False)
    sources = ROOT / 'sources'
    sources.mkdir(exist_ok=False)
    rows = []
    for identifier, year, title in [
        ('1304.6929', 2013, 'Second order Boltzmann equation: gauge dependence and gauge invariance'),
        ('2602.14963v1', 2026, 'Improved frequency hierarchy treatment for anisotropic spectral distortions')]:
        url = 'https://arxiv.org/html/' + identifier
        path = sources / (identifier + '.html')
        with urllib.request.urlopen(url, timeout=60) as response:
            payload = response.read()
        assert b'<html' in payload[:1000].lower()
        path.write_bytes(payload)
        rows.append(dict(source_url=url, title=title, paper_year=year, path=str(path), sha256=digest(path)))
    checks = [dict(name='Both primary texts archived with source URL and publication year', passed=len(rows) == 2)]
    finish(folder, dict(checks=checks, all_checks_passed=True, count=1, sources=rows), __file__,
           [Path(row['path']) for row in rows])
    print(json.dumps(rows), flush=True)


if __name__ == '__main__':
    main()
