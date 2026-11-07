from finite_matching_common import *


def main():
    modest()
    folder=ROOT/'results/additional-primary-sources'
    folder.mkdir(parents=True,exist_ok=False)
    sources=[
        dict(path=str(ROOT/'sources/2005.06941.pdf'),url='https://arxiv.org/pdf/2005.06941',
             doi='https://doi.org/10.1088/1475-7516/2020/10/025',use='Visually verified AppendixB page29, PDFpage30: two auxiliary-function inconsistencies also present in PDF, not only HTML'),
        dict(path=str(ROOT/'sources/2102.06718v2.html'),url='https://arxiv.org/html/2102.06718v2',
             doi='https://doi.org/10.1103/PhysRevLett.126.211801',use='Independent analytical vacuum total, Equations5-8 and threshold10'),
        dict(path=str(ROOT/'sources/Varma1992.pdf'),url='https://samirvarma.com/assets/pdf/Finite-temperature-radiative-corrections-to-Compton-scattering.pdf',
             doi='https://doi.org/10.1103/PhysRevD.46.3630',use='Primary thermal-loop integrands5.1; do not import the expanded final result outside5.4/5.5')]
    for source in sources:
        source['sha256']=digest(source['path'])
    write_json(ROOT/'sources/additional-provenance.json',dict(sources=sources,
        author_download_discovery='https://samirvarma.com/publications/',
        method='Public direct downloads; PDF visual scope check and HTML mathematical transcription'))
    checks=[dict(name='Acquired and hashed '+Path(source['path']).name,passed=True) for source in sources]
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=True,sources=sources),__file__,[Path(source['path']) for source in sources])
    print(json.dumps(dict(checks=len(checks),failed=[])),flush=True)


if __name__=='__main__':
    main()
