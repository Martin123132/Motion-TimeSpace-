from stage166_common import *


def main():
    modest()
    folder=ROOT/'results/comparison'
    folder.mkdir(parents=True,exist_ok=False)
    assert verify_packet(ROOT/'results/source-qualification')['source_qualified']
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    reader=ShapeReadout(ladder.basis,canonical=True)
    inputs=list(ladder.inputs)+[ROOT/'results/source-qualification/status.json']
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
                low_readout=reader.apply(final['photon_low'][-1,:,8:10],final['energy_low'][-1,8:10])
                high_readout=reader.apply(final['photon_high'][-1,:,8:10],final['energy_high'][-1,8:10])
                total_readout=reader.split_values(physical_potential,final['energy'][-1,8:10])
                step54_readout=reader.apply(final['photon'][-1,:,16:18],final['energy'][-1,16:18])
                step65_readout=reader.apply(final['photon'][-1,:,18:20],final['energy'][-1,18:20])
                close(checks,f'Observable order telescope:{model}:{route}:{count}',step54_readout['amplitudes']+step65_readout['amplitudes'],total_readout['amplitudes'],1e-8)
                records[f'{model}-{route}-{count}-physical-ladder']=dict(
                    step54_amplitudes=(proof['heat']*step54_readout['amplitudes']).tolist(),
                    step65_amplitudes=(proof['heat']*step65_readout['amplitudes']).tolist(),
                    amplitude_contraction=(abs(step65_readout['amplitudes'])/np.maximum(abs(step54_readout['amplitudes']),1e-300)).tolist(),
                    residual_norm_contraction=(step65_readout['residual_norm']/np.maximum(step54_readout['residual_norm'],1e-300)).tolist(),
                    finite_ladder_diagnostic_not_continuum_error_bound=True)
                close(checks,f'Retained low response readout:{model}:{route}:{count}',high_readout['amplitudes']+low_readout['amplitudes'],total_readout['amplitudes'],1e-10)
                records[f'{model}-{route}-{count}-low-part']=dict(amplitudes=(proof['heat']*low_readout['amplitudes']).tolist(),
                    photon_over_total=(state_norm(final['photon_low'][-1,:,8:10],ladder.basis.mass)/np.maximum(state_norm(final['photon'][-1,:,8:10],ladder.basis.mass),1e-300)).tolist())
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
                    close(checks,'Independent60digit baseline amplitudes:'+label,precise['amplitudes'][:,:1],split['amplitudes'][:,:1],1e-10)
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
        convergence_passed=all(row['passed'] for row in checks if row['name'].startswith('CONVERGENCE:')),
        numerical_integrity_passed=all(row['passed'] for row in checks if not row['name'].startswith('CONVERGENCE:')),
        baseline_inner_rerun=False,high_low_response_retained=True),__file__,inputs)
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()


