from response217 import *


def freeze():
    protocol()
    path=ROOT/'reference-repair-contract.json'
    assert not path.exists()
    diagnosis=read(ROOT/'results/energy-readout-diagnosis.json')
    assert not diagnosis['failed_checks']
    files=[ROOT/'repair_reference217.py',ROOT/'ENERGY-READOUT-REPAIR.md',ROOT/'diagnose_energy217.py',ROOT/'results/energy-readout-diagnosis.json']
    files.extend((ROOT/'cases').glob('*/result.json'))
    write(path,dict(frozen_at=now(),identity_tolerance=1e-10,readout='temperature.T @ same_solve_mass @ photon',
        change='reference energy readout only; photon/gas solutions unchanged',
        files={str(path.relative_to(ROOT)):digest(path) for path in files}))
    print('Reference repair and unchanged gate frozen.',flush=True)


def repaired_energy(values,stored):
    with mp.workdps(100):
        reference=as_mp(stored[:,:36])+as_mp(stored[:,36:])
        mass=as_mp(values['mass']);temperature=as_mp(values['temperature'][:,None])
        energy=as_mp(values['energy'][None,:])
        photon=mp.matrix(96,36)
        for row,index in enumerate(values['others'],start=1):
            photon[int(index),:]=reference[row,:]
        for column in range(36):
            photon[1,column]=(reference[0,column]-mp.fsum(energy[0,int(index)]*photon[int(index),column] for index in values['others']))/energy[0,1]
        reference[0,:]=temperature.T*mass*photon
        high,low=split_matrix(reference)
        photon_high,photon_low=split_matrix(photon)
    return np.column_stack([high,low]),photon_high,photon_low


def audit_sources(model,values,rows):
    with mp.workdps(100):
        temperature=as_mp(values['temperature'][None,:])
        for name,path in SOURCES.items():
            high,low=source_for_background(path,model)
            source=as_mp(high)+as_mp(low)
            moment=temperature*source[1:97,:]
            for column in range(source.cols):
                scale=max(abs(source[0,column]),mp.mpf('1e-300'))
                check(rows,f'{model}:{name}:original energy pair:{column}',abs(source[0,column]+source[97,column])/scale,1e-10,'identity')
                check(rows,f'{model}:{name}:original source moment:{column}',abs(moment[column]-source[0,column])/scale,1e-10,'identity')


def run():
    config=protocol();contract=read(ROOT/'reference-repair-contract.json')
    for name,value in contract['files'].items():
        assert digest(ROOT/name)==value,name
    rows=[];records=[]
    for model in config['models']:
        values=packet(ROOT/f'frozen/{model}.npz')
        audit_sources(model,values,rows)
        for count in config['counts']:
            folder=ROOT/f'cases/{model}-{count}'
            output=ROOT/f'reference-energy-repair/{model}-{count}'
            assert not (output/'reference.npz').exists()
            stored=packet(folder/'reference80.npz')['state']
            repaired,photon_high,photon_low=repaired_energy(values,stored)
            system,step=system_from_frozen(values,count)
            actual=packet(folder/'direct.npz')['state']
            compare_response(f'{model}:{count}:independent physical solve, protected energy',actual,repaired,system,rows,records)
            check(rows,f'{model}:{count}:nonenergy reference rows unchanged',np.max(abs(repaired[1:]-stored[1:])),0,'integrity')
            factor=linear.cholesky(values['mass'],lower=True)
            physical=photon_high+photon_low
            actual_photon=values['transform']@matched.collapsed(actual)[:96]
            relative=np.linalg.norm(factor.T@(actual_photon-physical),axis=0)/np.maximum(np.linalg.norm(factor.T@physical,axis=0),1e-300)
            check(rows,f'{model}:{count}:physical photon comparison without energy conversion',np.max(relative),1e-10,'identity')
            ledgers(f'{model}:{count}:corrected reference',repaired,system,step,rows)
            save(output/'reference.npz',state=repaired,physical_photon_high=photon_high,physical_photon_low=photon_low,
                 original_energy_high=stored[0,:36],original_energy_low=stored[0,36:])
    failed=[row for row in rows if not row['passed']]
    write(ROOT/'results/reference-repair.json',dict(checks=rows,failed_checks=failed,records=records,qualified=not failed,
        contract_sha256=digest(ROOT/'reference-repair-contract.json'),
        files={str(path.relative_to(ROOT)):digest(path) for path in (ROOT/'reference-energy-repair').rglob('*.npz')}))
    print(json.dumps(dict(checks=len(rows),failed=len(failed),maximum_replay=max(row['relative'] for row in records))),flush=True)


if __name__=='__main__':
    inherited.source.modest()
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['freeze','run'])
    args=parser.parse_args();{'freeze':freeze,'run':run}[args.phase]()
