from stage168_common import *
from fractions import Fraction
from evolve_heldout_audited import integrate
from evolve_twofold_checked import integrate as previous_integrate


def main():
    modest()
    folder=ROOT/'results/preflight-audited'
    folder.mkdir(parents=True,exist_ok=False)
    assert digest(PARENT/'results/stage-integrity.json')==PARENT_SEAL
    assert verify_packet(PARENT/'results/validation-ready')['all_checks_passed']
    evaluator=HeldoutSources()
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    inputs=[*evaluator.inputs,*ladder.inputs,PARENT/'results/validation-ready/status.json']
    checks=[]
    nodes=list(map(Fraction,[0,.25,.5,1]))
    weights=[]
    for index,node in enumerate(nodes):
        weight=Fraction(1)
        for other_index,other in enumerate(nodes):
            if index!=other_index:
                weight*=(Fraction(3,4)-other)/(node-other)
        weights.append(weight)
    assert weights==[Fraction(1,4),Fraction(-1),Fraction(3,2),Fraction(1,4)]
    for degree in range(4):
        assert sum(weight*node**degree for weight,node in zip(weights,nodes))==Fraction(3,4)**degree
    checks.append(dict(name='Exact heldout predictor coefficients and cubic reproduction',passed=True))
    old_proof=verify_packet(ROOT/'results/preflight')
    old_failures=[row for row in old_proof['checks'] if not row['passed']]
    assert len(old_failures)==2 and all(row['name'].startswith('Original photon equations:') for row in old_failures)
    inputs.extend([ROOT/'results/preflight/status.json',ROOT/'AUDIT-NORMALIZATION.md'])
    raw_failures=[]
    for route in ['local','cubic']:
        groups=evaluator.groups[route]
        close(checks,'Current source telescope:'+route,groups[0].high+groups[2].high,groups[1].high,1e-10)
        close(checks,'Independent raw source telescope:'+route,groups[1].high+groups[4].high,groups[5].high,1e-10)
        for name,record in evaluator.raw_metrics[route].items():
            for metric in ['exact_pair','exact_moment','represented_pair','represented_moment']:
                row=dict(name=route+':'+name+':'+metric,value=record[metric],limit=1e-10,passed=record[metric]<=1e-10)
                if not row['passed']:
                    raw_failures.append(row)
        for phase in np.linspace(0,1,65):
            supplied=evaluator.forcing(phase,route,slice(0,4))
            test(checks,'Frozen coordinate rewrite:'+route+':'+str(phase),supplied['rewrite'],1e-10)
        np.savez_compressed(folder/(route+'-sources.npz'),high=np.stack([packet.high for packet in groups]),
            low=np.stack([packet.low for packet in groups]),raw_high=np.stack([packet.high for packet in evaluator.raw_packets[route]]),
            raw_low=np.stack([packet.low for packet in evaluator.raw_packets[route]]),mass=evaluator.data['mass'],
            temperature=evaluator.data['temperature'],groups=np.array(GROUPS))
    assert raw_failures
    for model in ['heavy','cold']:
        selection=slice(0,2) if model=='heavy' else slice(2,4)
        background=thermal_wave.thermal.ThermalBackground(model)
        emission=NonlocalEmission(ladder.basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
        inputs.extend([*emission.inputs,background.parent.source,background.native_constants])
        initial={key:np.zeros((96,24)) if key=='photon' else np.zeros(24) for key in
            ['photon','energy','gas','work','integrated_number_source']}
        forcing=lambda phase:evaluator.forcing(phase,'cubic',selection,closed=True)
        old,old_checks,unused=previous_integrate(model,32,initial,forcing,ladder,background,emission,.75,1.,model+'-closed-old')
        new,new_checks,unused=integrate(model,32,initial,forcing,ladder,background,emission,.75,1.,model+'-closed-new')
        checks.extend(old_checks+new_checks)
        for key in old:
            assert np.array_equal(old[key],new[key]),(model,key)
        assert np.all(new['integrated_imbalance']==0)
        checks.append(dict(name='Closed reference recovered bitwise:'+model,passed=True))
        raw,raw_checks,raw_metrics=integrate(model,32,initial,lambda phase:evaluator.forcing(phase,'cubic',selection),ladder,background,emission,.75,1.,model+'-raw-audit')
        checks.extend(raw_checks)
        original_path=ROOT/'results/preflight'/(model+'-smoke.npz')
        original=read_npz(original_path)
        assert all(np.array_equal(raw[key],original[key]) for key in original)
        checks.append(dict(name='Audit check separation leaves all computed arrays bitwise unchanged:'+model,passed=True))
        inputs.append(original_path)
        assert np.any(raw['integrated_imbalance'][:,8:12])
        assert np.array_equal(raw['integrated_imbalance'][:,2:4],np.zeros_like(raw['integrated_imbalance'][:,2:4]))
        np.savez_compressed(folder/(model+'-smoke.npz'),**raw)
    report=dict(checks=checks,raw_source_failures=raw_failures,raw_source_metrics=evaluator.raw_metrics,
        source_records=evaluator.source_records,numerical_production_allowed=all(row['passed'] for row in checks),
        independent_raw_physical_source_qualified=False,closed_reference_bitwise_recovered=True,
        raw_imbalance_explicit=True,retained_smoke_failures=old_failures,raw_difference_has_separate_backward_error_gate=True,temperature_curve_changed=False,
        historical_profile_retained=True,pointwise_defect_does_not_determine_true_history=True)
    finish(folder,report,inputs)
    print(json.dumps(dict(checks=len(checks),failures=[row for row in checks if not row['passed']],raw_failures=len(raw_failures),
        source=evaluator.source_records)),flush=True)
    assert report['numerical_production_allowed']


if __name__=='__main__':
    main()
