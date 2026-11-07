from finite_matching_common import *
import fitz
import hashlib


def main():
    modest()
    folder = ROOT / 'results/source-acquisition'
    assert not (folder / 'COMPLETE').exists()
    folder.mkdir(parents=True, exist_ok=True)
    source = ROOT / 'sources/BROpr52.pdf'
    assert hashlib.md5(source.read_bytes()).hexdigest() == '526fbf5ac8ab424750e0ba97d790fcba'
    document = fitz.open(source)
    for index, page in enumerate(document):
        (ROOT / 'sources' / ('brown-page-' + str(index + 1) + '.txt')).write_text(page.get_text(), encoding='utf-8')
    record = dict(url='https://authors.library.caltech.edu/records/hpgb4-8p134/files/BROpr52.pdf?download=1',
        landing='https://authors.library.caltech.edu/records/hpgb4-8p134',
        doi='https://doi.org/10.1103/PhysRev.85.231', path=str(source), sha256=digest(source),
        acquisition='Direct institutional download with cache-busting query after web-tool expired redirect',
        md5_matches_institution=True, pages=len(document))
    write_json(ROOT / 'sources/provenance.json', dict(sources=[record]))
    checks = [dict(name='Institutional PDF MD5 matches published file', passed=True)]
    finish(folder, dict(checks=checks, count=1, all_checks_passed=True, source=record), __file__, [source])
    print(json.dumps(record), flush=True)


if __name__ == '__main__':
    main()
