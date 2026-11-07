from stage165_common import *


def main():
    modest()
    folder=ROOT/'results/comparison'
    folder.mkdir(parents=True,exist_ok=False)
    assert verify_packet(ROOT/'results/reference-certified')['reference_replay_qualified']
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    reader=ShapeReadout(ladder.basis,canonical=True)
    inputs=list(ladder.inputs)+[ROOT/'results/reference-certified/status.json']
    checks,records=[],{}
    for model in ['heavy','cold']:
        for route in ['local','cubic']:
            states={}
            for count in COUNTS:
                location=ROOT/'results/response'/f'{model}-{route}-{count}'
                proof=verify_packet(location)
                assert proof['all_checks_passed']
                states[count]={window:read_npz(location/(window+'.npz')) for window in ['earlier','terminal']}
                inputs.extend([location/'status.json',location/'earlier.npz',location/'terminal.npz'])
                final=states[count]['terminal']
                reference_potential=reader.values@final['photon'][-1,:,2:4]
                physical_potential=reader.values@final['photon'][-1,:,8:10]
                combined_potential=reader.values@final['photon'][-1,:,10:12]
                close(checks,f'Final reference/physical superposition:{model}:{route}:{count}',reference_potential+physical_potential,combined_potential,1e-8)
                for match in [20,40]:
                    label=f'{model}-{route}-{count}-m{match}'
                    prior_path=READOUT_OWNER/'results/comparison'/(label+'.npz')
                    prior=read_npz(prior_path)
                    inputs.append(prior_path)
                    baseline=prior['potential'][:,:1]
                    saved=prior['potential'][:,3:5]
                    before=saved+reference_potential
                    after=before+physical_potential
                    reference_energy=final['energy'][-1,2:4]
                    physical_energy=final['energy'][-1,8:10]
                    before_energy=prior['energy'][3:5]+reference_energy
                    after_energy=before_energy+physical_energy
                    potential=np.column_stack([baseline,before,after,baseline+before,baseline+after,physical_potential,reference_potential,saved])
                    energy=np.r_[prior['energy'][:1],before_energy,after_energy,prior['energy'][:1]+before_energy,
                        prior['energy'][:1]+after_energy,physical_energy,reference_energy,prior['energy'][3:5]]
                    split=reader.split_values(potential,energy)
                    inherited.invariants(checks,reader,split,label)
                    assert np.array_equal(potential[:,:1],prior['potential'][:,:1])
                    assert np.array_equal(split['amplitudes'][:,:1],prior['amplitudes'][:,:1])
                    precise=precise_readout(dict(potential=potential,energy=energy),reader)
                    test(checks,'Same baseline60digit cancellation:'+label,precise['same_baseline_cancellation'],1e-8)
                    close(checks,'Physical increment60digit amplitudes:'+label,precise['amplitudes'][:,3:5],split['amplitudes'][:,9:11],1e-8)
                    close(checks,'Physical increment60digit residual:'+label,precise['residual'][:,3:5],split['residual'][:,9:11],1e-10)
                    direct=reader.split_values(reference_potential,reference_energy)
                    close(checks,'Independent numerical-reference amplitude:'+label,direct['amplitudes'],split['amplitudes'][:,11:13],1e-10)
                    records[label]=dict(reference_amplitudes=(proof['heat']*direct['amplitudes']).tolist(),
                        physical_amplitudes=(proof['heat']*split['amplitudes'][:,9:11]).tolist(),
                        reference_mu_y_over_saved=(abs(direct['amplitudes'])/np.maximum(abs(prior['amplitudes'][:,3:5]),1e-300)).tolist(),
                        physical_mu_y_over_saved=(abs(split['amplitudes'][:,9:11])/np.maximum(abs(prior['amplitudes'][:,3:5]),1e-300)).tolist(),
                        baseline_unchanged=True,reference_is_arithmetic_only=True,adopted=False)
                    np.savez_compressed(folder/(label+'.npz'),**split,frequency=reader.frequency,measure=reader.measure,heat=proof['heat'])
            for window in ['earlier','terminal']:
                for label,selection in [('reference',slice(2,4)),('physical64',slice(8,10)),('combined',slice(10,12)),
                    ('physical54',slice(16,18)),('physical65',slice(18,20))]:
                    for quantity in ['photon','gas']:
                        fine=states[4096][window][quantity][...,selection]
                        coarse=states[2048][window][quantity][...,selection]
                        measure=lambda value:state_norm(value,ladder.basis.mass) if quantity=='photon' else abs(value)
                        ratio=measure(fine[::2]-coarse).max(axis=0)/np.maximum(measure(fine).max(axis=0),1e-300)
                        test(checks,f'CONVERGENCE:{model}:{route}:{window}:{label}:{quantity}',float(max(ratio)),.01)
                        records[f'{model}-{route}-{window}-{label}-{quantity}']=ratio.tolist()
    finish(folder,dict(checks=checks,records=records,reference_history_replayed=True,
        paired_baseline_mts=True,baseline_preserved=True,adopted=False,new_response_evolutions=16,
        convergence_passed=all(row['passed'] for row in checks if row['name'].startswith('CONVERGENCE:'))),__file__,inputs)
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
