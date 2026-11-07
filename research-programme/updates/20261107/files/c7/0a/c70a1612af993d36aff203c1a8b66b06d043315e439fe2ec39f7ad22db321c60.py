import urllib.request
from soft_matching_common import *


def main():
    modest()
    folder = ROOT / 'sources'
    folder.mkdir(parents=True, exist_ok=False)
    entries = [
        ('hep-ph-9308249.html', 'https://arxiv.org/html/hep-ph/9308249', 'Weldon1993: thermal real/virtual cancellation and current coefficient.'),
        ('hep-ph-9507341.html', 'https://arxiv.org/html/hep-ph/9507341', 'Gupta et al1995: covariant four-momentum generating functional, its hard-scale domain retained.'),
        ('2203.05252v1.html', 'https://arxiv.org/html/2203.05252v1', 'Gamma=0 six-diagram topology only; no phenomenological finite-width prescription adopted.')]
    rows = []
    for name, url, use in entries:
        request = urllib.request.Request(url, headers={'User-Agent': 'MTS-private-research/1.0'})
        with urllib.request.urlopen(request, timeout=60) as response:
            content = response.read()
        assert b'<html' in content.lower() and len(content) > 10000
        path = folder / name
        path.write_bytes(content)
        rows.append(dict(path=str(path), url=url, sha256=digest(path), bytes=len(content), use=use))
    write_json(folder / 'provenance.json', dict(sources=rows, retrieved_utc=datetime.now(timezone.utc).isoformat()))
    result = ROOT / 'results/source-acquisition'
    result.mkdir(parents=True, exist_ok=False)
    checks = [dict(name='Archived primary source ' + row['url'], passed=True) for row in rows]
    finish(result, dict(checks=checks, count=len(checks), all_checks_passed=True), __file__,
        [folder / 'provenance.json', *[Path(row['path']) for row in rows]])
    print(json.dumps(dict(sources=len(rows))), flush=True)


if __name__ == '__main__':
    main()
