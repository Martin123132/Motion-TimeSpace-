from __future__ import annotations

import importlib.util
import io
from window_common import *


def main():
    modest()
    folder=ROOT/'results/prepared'
    folder.mkdir(parents=True,exist_ok=False)
    manifest=json.loads((ROOT/'sources/manifest.json').read_text())
    assert manifest['state']=='complete'
    for record in manifest['records']:
        assert digest(ROOT/'sources'/record['local_file'])==record['sha256']
    spec=importlib.util.spec_from_file_location('author_pk_tools',ROOT/'sources/pk_tools.py')
    author=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(author)
    reports=[]
    for cap in ['NGC','SGC']:
        power_path=next((ROOT/'sources').glob('ps1D*'+cap+'*.dat'))
        lines=power_path.read_text().splitlines()
        markers=[index for index,line in enumerate(lines) if line=='### header ###']
        assert len(markers)==2
        raw=np.loadtxt(io.StringIO('\n'.join(lines[markers[1]+1:])))
        assert raw.shape==(400,13) and np.isfinite(raw).all()
        assert np.allclose(raw[:,0],KIN,rtol=0,atol=1e-10)
        counts=raw[:,12].reshape(40,10)
        assert np.all(counts>=0) and np.all(counts.sum(axis=1)>0)
        weighted=lambda value:np.sum(value.reshape(40,10)*counts,axis=1)/counts.sum(axis=1)
        observed=np.concatenate([weighted(raw[:,2+2*ell]) for ell in range(5)])
        effective=weighted(raw[:,1])
        reference=author.read_power(str(power_path),combine_bins=10)
        _,reference_vector=author.dict_to_vec(reference)
        assert np.allclose(observed,reference_vector,rtol=1e-14,atol=1e-9)
        assert np.allclose(effective,reference['k'],rtol=0,atol=1e-14)
        matrix=np.loadtxt(next((ROOT/'sources').glob('M_*'+cap+'*.gz')))
        window=np.loadtxt(next((ROOT/'sources').glob('W_*'+cap+'*.gz')))
        covariance=np.loadtxt(next((ROOT/'sources').glob('C_*'+cap+'*.gz')))
        assert matrix.shape==(2000,1200) and window.shape==(200,2000) and covariance.shape==(200,200)
        assert all(np.isfinite(array).all() for array in [matrix,window,covariance])
        assert np.allclose(covariance,covariance.T,rtol=0,atol=1e-7)
        linalg.cholesky(covariance,lower=True)
        even=np.concatenate([np.arange(400)+ell*400 for ell in [0,2,4]])
        assert np.array_equal(matrix[even],np.eye(1200))
        operator=window@matrix
        np.savez_compressed(folder/(cap+'.npz'),data=observed,covariance=covariance,
            wide_angle=matrix,window=window,operator=operator,k_effective=effective,k_nominal=KOUT,k_theory=KIN,
            mode_count=counts.sum(axis=1))
        reports.append(dict(cap=cap,rows=len(observed),wide_angle_shape=list(matrix.shape),window_shape=list(window.shape),
            covariance_min_eigenvalue=float(min(linalg.eigvalsh(covariance))),mock_count=NMOCK,
            rebin_max_difference=float(max(abs(observed-reference_vector))),
            actual_orientation_differs_from_landing_page_label=True,z_effective_source='Table1: .38, not the unused zeff=0 header'))
    finish(folder,dict(surveys=reports,cross_cap_covariance_policy='Disjoint sky caps treated independently; no extra cross-cap product supplied.'),
        __file__,[ROOT/'sources/manifest.json',*[ROOT/'sources'/row['local_file'] for row in manifest['records']],*folder.glob('*.npz')])
    print(json.dumps(reports,indent=2))


if __name__=='__main__':
    main()
