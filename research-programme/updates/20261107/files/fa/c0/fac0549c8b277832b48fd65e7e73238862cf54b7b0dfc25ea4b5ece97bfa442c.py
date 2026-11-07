from window_transfer_common import *


def main():
    modest()
    folder=ROOT/'results/transfer-preflight'
    folder.mkdir(parents=True,exist_ok=False)
    ancestors=sealed_ancestors()
    parent=json.loads((PARENT/'results/stage-integrity.json').read_text())
    for name,expected in parent['file_hashes'].items():
        assert digest(PARENT/name)==expected,name
    authority_path=PARENT/'results/refinement-response-stable/status.json'
    authority=json.loads(authority_path.read_text())
    assert authority['numerical_integrity_all_passed'] and authority['stable_increment_independently_evolved']
    for path,expected in authority['input_hashes'].items():
        assert digest(path)==expected,path
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    coordinates=EnergyCoordinates(basis)
    endpoint=Spectra(1.)
    assert np.array_equal(endpoint.basis.mass,basis.mass)
    checks=[dict(name='Stage106 payloads unchanged and stable authority accepted',value=len(parent['file_hashes']),passed=True)]
    inputs=[authority_path,*ladder.inputs,*endpoint.inputs]
    coverage={}
    for model in ['heavy','cold']:
        background=thermal_wave.thermal.ThermalBackground(model)
        emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
        temperatures=[]
        maximum=0.
        for coordinate in np.linspace(.5*background.end,background.end,1025):
            local=background.at(coordinate)
            theta=local['thermal_parameter']
            assert ladder.temperatures[0]*(1-1e-12)<=theta<=ladder.temperatures[-1]*(1+1e-12)
            assert emission.temperatures[0]*(1-1e-12)<=theta<=emission.temperatures[-1]*(1+1e-12)
            assert background.parent.solution.t[0]<=local['moment']<=background.parent.solution.t[-1]
            assert all(np.isfinite(value) and value>0 for value in [theta,local['coefficient'],local['hubble'],background.chi])
            operator=ladder.at(theta,0)[:96,:96]-emission.at(theta,'dcbr')
            assert operator.shape==(96,96) and np.isfinite(operator).all()
            maximum=max(maximum,float(np.max(abs(operator))))
            temperatures.append(theta)
        for count in [128,256,512]:
            saved,path=load_terminal(model,count)
            assert saved['photon'].shape==(count+1,96,16) and saved['gas'].shape==(count+1,16)
            assert saved['coordinate'][-1]==.5*background.end
            state=np.vstack([saved['energy'][-1],saved['photon'][-1,coordinates.others]])
            reconstructed=coordinates.transform@state
            relative=photon_norm(reconstructed-saved['photon'][-1],basis.mass)/np.maximum(photon_norm(saved['photon'][-1],basis.mass),1e-300)
            checks.append(dict(name=f'Saved independent-energy terminal reconstruction:{model}-{count}',value=float(relative.max()),passed=bool(relative.max()<1e-12)))
            inputs.append(path)
        assert abs(endpoint.coordinate-background.end)<1e-14
        for path in endpoint.inputs:
            if path.name in ['history.npz','tail.npz']:
                with np.load(path) as archive:
                    assert archive['expansion'][0]<=0 and archive['expansion'][-1]>=background.end-1e-14
        coverage[model]=dict(start_fraction=.5,end_fraction=1.,start_scale=background.at(.5*background.end)['scale'],
            final_scale=background.at(background.end)['scale'],temperature_start=temperatures[0],temperature_end=temperatures[-1],
            compton_temperature_range=ladder.temperatures[[0,-1]].tolist(),
            emission_temperature_range=emission.temperatures[[0,-1]].tolist(),
            tested_downstream_knots=len(temperatures),maximum_operator_entry=maximum,heat=background.chi)
        inputs.extend([*emission.inputs,background.parent.source,background.native_constants])
        checks.extend([dict(name='Full downstream operator/background coverage without extrapolation:'+model,passed=True),
            dict(name='Final saved profile and tail domain cover the transfer:'+model,passed=True)])
    for path in dict.fromkeys(inputs):
        verify_reference(path,ancestors)
    checks.append(dict(name='Every reused input has an unchanged sealed owner',passed=True))
    finish(folder,dict(checks=checks,coverage=coverage,column_order=authority['column_order'],source_integrals_recomputed=0,
        prior_chain_entries=sum(len(packet['file_hashes']) for packet in ancestors.values()),
        scope='Only the already tested interval contribution;outside-window contribution remains separate.'),
        __file__,[*inputs,ROOT/'DERIVATION.md'])
    print(json.dumps(dict(checks=len(checks),coverage=coverage,failed=[row['name'] for row in checks if not row['passed']])),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
