from urllib.request import Request, urlopen
from step_common import *


def main():
    modest()
    folder = ROOT / 'results/source-acquisition'
    assert not folder.exists()
    sources = ROOT / 'sources'
    sources.mkdir(exist_ok=False)
    url = 'https://arxiv.org/html/astro-ph/9910280v3'
    request = Request(url, headers={'User-Agent': 'MTS-research-source-archive/1.0'})
    with urlopen(request, timeout=45) as response:
        content = response.read()
        final_url = response.url
    path = sources / 'sazonov-sunyaev-9910280v3.html'
    with path.open('xb') as stream:
        stream.write(content)
    checks = [dict(name='Primary HTML contains paper identity and physical kernel section',
                   passed=b'9910280' in content and b'Klein' in content and b'<html' in content.lower())]
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        source_url=url, final_url=final_url, source_sha256=digest(path),
                        doi='10.1086/317078', publication_year=2000,
                        sections_consulted=['1.1', '1.2', '2.1 detailed balance', '3 equations52-59'],
                        experimental_HTML_not_visually_verified_against_PDF=True,
                        unpolarized_physical_law_reference_not_new_MTS_evidence=True), __file__, [path])
    print(json.dumps(dict(archived=str(path), checks=checks)), flush=True)


if __name__ == '__main__':
    main()
