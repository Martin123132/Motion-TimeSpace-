from stage166_common import *
from twofold_sources import TwofoldSources,LOW_INDICES


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    immediate=chain[PARENT/'results/stage-integrity.json']
    prior_paths={PARENT/name for name in immediate['file_hashes']}
    checks,packets,consumed=[],{},{}
    locations=[path.parent for path in (ROOT/'results').rglob('status.json') if path.parent!=folder]
    for location in locations:
        packet=verify_packet(location)
        packets[str(location)]=packet
        failures=[row for row in packet['checks'] if not row['passed']]
        if location==ROOT/'results/response-smoke/heavy-local-32-split/earlier':
            assert len(failures)==6 and all('combined=physical+reference' in row['name'] for row in failures)
        elif location==ROOT/'results/comparison':
            assert all(row['name'].startswith('CONVERGENCE:') for row in failures)
        else:
            assert not failures,(location,failures)
        for filename,sha in packet['input_hashes'].items():
            if filename not in consumed:
                path=Path(filename)
                assert digest(path)==sha,path
                consumed[filename]=sha
                if not path.is_relative_to(ROOT):
                    prior_paths.add(path)
        checks.append(dict(name='Complete packet,allowed failure scope and consumed hashes:'+str(location.relative_to(ROOT)),passed=True))
    prior_hashes=authenticate(prior_paths,chain)
    evaluator=TwofoldSources()
    assert np.array_equal(evaluator.data['temperature'][:2],evaluator.temperature_high)
    source=packets[str(ROOT/'results/source-qualification')]
    assert source['source_qualified'] and source['all_checks_passed'] and source['phases_per_route']==4097
    assert len(source['previous_failed_checks'])==5
    checks.append(dict(name='Frozen source high parts and old failed predicates preserved',passed=True))
    original_smoke=read_npz(ROOT/'results/response-smoke/heavy-local-32-split/earlier.npz')
    corrected_smoke=read_npz(ROOT/'results/response-smoke-checked/heavy-local-32-split/earlier.npz')
    assert original_smoke.keys()==corrected_smoke.keys()
    assert all(np.array_equal(original_smoke[key],corrected_smoke[key]) for key in original_smoke)
    for quantity in ['photon','gas','energy','work','number','integrated_number_source']:
        values=original_smoke[quantity]
        error=values[...,10:12]-values[...,8:10]-values[...,2:4]
        old_ratio=float(np.max(abs(error)))/max(float(np.max(abs(values[...,2:4]))),1e-300)
        corrected_ratio=float(np.max(abs(error)))/max(float(np.max(abs(values[...,10:12]))),1e-300)
        assert old_ratio>1e-8 and corrected_ratio<1e-8
    checks.append(dict(name='Corrected smoke is bitwise identical;only wrong-channel normalization changed',passed=True))
    with localcontext() as context:
        context.prec=80
        for window in ['earlier','terminal']:
            for route in ['local','cubic']:
                for step in ['54','65','64']:
                    for phase in [0.,.25,.32080078125,.5,.590576171875,.75,1.]:
                        packet=evaluator.physical_packet(phase,route,window,step)
                        reconstructed=np.array([[Decimal.from_float(float(high))+Decimal.from_float(float(low)) for high,low in zip(high_row,low_row)] for high_row,low_row in zip(packet.high[LOW_INDICES],packet.low[LOW_INDICES])],dtype=object)
                        assert np.array_equal(reconstructed,packet.represented)
                        scale=np.maximum(abs(reconstructed[0]),Decimal('1e-300'))
                        assert max(abs(reconstructed[0]+reconstructed[-1])/scale)<Decimal('1e-10')
                        assert max(abs(evaluator.temperature@reconstructed[1:3]-reconstructed[0])/scale)<Decimal('1e-10')
                    checks.append(dict(name='Independent represented moment replay:'+window+':'+route+':'+step,passed=True))
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    reader=ShapeReadout(ladder.basis,canonical=True)
    for model in ['heavy','cold']:
        for route in ['local','cubic']:
            for count in COUNTS:
                label=f'{model}-{route}-{count}'
                location=ROOT/'results/response'/label
                packet=packets[str(location)]
                assert packet['all_checks_passed'] and packet['high_low_outputs_retained'] and packet['mode']=='split'
                states={window:read_npz(location/(window+'.npz')) for window in ['earlier','terminal']}
                for window,state in states.items():
                    for quantity in ['photon','gas','energy','work','number','integrated_number_source']:
                        assert np.array_equal(state[quantity],state[quantity+'_high']+state[quantity+'_low'])
                        assert np.array_equal(state[quantity][...,6:8],np.zeros_like(state[quantity][...,6:8]))
                        close(checks,'Independent response superposition:'+label+':'+window+':'+quantity,
                            state[quantity][...,2:4]+state[quantity][...,8:10],state[quantity][...,10:12],1e-8)
                    assert np.any(state['photon_low'])
                    balance=state['energy']+packet['heat']*state['gas']+state['work']
                    scale=np.maximum(np.max(abs(state['energy'])+abs(packet['heat']*state['gas'])+abs(state['work']),axis=0),1e-300)
                    test(checks,'Independent carried energy/work:'+label+':'+window,float(np.max(abs(balance-balance[0])/scale)),1e-7)
                for quantity in ['photon','gas','energy','work','integrated_number_source']:
                    for suffix in ['', '_high','_low']:
                        assert np.array_equal(states['earlier'][quantity+suffix][-1],states['terminal'][quantity+suffix][0])
                checks.append(dict(name='Both response parts carried through shared endpoint:'+label,passed=True))
                final=states['terminal']
                physical=reader.values@final['photon'][-1,:,8:10]
                arithmetic=reader.values@final['photon'][-1,:,2:4]
                for match in [20,40]:
                    name=label+f'-m{match}'
                    old=read_npz(READOUT_OWNER/'results/comparison'/(name+'.npz'))
                    current=read_npz(ROOT/'results/comparison'/(name+'.npz'))
                    assert np.any(old['potential'][:,:1])
                    assert np.array_equal(current['potential'][:,:1],old['potential'][:,:1])
                    assert np.array_equal(current['amplitudes'][:,:1],old['amplitudes'][:,:1])
                    close(checks,'Saved MTS plus independently evolved reference:'+name,current['potential'][:,1:3],old['potential'][:,3:5]+arithmetic,1e-10)
                    close(checks,'Repaired MTS includes evolved physical increment:'+name,current['potential'][:,3:5],current['potential'][:,1:3]+physical,1e-10)
    summary=json.loads((ROOT/'NUMERICAL-SUMMARY.json').read_text())
    assert summary['source_qualified'] and summary['reference_history_replayed'] and summary['new_response_evolutions']==16
    assert summary['new_event_evaluations']==0 and summary['new_virtual_integrations']==0 and not summary['baseline_inner_history_rerun']
    assert not summary['temperature_curve_changed'] and not summary['tolerances_changed'] and not summary['reference_history_adopted']
    assert summary['band_orders']==[6,6,6,8,7,7,6]
    scripts=list(ROOT.glob('*.py'))
    for path in scripts:
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    assert not list(ROOT.rglob('__pycache__'))
    largest=max(sum(path.is_file() for path in directory.iterdir()) for directory in [ROOT,*[path for path in ROOT.rglob('*') if path.is_dir()]])
    assert largest<=500
    modified=[str(path) for path in (POST.parent/'formalization-workbench').rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    assert not modified,modified[:10]
    checks.append(dict(name='Compile,no bytecode,folder cap,unchanged bands/curve/tolerances and protected-workbench mtime scan',passed=True))
    assert all(row['passed'] for row in checks),[row for row in checks if not row['passed']]
    packet_checks=[row for packet in packets.values() for row in packet['checks']]
    finish(folder,dict(checks=checks,compiled_scripts=len(scripts),largest_direct_file_count=largest,
        consumed_and_immediate_rehashed=prior_hashes,rehashed_prior_files=len(prior_hashes),
        calculation_checks_including_packet_repeats=len(packet_checks),retained_failed_checks=[row for row in packet_checks if not row['passed']],
        accepted_scope_verified=True,protected_workbench_recent_modified_file_count=0,
        protected_check_scope='Modification-time scan since15:45:40UTC19Oct2026,not a pre-turn content snapshot.'),__file__,
        [*consumed,*prior_hashes,ROOT/'NUMERICAL-SUMMARY.json',ROOT/'SUPERPOSITION-TEST-CORRECTION.md'])
    print(json.dumps(dict(checks=len(checks),passed=True,prior_files=len(prior_hashes),retained_failures=sum(not row['passed'] for row in packet_checks))),flush=True)


if __name__=='__main__':
    main()
