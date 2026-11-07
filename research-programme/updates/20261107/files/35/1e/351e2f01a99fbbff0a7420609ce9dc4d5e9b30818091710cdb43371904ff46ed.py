import urllib.request
from thermal_vertex_common import *


def main():
    modest()
    folder=ROOT/'results/source-registration'
    folder.mkdir(parents=True,exist_ok=False)
    url='https://dlmf.nist.gov/5.9'
    target=ROOT/'sources/DLMF-5.9.html'
    request=urllib.request.Request(url,headers={'User-Agent':'MTS-private-research-source-check/1.0'})
    with urllib.request.urlopen(request,timeout=60) as response:
        target.write_bytes(response.read())
    assert '5.9.15' in target.read_text(encoding='utf-8')
    sources=[dict(url=url+'#E15',path=str(target),sha256=digest(target),role='Binet identity; boundary-value continuation derived here'),
             dict(url='https://samirvarma.com/assets/pdf/Finite-temperature-radiative-corrections-to-Compton-scattering.pdf',
                  doi='https://doi.org/10.1103/PhysRevD.46.3630',path=str(PARENT/'sources/Varma1992.pdf'),
                  sha256=digest(PARENT/'sources/Varma1992.pdf'),role='Original finite-temperature diagram organization and mass benchmark')]
    write_json(ROOT/'sources/provenance.json',dict(sources=sources,retrieved_utc=datetime.now(timezone.utc).isoformat(),
                                                 previous_author_listing='https://samirvarma.com/publications/'))
    checks=[dict(name='Primary Binet identity archived without modifying prior PDF',passed=True)]
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=True,sources=sources),__file__,
           [target,ROOT/'sources/provenance.json',PARENT/'sources/Varma1992.pdf'])
    print(json.dumps(dict(checks=1,source_bytes=target.stat().st_size)),flush=True)


if __name__=='__main__':
    main()
