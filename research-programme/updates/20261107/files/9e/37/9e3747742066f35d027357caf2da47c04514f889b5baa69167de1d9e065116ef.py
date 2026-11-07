from stage168_common import *


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    comparison=verify_packet(ROOT/'results/comparison')
    assert comparison['all_checks_passed']
    chain=ancestors()
    immediate=chain[PARENT/'results/stage-integrity.json']
    paths={PARENT/name for name in immediate['file_hashes']}
    checks,consumed,packets=[],{},{}
    for path in (ROOT/'results').rglob('status.json'):
        if path.parent==folder:
            continue
        packet=verify_packet(path.parent)
        packets[str(path.parent)]=packet
        failed=[row for row in packet['checks'] if not row['passed']]
        if path.parent==ROOT/'results/preflight':
            assert len(failed)==2 and all(row['name'].startswith('Original photon equations:') for row in failed)
        else:
            assert not failed,(path,failed)
        for name,sha in packet['input_hashes'].items():
            if name not in consumed:
                assert digest(name)==sha,name
                consumed[name]=sha
                if not Path(name).is_relative_to(ROOT):
                    paths.add(Path(name))
        checks.append(dict(name='Packet and consumed hashes:'+str(path.parent.relative_to(ROOT)),passed=True))
    prior_hashes=authenticate(paths,chain)
    evaluator=HeldoutSources()
    preflight=packets[str(ROOT/'results/preflight-audited')]
    assert preflight['closed_reference_bitwise_recovered'] and len(preflight['raw_source_failures'])==40
    assert not preflight['independent_raw_physical_source_qualified']
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    reader=ShapeReadout(ladder.basis,canonical=True)
    for model in ['heavy','cold']:
        previous=read_npz(ROOT/'results/preflight'/(model+'-smoke.npz'))
        audited=read_npz(ROOT/'results/preflight-audited'/(model+'-smoke.npz'))
        assert all(np.array_equal(previous[key],audited[key]) for key in previous)
        checks.append(dict(name='Unchanged smoke arrays and retained failures:'+model,passed=True))
        for route in ['local','cubic']:
            for count in COUNTS:
                label=f'{model}-{route}-{count}'
                location=ROOT/'results/response'/label
                packet=packets[str(location)]
                state=read_npz(location/'response.npz')
                heat=packet['heat']
                for quantity in ['photon','energy','gas','work','number','integrated_number_source','integrated_imbalance']:
                    assert np.array_equal(state[quantity],state[quantity+'_high']+state[quantity+'_low'])
                    assert np.array_equal(state[quantity][...,6:8],np.zeros_like(state[quantity][...,6:8]))
                    close(checks,'Independent source update:'+label+':'+quantity,state[quantity][...,:2]+state[quantity][...,4:6],state[quantity][...,2:4],1e-8)
                    close(checks,'Independent raw-reference audit:'+label+':'+quantity,state[quantity][...,2:4]+state[quantity][...,8:10],state[quantity][...,10:12],1e-8)
                canonical=state['energy'][:,2:4]+heat*state['gas'][:,2:4]+state['work'][:,2:4]
                scale=np.maximum(np.max(abs(state['energy'][:,2:4])+abs(heat*state['gas'][:,2:4])+abs(state['work'][:,2:4]),axis=0),1e-300)
                test(checks,'Reference closed energy/work:'+label,float(np.max(abs(canonical-canonical[0])/scale)),1e-7)
                raw=state['energy'][:,10:12]+heat*state['gas'][:,10:12]+state['work'][:,10:12]-state['integrated_imbalance'][:,10:12]
                scale=np.maximum(np.max(abs(state['energy'][:,10:12])+abs(heat*state['gas'][:,10:12])+abs(state['work'][:,10:12])+abs(state['integrated_imbalance'][:,10:12]),axis=0),1e-300)
                test(checks,'Raw independent supplied-imbalance ledger:'+label,float(np.max(abs(raw-raw[0])/scale)),1e-7)
                assert np.any(state['integrated_imbalance'][:,10:12])
                assert not np.any(state['integrated_imbalance'][:,2:4])
                direct=reader.apply(state['photon'][-1,:,2:4],state['energy'][-1,2:4])
                for match in [20,40]:
                    name=label+f'-m{match}'
                    saved=read_npz(ROOT/'results/comparison'/(name+'.npz'))
                    prior=read_npz(BRANCH/'endpoint-twofold-response-20261019/results/comparison'/(name+'.npz'))
                    assert np.array_equal(saved['potential'][:,:1],prior['potential'][:,:1])
                    assert np.array_equal(saved['potential'][:,3:5],prior['potential'][:,3:5])
                    close(checks,'Direct heldout source,not local-cubic spread:'+name,saved['potential'][:,9:11],direct['potential'],1e-10)
                    close(checks,'Heldout not added twice:'+name,saved['potential'][:,1:3]+direct['potential'],saved['potential'][:,3:5],1e-10)
                    close(checks,'Independent heldout metrics:'+name,metrics(direct,heat,reader.measure),saved['defect_metrics'],1e-10)
                    corrupt=[]
                    close(corrupt,'Injected1e-6 readout corruption',saved['defect_metrics']*1.000001,saved['defect_metrics'],1e-10)
                    assert not corrupt[0]['passed']
                    checks.append(dict(name='Readout corruption rejected:'+name,passed=True))
    summary=json.loads((ROOT/'NUMERICAL-SUMMARY.json').read_text())
    assert summary['numerical_integrity_passed'] and summary['convergence_passed']
    assert not summary['independent_raw_physical_source_qualified']
    assert summary['new_event_evaluations']==summary['new_expensive_virtual_integrations']==0
    assert summary['new_response_evolutions']==8
    assert not summary['temperature_curve_changed'] and not summary['tolerances_changed'] and not summary['curve_adopted']
    assert summary['band_orders']==[6,6,6,8,7,7,6]
    assert not summary['baseline_inner_rerun']
    scripts=list(ROOT.glob('*.py'))
    for path in scripts:
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    assert not list(ROOT.rglob('__pycache__'))
    modified=[str(path) for path in (POST.parent/'formalization-workbench').rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    assert not modified,modified[:10]
    checks.append(dict(name='Fixed controls,compile,no bytecode,protected-workbench mtime guard',passed=True))
    failures=[row for row in checks if not row['passed']]
    finish(folder,dict(checks=checks,accepted_scope_verified=not failures,compiled_scripts=len(scripts),
        consumed_and_immediate_rehashed=prior_hashes,rehashed_prior_files=len(prior_hashes),
        raw_source_failures=preflight['raw_source_failures'],retained_smoke_failures=preflight['retained_smoke_failures'],
        protected_workbench_recent_modified_file_count=0,
        protected_check_scope='Modification-time scan since16:50:41UTC19October2026;not a pre-turn content snapshot.'),
        [*consumed,*prior_hashes,ROOT/'NUMERICAL-SUMMARY.json'])
    print(json.dumps(dict(checks=len(checks),failures=failures,prior_files=len(prior_hashes))),flush=True)
    assert not failures


if __name__=='__main__':
    main()
