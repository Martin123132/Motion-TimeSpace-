from emission_angular_common import *


def main():
    modest()
    folder = ROOT / 'results/source-and-angular-refinement'
    folder.mkdir(parents=True, exist_ok=False)
    sources = ROOT / 'sources'
    sources.mkdir(exist_ok=False)
    authorities = [
        dict(path=str(BRANCH / 'scaled-spectral-evolution-20261007/sources/2005.06941v1.html'),
             url='https://arxiv.org/html/2005.06941v1', doi='https://doi.org/10.1088/1475-7516/2020/10/025',
             use='Bose factor, differential Gould kernel, full matrix element and infrared matching discussion.', current_web_read=True),
        dict(path=str(PARENT / 'sources/astro-ph-0611172.html'), url='https://arxiv.org/html/astro-ph/0611172',
             use='Independent historical form of squared DC amplitude and soft-emission normalization.', current_web_read=False),
        dict(path=str(BACKGROUND / 'sources/1109.6552.html'), url='https://arxiv.org/html/1109.6552',
             doi='https://doi.org/10.1111/j.1365-2966.2011.19786.x',
             use='Inherited isotropic source approximation; not a full angular kernel.', current_web_read=False)]
    for charge in ['01', '02']:
        authorities.append(dict(path=str(BACKGROUND / ('sources/gauntff_merged_Z' + charge + '.dat')),
            url='https://data.nublado.org/gauntff/', use='Unchanged tabulated BR Gaunt factor Z=' + charge, current_web_read=False))
    for source in authorities:
        source['sha256'] = digest(source['path'])
    write_json(sources / 'provenance.json', dict(archived_sources_reused_without_edits=True, sources=authorities))
    coarse, fine = ROOT / 'results/full-matrix-marginals', ROOT / 'results/full-matrix-marginals-order10'
    checks, inputs = [], [coarse / 'status.json', fine / 'status.json']
    for path in sorted(fine.glob('sample-*.npz')):
        other = coarse / path.name
        inputs.extend([path, other])
        with np.load(path) as refined, np.load(other) as original:
            error = float(np.max(abs(refined['actual'] - original['actual'])))
        checks.append(check('Full-matrix angular quadrature refinement ' + path.stem, error, 1e-10))
    checks.append(dict(name='All archived primary paths and source hashes recorded', passed=True))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
        source_count=len(authorities), maximum_angular_change=max(row.get('value', 0.) for row in checks)), __file__,
        [*inputs, sources / 'provenance.json', *[Path(source['path']) for source in authorities]])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']],
        maximum=max(row.get('value', 0.) for row in checks))), flush=True)


if __name__ == '__main__':
    main()
