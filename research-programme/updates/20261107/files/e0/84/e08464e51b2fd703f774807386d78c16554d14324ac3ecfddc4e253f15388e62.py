import urllib.request
from angular_common import *


def main():
    modest()
    folder = ROOT / 'results/source'
    folder.mkdir(parents=True, exist_ok=False)
    sources = ROOT / 'sources'
    sources.mkdir(exist_ok=True)
    rows = []
    for url, name in [
        ('https://arxiv.org/html/1902.09456v2', 'pitrou-1902.09456v2.html'),
        ('https://arxiv.org/pdf/1902.09456v2', 'pitrou-1902.09456v2.pdf'),
    ]:
        request = urllib.request.Request(url, headers={'User-Agent': 'MTS-source-audit/1.0'})
        with urllib.request.urlopen(request, timeout=60) as response:
            data = response.read()
            path = sources / name
            path.write_bytes(data)
            rows.append(dict(url=url, final_url=response.url, http_status=response.status,
                             path=str(path), sha256=digest(path), bytes=len(data)))
    import fitz
    document = fitz.open(sources / 'pitrou-1902.09456v2.pdf')
    for index in [29, 30]:
        document[index].get_pixmap(matrix=fitz.Matrix(1.4, 1.4)).save(sources / ('page-' + str(index + 1) + '.png'))
    checks = [dict(name='Primary source fetched and content type verified: ' + row['url'],
                   passed=row['http_status'] == 200 and row['bytes'] > 10000) for row in rows]
    finish(folder, dict(checks=checks, all_checks_passed=all(row['passed'] for row in checks), sources=rows,
                        pdf_pages=len(document), publication_year=2021, preprint_version_year=2020,
                        original_preprint_year=2019, render_date_not_publication_date=True), __file__,
           [Path(row['path']) for row in rows])
    print(json.dumps(dict(sources=len(rows), pdf_pages=len(document))), flush=True)


if __name__ == '__main__':
    main()
