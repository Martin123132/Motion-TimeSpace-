from __future__ import annotations

import csv
import shutil
from spectrum_common import *


def main():
    modest()
    folder=ROOT/'sources/sdss-growth'
    folder.mkdir(parents=True,exist_ok=False)
    origin=POST.parent/'formalization-workbench/data/cosmology/growth_CMB'
    manifest=origin/'source_manifest.csv'
    with manifest.open(encoding='utf-8-sig',newline='') as handle:
        rows=list(csv.DictReader(handle))
    names=['README.txt']+[f'sdss_{sample}_FS_DMDHfs8{suffix}.txt'
        for sample in ['DR12_LRG','DR16_LRG','DR16_QSO'] for suffix in ['','_covtot']]
    selected=[row for row in rows if '/Full-shape-only/' in row['remote_url'] and row['item_id'] in names]
    assert len(selected)==7
    for row in selected:
        source=Path(row['local_path'])
        assert source.is_file() and digest(source)==row['sha256']
        shutil.copyfile(source,folder/row['item_id'])
    vectors=[]; blocks=[]; redshifts=[]; full_checks=[]
    for sample in ['DR12_LRG','DR16_LRG','DR16_QSO']:
        path=folder/f'sdss_{sample}_FS_DMDHfs8.txt'
        entries=[line.split() for line in path.read_text().splitlines() if line.strip() and not line.startswith('#')]
        mean=np.array([float(row[1]) for row in entries])
        covariance=np.loadtxt(folder/f'sdss_{sample}_FS_DMDHfs8_covtot.txt')
        assert covariance.shape==(len(mean),len(mean))
        assert np.allclose(covariance,covariance.T,rtol=0,atol=1e-12)
        eigenvalues=np.linalg.eigvalsh(covariance)
        assert min(eigenvalues)>0
        indices=[index for index,row in enumerate(entries) if row[2]=='f_sigma8']
        block=covariance[np.ix_(indices,indices)]
        vectors.extend(mean[indices]);redshifts.extend(float(entries[index][0]) for index in indices)
        blocks.append(block)
        full_checks.append(dict(sample=sample,full_shape=list(covariance.shape),minimum_eigenvalue=float(min(eigenvalues)),
            selected_indices=indices,marginal_covariance=block.tolist()))
    covariance=linalg.block_diag(*blocks)
    assert np.allclose(redshifts,[.38,.51,.698,1.48])
    np.savez_compressed(folder/'growth-only.npz',redshifts=redshifts,mean=vectors,covariance=covariance)
    finish(folder,dict(source_records=selected,full_covariance_checks=full_checks,redshifts=redshifts,
        mean=list(vectors),standard_deviations=np.sqrt(np.diag(covariance)).tolist(),
        official_landing_page='https://www.sdss4.org/science/final-bao-and-rsd-measurements/',
        landing_page_checked_utc='2026-10-07',file_web_fetch='Browser retrieval of SVN README/vector failed; existing2026-05-28 source archive verified against saved manifest hashes.',
        no_fresh_download_claim=True,covariance_operation='Marginal growth covariance: covariance submatrix, not precision submatrix.',
        excluded=['Superseded high-redshift DR12 bin','Duplicate legacy LRG alias','Non-Gaussian ELG grid','MGS not in selected full-shape-only set'],
        fit_status='Fixed-parameter conditional screening only; not a model-independent RSD likelihood validation.'),
        __file__,[manifest,*[Path(row['local_path']) for row in selected],*folder.glob('*.txt'),folder/'growth-only.npz'])
    print(json.dumps(dict(z=redshifts,values=vectors,error=np.sqrt(np.diag(covariance)).tolist()),indent=2))


if __name__=='__main__':
    main()
