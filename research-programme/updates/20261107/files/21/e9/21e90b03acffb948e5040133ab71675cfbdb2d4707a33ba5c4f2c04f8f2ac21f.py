from common import *
from source_adapter import native_background,other_density
import numpy as np


def main():
    modest()
    check_parent()
    require(read(ROOT/'inventory-01.end.json')['exit_code']==1,'inspect the retained failed inventory only')
    target=read(ROOT/'inventory/cold-target.json')
    destination=ROOT/'density-diagnosis'
    destination.mkdir(exist_ok=False)
    reports=[]
    names=['cdm','baryon','photon','neutrino','nu']
    for model in ('heavy','cold'):
        guard()
        accepted=load(BACKGROUND/'runs'/model/'dop-half-cap.npz')
        native=native_background(model)
        probes=np.linspace(accepted['efold'][0],np.log(target['scale_end']),513)
        central=native.get_background_densities(np.exp(probes),vars=names,format='array')/np.exp(2*probes)[:,None]
        rows=[]
        for width in (.01,.003,.001,.0005,.0001):
            samples=[native.get_background_densities(np.exp(probes+shift*width),vars=names,format='array')/np.exp(2*(probes+shift*width))[:,None] for shift in (-2,-1,1,2)]
            first=(samples[0]-8*samples[1]+8*samples[2]-samples[3])/(12*width)
            second=(-samples[0]+16*samples[1]-30*central+16*samples[2]-samples[3])/(12*width**2)
            ratio=second.sum(axis=1)/central.sum(axis=1)
            bad=np.flatnonzero((ratio<1-GATE)|(ratio>4+GATE))
            rows.append(dict(width=width,total_curvature_range=[float(ratio.min()),float(ratio.max())],outliers=[dict(index=int(index),scale=float(np.exp(probes[index])),total_ratio=float(ratio[index]),component_ratios=(second[index]/central[index]).tolist(),component_fractions=(central[index]/central[index].sum()).tolist()) for index in bad],component_ranges={name:[float((second[:,index]/central[:,index]).min()),float((second[:,index]/central[:,index]).max())] for index,name in enumerate(names)}))
            np.savez_compressed(destination/(model+'-h'+str(width)+'.npz'),efold=probes,density=central,first=first,second=second)
        reports.append(dict(model=model,widths=rows))
        print(model,[(row['width'],row['total_curvature_range'],len(row['outliers'])) for row in rows],flush=True)
        del native,accepted
    check_parent()
    write(destination/'result.json',dict(state='diagnosis_only_no_retry',failed_inventory_preserved=True,new_ode_solves=0,bounds_or_tolerances_changed=False,components=names,reports=reports,source_hashes=frozen_sources()))


if __name__=='__main__':
    main()
