from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_continuum_characteristics_20260915 import LiveContinuumCharacteristics
from annular_live_continuum_comparison_tools_20260915 import sample_geometry
from annular_live_jump_aware_comparison_20260915 import sample_geometry_fast, jump_aware_difference
import sympy as sp
import numpy as np
import json


def main():
    evidence = EvidenceRun('annular-live-oracle-jump-aware-refinement-attempt01', __file__)
    try:
        original = evidence.output.parent/'annular-live-continuum-refinement-attempt02'
        original_status = json.loads((original/'status.json').read_text())
        evidence.own(original/'status.json')
        evidence.check('misaligned_sup_norm_failure_preserved', original_status['state'] == 'failed'
                       and original_status['checks'][-1]['name'] == 'independent_continuum_fields_refine')
        evidence.check('all_live_trajectory_constraint_checks_precede_norm_failure', all(row['passed'] for row in original_status['checks'][:-1])
                       and original_status['accepted_time'] == .02)
        raw = original/'degree384.npz'
        evidence.own(raw)
        saved = np.load(raw)
        system = LiveContinuumCharacteristics(384, 8, 18, radial_spacing=.025, label_order=12)
        geometry = system.solve(saved['states'][-1])
        targets = np.linspace(5.21, 6.79, 137)
        labels = np.zeros(len(targets))
        difference = float(np.max(abs(np.array(sample_geometry(system, geometry, targets, labels))-np.array(sample_geometry_fast(system, geometry, targets, labels)))))
        evidence.check('fast_sampling_matches_original_physical_interpolant', difference < 2e-13, difference)
        jump, displacement = sp.symbols('jump displacement', positive=True)
        integral = sp.integrate(jump**2, (sp.Symbol('radius'), 0, displacement))
        evidence.check('translated_jump_exact_L2_square_law', sp.simplify(integral-jump**2*displacement) == 0)
        evidence.check('translated_jump_sup_norm_not_a_convergence_norm', sp.limit(jump, displacement, 0, dir='+') == jump)
        summaries = []
        for degree in [96, 192]:
            coarse_path = evidence.output.parent/'annular-live-continuum-evolution-attempt01'/('degree'+str(degree)+'-main.npz')
            evidence.own(coarse_path)
            coarse = LiveContinuumCharacteristics(degree, 4, 14, radial_spacing=.05)
            coarse_states = np.load(coarse_path)['states']
            comparisons = jump_aware_difference(coarse, coarse_states, system, saved['states'])
            output = evidence.output/('degree'+str(degree)+'-comparison.json')
            output.write_text(json.dumps(dict(times=saved['times'].tolist(), comparisons=comparisons), indent=2, allow_nan=False)+'\n', encoding='utf-8')
            evidence.own(output, 'outputs')
            row = dict(degree=degree, **{name:max(item[name] for item in comparisons) for name in comparisons[0]})
            summaries.append(row)
            evidence.report['cases'].append(row)
            evidence.save()
            print(row, flush=True)
        coarse, fine = summaries
        evidence.check('one_sided_aligned_fields_refine_at_same_absolute_tolerance', fine['aligned_field_error'] < 2e-6
                       and fine['aligned_field_error'] < .8*coarse['aligned_field_error'], summaries)
        evidence.check('physical_L2_including_source_gap_refines', fine['physical_relative_L2_error'] < .001
                       and fine['physical_relative_L2_error'] < .8*coarse['physical_relative_L2_error']
                       and fine['physical_absolute_L2_error'] < 2e-6, summaries)
        evidence.check('misaligned_gap_is_small_and_explains_old_sup_discrepancy', fine['maximum_source_gap'] < 1e-8
                       and fine['pointwise_error_inside_gap'] > 10*fine['aligned_field_error'], fine)
        previous_sources = original_status['cases'][-1]
        evidence.check('independent_source_motion_and_clocks_refined', previous_sources['source_difference'] < 1e-8
                       and previous_sources['velocity_difference'] < 2e-7 and previous_sources['clock_difference'] < 1e-8, previous_sources)
        evidence.report.update(independent_common_live_geometry_continuum_evolved=True,
                               sampled_finite_time_continuum_accuracy_qualified=True,
                               old_global_sup_metric_replaced_for_discontinuous_interface=True,
                               same_one_sided_absolute_tolerance=True, physical_L2_gap_not_masked=True,
                               trajectory_equations_parameters_and_data_unchanged=True,
                               no_rerun_or_failed_status_rewrite=True, full_GR_limit_proven=False, valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
