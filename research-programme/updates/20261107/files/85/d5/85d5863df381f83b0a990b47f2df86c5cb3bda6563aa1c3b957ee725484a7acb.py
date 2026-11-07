import urllib.request
from wave_common import *


def main():
    modest()
    folder = ROOT / 'sources'
    folder.mkdir(exist_ok=False)
    url = 'https://arxiv.org/html/astro-ph/0611172'
    request = urllib.request.Request(url, headers={'User-Agent': 'MTS-local-research/1.0'})
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read()
    path = folder / 'astro-ph-0611172.html'
    path.write_bytes(data)
    assert b'Chluba' in data and b'stimulated' in data
    write_json(folder / 'provenance.json', dict(url=url, retrieved_utc=datetime.now(timezone.utc).isoformat(),
        path=str(path), sha256=digest(path), title='The double Compton emissivity in a mildly relativistic thermal plasma within the soft photon limit',
        arxiv='astro-ph/0611172v2', year=2007,
        use='Check the source assumptions of spectrum and electron-temperature derivatives; not permission to treat soft isotropic approximations as a general anisotropic collision kernel.'))
    print(json.dumps(dict(bytes=len(data), sha256=digest(path))), flush=True)


if __name__ == '__main__':
    main()
