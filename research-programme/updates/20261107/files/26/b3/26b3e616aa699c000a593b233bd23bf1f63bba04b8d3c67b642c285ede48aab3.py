from kinetic_common import *


def main():
    modest()
    folder=ROOT/'results/resolved-source-comparison'
    folder.mkdir(parents=True,exist_ok=False)
    names=['resolved-e2-a2-f4-s12','resolved-e3-a3-f6-s18','resolved-e3-a4-f8-s24','paired-e3-a3-f6-s18']
    reports={name:json.loads((ROOT/'results'/name/'status.json').read_text()) for name in names}
    checks=[]
    for name,report in reports.items():
        assert report['all_checks_passed'],name
    coarse=reports['resolved-e3-a3-f6-s18']
    fine=reports['resolved-e3-a4-f8-s24']
    paired=reports['paired-e3-a3-f6-s18']
    for key in ['matrix','source_scaled']:
        left=np.array(coarse[key])
        right=np.array(fine[key])
        error=float(np.linalg.norm(left-right)/np.linalg.norm(right))
        checks.append(check('Finite-band real '+key+' quadrature refinement',error,.002))
        cross=float(np.linalg.norm(np.array(paired[key])-right)/np.linalg.norm(right))
        checks.append(check('Independent ordered emission versus paired inverse representation '+key,cross,.002))
    theta=json.loads((ROOT/'results/saved-state/status.json').read_text())['reference_temperature']
    with np.load(ROOT/'results/derived-gaunt-bank/gaunt.npz') as saved:
        gaunt=float(interpolate.CubicSpline(np.log(saved['temperatures']),saved['gaunt'])(math.log(theta)))
    leading=16*source.ALPHA/(3*np.pi)*theta**2*gaunt
    chemical_coefficient=-fine['matrix'][0][0]*fine['arguments']['minimum']
    checks.append(check('Finite-band chemical pole agrees with independent population soft integral',abs(chemical_coefficient/leading-1),1e-4))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),
                       soft_population_coefficient=leading,finite_cutoff_chemical_coefficient=chemical_coefficient,
                       source_physical=fine['source_physical'],matrix=fine['matrix'],
                       numerical_scope='Resolved real scalar weak block at the saved midpoint; not the matched full operator.',
                       number_mode_remains_physical=True,finite_virtual_projection_pending=True),__file__,
           [*[ROOT/'results'/name/'status.json' for name in names],ROOT/'results/saved-state/status.json',
            ROOT/'results/derived-gaunt-bank/gaunt.npz'])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],
                          soft=leading,finite_cutoff=chemical_coefficient)),flush=True)


if __name__=='__main__':
    main()
