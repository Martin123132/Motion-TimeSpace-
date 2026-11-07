from __future__ import annotations

from matching_common import *
from analyze_matching import matter


def main():
    modest()
    folder=ROOT/'results/trajectory-stability'
    folder.mkdir(parents=True,exist_ok=False)
    source,reference=matter(ROOT/'runs/late-225')
    selected=source['requested_scale']>=.001
    reference=reference[:,selected]
    rows=[]
    labels=['late-200','late-250','late-225-bg4','late-225-window4','late-225-degree6']
    for label in labels:
        data,actual=matter(ROOT/'runs'/label)
        chosen=data['requested_scale']>=.001
        assert np.array_equal(data['requested_scale'][chosen],source['requested_scale'][selected])
        difference=abs(actual[:,chosen]/reference-1)
        bound=.005 if label in ['late-200','late-250'] else 5e-4
        rows.append(dict(label=label,maximum_late_amplitude_change=float(np.max(difference)),
            per_mode=np.max(difference,axis=1).tolist(),limit=bound,passed=bool(np.max(difference)<bound)))
    table=np.load(BACKGROUND)
    phi=interpolate.CubicSpline(table['heavy_efold'],table['phi_h'])
    velocity=interpolate.CubicSpline(table['heavy_efold'],table['phidot_h'])
    mass=float(table['heavy_mass_mpc'])
    phases=[]
    for tag in ['a200','a225','a250']:
        scale=float(np.load(ROOT/'runs/matching-inputs'/(tag+'-w6-d8.npz'))['matching_scale'])
        kinetic=velocity(math.log(scale))**2
        potential=(scale*mass*phi(math.log(scale)))**2
        phases.append(dict(tag=tag,matching_scale=scale,instantaneous_w_before=float((kinetic-potential)/(kinetic+potential))))
    finish(folder,dict(rows=rows,all_checks_passed=all(row['passed'] for row in rows),
        number_of_late_times=int(selected.sum()),scale_interval=[.001,1.],background_crossing_phases=phases),
        __file__,[BACKGROUND,ROOT/'analyze_matching.py',*native_hashes(),
            *[ROOT/'runs'/label/'evolution.npz' for label in ['late-225',*labels]]])
    print(json.dumps(dict(rows=rows,phases=phases),indent=2))
    assert all(row['passed'] for row in rows)


if __name__=='__main__':
    main()
