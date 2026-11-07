from kinetic_common import *


def main():
    modest()
    folder=ROOT/'results/evolved-source-comparison'
    folder.mkdir(parents=True,exist_ok=False)
    checks,rows,dependencies=[],[],[]
    for model in ['heavy','cold']:
        paths=dict(parent=BACKGROUND/'backgrounds'/(model+'-ir96-integrated-6400'),
                   control=ROOT/'backgrounds'/(model+'-retained-control'),
                   derived=ROOT/'backgrounds'/(model+'-derived-gaunt'),
                   coarse_control=ROOT/'backgrounds'/(model+'-retained-control-3200'),
                   coarse_derived=ROOT/'backgrounds'/(model+'-derived-gaunt-3200'))
        saved={}
        for key,path in paths.items():
            metadata=json.loads((path/'status.json').read_text())
            assert metadata['all_checks_passed']
            with np.load(path/'history.npz') as data:
                saved[key]={name:data[name].copy() for name in data.files}
            dependencies.extend([path/'status.json',path/'history.npz'])
        for key in ['profiles','energy_scaled','temperature_scaled','number_scaled','expansion_work','integrated_number_source']:
            difference=saved['control'][key]-saved['parent'][key]
            error=float(np.max(abs(difference))/max(np.max(abs(saved['parent'][key])),1e-30))
            checks.append(check('Retained-factor control reproduces prior '+model+' '+key,error,2e-12))
        fine_delta=saved['derived']['number_scaled'][-1]-saved['control']['number_scaled'][-1]
        coarse_delta=saved['coarse_derived']['number_scaled'][-1]-saved['coarse_control']['number_scaled'][-1]
        checks.append(check('Change in photon production refines in time for '+model,abs(coarse_delta/fine_delta-1),.002))
        checks.append(dict(name='Derived-factor change is resolved and small for '+model,
                           passed=bool(fine_delta!=0 and abs(fine_delta/saved['control']['number_scaled'][-1])<1e-4)))
        common=saved['derived']['energy_scaled']+saved['derived']['heat']*saved['derived']['temperature_scaled']+saved['derived']['expansion_work']
        checks.append(check('Updated photon gas and expansion work close for '+model,float(np.max(abs(common))),1e-8))
        heat=float(saved['derived']['heat'])
        number_factor=np.pi**4/(30*special.zeta(3))
        rows.append(dict(model=model,control_final_photon_number_fraction=float(heat*saved['control']['number_scaled'][-1]*number_factor),
                         derived_final_photon_number_fraction=float(heat*saved['derived']['number_scaled'][-1]*number_factor),
                         number_fraction_change=float(heat*fine_delta*number_factor),
                         relative_number_change=float(fine_delta/saved['control']['number_scaled'][-1]),
                         time_refinement_of_change=float(abs(coarse_delta/fine_delta-1)),
                         gas_temperature_fraction_change=float(heat*(saved['derived']['temperature_scaled'][-1]-saved['control']['temperature_scaled'][-1])),
                         final_total_radiation_energy_fraction=float(heat*saved['derived']['energy_scaled'][-1])))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),rows=rows,
                       both_inherited_branches_updated=True,empirical_parameters_refitted=False,
                       resolved_real_redistribution_not_inserted_before_virtual_matching=True),__file__,
           [*dependencies,ROOT/'evolve_derived_gaunt.py',ROOT/'results/derived-gaunt-bank/status.json'])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],rows=rows)),flush=True)


if __name__=='__main__':
    main()
