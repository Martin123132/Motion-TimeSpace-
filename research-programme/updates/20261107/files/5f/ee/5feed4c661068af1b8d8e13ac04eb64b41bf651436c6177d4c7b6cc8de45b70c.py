import urllib.request
from thermal_wave_common import *


def main():
    modest()
    folder = ROOT / 'results/primary-source'
    assert not folder.exists()
    source_folder = ROOT / 'sources'
    source_folder.mkdir(exist_ok=True)
    url = 'https://arxiv.org/html/astro-ph/9506072'
    target = source_folder / 'ma-bertschinger-9506072.html'
    assert not target.exists()
    request = urllib.request.Request(url, headers={'User-Agent': 'MTS-private-research-source-archive/1.0'})
    with urllib.request.urlopen(request, timeout=60) as response:
        payload, final_url = response.read(), response.url
    text = payload.decode('utf-8')
    assert 'Cosmological Perturbation Theory' in text and len(payload) > 10000
    target.write_bytes(payload)
    folder.mkdir(parents=True, exist_ok=False)
    checks = [dict(name='Primary paper archived with identifiable title and nonempty text', passed=True),
              dict(name='Previously archived plasma-cooling primary source retained',
                   passed=(THERMAL / 'sources/khatri-sunyaev-chluba-1110.0475v2.html').is_file())]
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        source_url=url, final_url=final_url, sha256=digest(target), bytes=len(payload),
                        authors='Chung-Pei Ma and Edmund Bertschinger', paper_year=1995,
                        used_scope='Sections4 and5: conservation and standard cold Thomson/baryon limit; not authority for our derived mixed thermal extension.',
                        retrieved_utc=datetime.now(timezone.utc).isoformat()), __file__,
           [target, THERMAL / 'sources/khatri-sunyaev-chluba-1110.0475v2.html'])
    print(json.dumps(dict(source=str(target), bytes=len(payload), sha256=digest(target))), flush=True)


if __name__ == '__main__':
    main()
