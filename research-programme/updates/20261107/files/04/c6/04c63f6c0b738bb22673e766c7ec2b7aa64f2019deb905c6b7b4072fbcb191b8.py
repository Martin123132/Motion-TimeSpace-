from __future__ import annotations

from matching_common import *


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    checks=[]

    def check(name,passed,value=None,limit=None):
        checks.append(dict(name=name,passed=bool(passed),value=value,limit=limit))

    def report(relative):
        return json.loads((ROOT/relative).read_text())

    matching=report('runs/matching-inputs/status.json')
    comparison=report('results/late-comparison/status.json')
    probe=report('runs/independent-probes/status.json')
    controls=report('runs/prior-native-controls/status.json')
    guards=report('results/input-guards/status.json')
    identities=report('results/identities/status.json')
    check('isolated_library',Path(camb.__file__).resolve().is_relative_to(ROOT/'native'))
    check('seven_exact_averaged_identities',identities['count']==7 and identities['all_checks_passed'])
    check('all_input_guards',guards['all_checks_passed'])
    check('temporary_drive_removed',not Path('R:/').exists())
    for row in matching['matches']:
        key=str(row['nominal_a'])
        check('continuous_background_'+key,row['background_density_jump_fraction']<1e-9,row['background_density_jump_fraction'],1e-9)
        check('background_flatness_'+key,row['flatness_error']<1e-10,row['flatness_error'],1e-10)
        maximum=max(item['pressure_error_over_mode_norm'] for projection in row['projections'] for item in projection['rows'])
        check('retained_pressure_gate_'+key,maximum<2e-6,maximum,2e-6)
    for row in comparison['comparisons']:
        label=row['label']
        status=report('runs/'+label+'/status.json')
        check(label+'_finite_complete',status['state']=='complete' and status['finite'] and row['finite'])
        check(label+'_reached_today',abs(status['end_scale']-1)<2e-6,status['end_scale'],2e-6)
        check(label+'_time_scale_map',status['maximum_scale_map_error']<2e-6,status['maximum_scale_map_error'],2e-6)
        expected=0 if status['arguments']['cold'] else 1
        check(label+'_single_switch',all(value==expected for value in status['matching_count']))
        check(label+'_preserved_nonheavy_states',status['maximum_nonheavy_state_change']==0,
            status['maximum_nonheavy_state_change'],0)
        maximum=max(abs(value) for value in row['today_fractional_change_from_central'])
        if label in ['late-200','late-250']:
            check(label+'_matching_epoch_stability',maximum<.005,maximum,.005)
        if label in ['late-225-bg4','late-225-window4','late-225-degree6']:
            check(label+'_numerical_projection_stability',maximum<5e-4,maximum,5e-4)
    for row in controls['controls']:
        check(row['label']+'_prior_native_reproduced',row['maximum_column_normalized_error']<1e-8,
            row['maximum_column_normalized_error'],1e-8)
    maximum=max(row['normalized_change'] for row in probe['early_comparisons'])
    check('prior_early_standard_states_reproduced',maximum<1e-6,maximum,1e-6)
    check('mode_order_independent',probe['reversed_mode_order_error']==0,probe['reversed_mode_order_error'],0)
    for packet in probe['residuals']:
        for row in packet['rows']:
            label=str(packet['samples'])+'_k'+str(row['k'])
            check('metric_density_assembly_'+label,row['density_assembly_error']<2e-6,row['density_assembly_error'],2e-6)
            for name,value in row['maximum_normalized_residuals'].items():
                check('finite_difference_'+name+'_'+label,value<1e-3,value,1e-3)
    for row in probe['overlap']:
        check('exact_overlap_delta_k'+str(row['k']),row['delta_difference_over_mode_norm']<.005,
            row['delta_difference_over_mode_norm'],.005)
        check('exact_overlap_momentum_k'+str(row['k']),row['momentum_difference_over_mode_norm']<.005,
            row['momentum_difference_over_mode_norm'],.005)
    maximum=max(abs(value) for value in next(row for row in comparison['comparisons'] if row['label']=='late-225-raw')['today_fractional_change_from_central'])
    check('raw_handoff_negative_control_detected',maximum>.005,maximum,.005)
    check('total_matter_includes_heavy',comparison['physical_matter_includes_heavy'])
    check('no_full_spectrum_or_fit_claim',not comparison['spectrum_integral'] and not comparison['data_fit'])
    report_paths=[ROOT/path for path in ['runs/matching-inputs/status.json','results/late-comparison/status.json',
        'runs/independent-probes/status.json','runs/prior-native-controls/status.json',
        'results/input-guards/status.json','results/identities/status.json']]
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),
        finite_difference_scope='Coarse/refined time stencils with float32 cold transfer output; residual maxima are not monotonically convergent.',
        handoff_scope='Leading averaged chart with explicit projection remainder; no exact instantaneous junction claim.'),
        __file__,report_paths+native_hashes()+[ROOT/'ACCEPTANCE.md'])
    print(json.dumps(dict(count=len(checks),failed=[row for row in checks if not row['passed']]),indent=2))
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
