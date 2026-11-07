from urllib.request import Request, urlopen
from kernel_common import *


def main():
    modest()
    folder = ROOT / 'results/source-acquisition'
    assert not folder.exists()
    source_folder = ROOT / 'sources'
    source_folder.mkdir(exist_ok=False)
    url = 'https://geant4.web.cern.ch/documentation/dev/prm_html/PhysicsReferenceManual/electromagnetic/polarized_incident/livermore_polarizedcompton.html'
    with urlopen(Request(url, headers={'User-Agent': 'MTS-source-archive/1.0'}), timeout=45) as response:
        content, final_url = response.read(), response.url
    path = source_folder / 'geant4-polarized-compton.html'
    with path.open('xb') as stream:
        stream.write(content)
    checks = [dict(name='Official polarized cross-section reference archived',
                   passed=b'Klein' in content and b'<html' in content.lower() and b'polarized' in content.lower())]
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        source_url=url, final_url=final_url, document_revision='Geant4 11.4',
                        read_scope='Cross Section second angular formula; not outgoing-vector sampling algorithm',
                        amplitude_and_reciprocity_derived_locally_not_copied_from_this_page=True), __file__, [path])
    print(json.dumps(dict(checks=checks)), flush=True)


if __name__ == '__main__':
    main()
