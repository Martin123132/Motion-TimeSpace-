from stage166_common import *
from twofold_sources import TwofoldSources


def main():
    modest()
    folder=ROOT/'results/source-qualification'
    folder.mkdir(parents=True,exist_ok=False)
    previous=verify_packet(PARENT/'results/reference-certified')
    assert not previous['reference_replay_qualified']
    assert verify_packet(PARENT/'results/basis-representation-diagnosis')['all_checks_passed']
    assert verify_packet(PARENT/'results/sources-refined')['all_checks_passed']
    evaluator=TwofoldSources()
    checks,records=[],{}
    for window in ['earlier','terminal']:
        for route in ['local','cubic']:
            maxima={}
            for phase in np.linspace(0,1,4097):
                candidates=[(label,evaluator.complete_packet(phase,route,window,order)) for label,order in [('old',None),('repaired4',4),('repaired6',6)]]
                candidates.extend((step,evaluator.physical_packet(phase,route,window,step)) for step in ['54','65','64'])
                for label,packet in candidates:
                    for name,value in evaluator.metrics(packet).items():
                        maxima[label+':'+name]=max(maxima.get(label+':'+name,0.),value)
            for name,value in maxima.items():
                if not name.endswith('legacy_single_float_moment'):
                    test(checks,'Unchanged twofold source gate:'+window+':'+route+':'+name,value,1e-10)
            records[window+'-'+route]=maxima
            print(json.dumps(dict(window=window,route=route,checks=len(checks),failed=[row for row in checks if not row['passed']])),flush=True)
    with localcontext() as context:
        context.prec=80
        for endpoint in ENDPOINTS:
            lower=evaluator.full[(endpoint,6)]-evaluator.full[(endpoint,4)]
            close(checks,'Independent reference/physical identity:'+endpoint,np.asarray(lower,dtype=float),np.asarray(evaluator.low[(endpoint,'64')],dtype=float),1e-10)
    for phase in [0.,.25,.5,.590576171875,.75,1.]:
        for route in ['local','cubic']:
            for window in ['earlier','terminal']:
                force=evaluator.forcing(phase,route,window,slice(0,4))
                assert force['high'].shape==(98,48) and force['low'].shape==(98,48)
                for part in ['high','low']:
                    assert np.array_equal(force[part][:,12:16],np.zeros((98,4)))
                test(checks,f'Split forcing coordinate rewrite:{phase}:{route}:{window}',force['rewrite'],1e-10)
    allowed=all(row['passed'] for row in checks)
    finish(folder,dict(checks=checks,phase_records=records,phases_per_route=4097,source_qualified=allowed,
        exact_and_represented_gates_required=True,previous_failed_checks=[row for row in previous['checks'] if not row['passed']],
        source_repair_is_precision_only=True,temperature_high=evaluator.temperature_high.tolist(),temperature_low=evaluator.temperature_low.tolist(),
        temperature_curve_changed=False,bands_changed=False,tolerances_changed=False,source_adopted=False),__file__,
        [PARENT/'results/reference-certified/status.json',PARENT/'results/sources-refined/status.json',PARENT/'results/basis-representation-diagnosis/status.json',*evaluator.inputs])
    print(json.dumps(dict(allowed=allowed,checks=len(checks),failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
