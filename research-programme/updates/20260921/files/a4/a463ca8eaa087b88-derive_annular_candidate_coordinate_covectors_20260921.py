from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_coordinate_covectors_20260921 import CoordinateAction, scaled_error
from annular_candidate_canonical_response_20260920 import common_material, probe_directions, restored_solver
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from run_annular_P2_continuum_bridge_20260918 import checked_load
from derive_annular_transfer_kernel_and_common_overlay_20260919 import owned_json
from annular_decimal_transport_v2_20260919 import decimal_array
from decimal import localcontext
from time import perf_counter
import contextlib
import json
import numpy as np
import sympy as sp


def symbolic_checks(evidence):
    radius, jacobian, displacement, jacobian_source, lapse, metric = sp.symbols('r J d J_b N F', positive=True)
    lapse_radial, metric_radial, gradient, rate, velocity, source_mass = sp.symbols('N_r F_r Q_xi nu V m_s')
    kinetic, spatial = jacobian*radius**2/(lapse*sp.sqrt(metric)), radius**2*lapse*sp.sqrt(metric)/jacobian
    temporal = rate-velocity*displacement*gradient/jacobian
    action = kinetic*temporal**2/2-spatial*gradient**2/2
    derivative = sum(sp.diff(action, variable)*variation for variable, variation in
        [(radius, displacement), (jacobian, jacobian_source), (lapse, lapse_radial*displacement),
         (metric, metric_radial*displacement)])
    expected = kinetic*(jacobian_source/jacobian+displacement*(2/radius-lapse_radial/lapse-metric_radial/(2*metric)))*temporal**2/2
    expected += kinetic*temporal*velocity*displacement*gradient*jacobian_source/jacobian**2
    expected -= spatial*(displacement*(2/radius+lapse_radial/lapse+metric_radial/(2*metric))-jacobian_source/jacobian)*gradient**2/2
    evidence.check('symbolic_full_moving_source_wave_covector', sp.factor(derivative-expected) == 0)
    evidence.check('symbolic_field_weak_covector', sp.factor(sp.diff(action, gradient)+
        kinetic*temporal*velocity*displacement/jacobian+spatial*gradient) == 0)
    clock = sp.sqrt(lapse**2-velocity**2/metric)
    dust = -source_mass*clock
    derivative = sp.diff(dust, lapse)*lapse_radial+sp.diff(dust, metric)*metric_radial
    evidence.check('symbolic_proper_clock_source_covector', sp.simplify(derivative+
        source_mass*(lapse*lapse_radial+velocity**2*metric_radial/(2*metric**2))/clock) == 0)


def main():
    evidence = EvidenceRun('annular-candidate-coordinate-covectors-attempt01', __file__)
    started = perf_counter()
    deadline = started+9900
    try:
        evidence.report.update(github_action=False, subagents_used=False, candidate_only=True,
            polar_zero_shift_only=True, original_live_action_unchanged=True, no_new_evolution=True,
            new_coupled_evolution=False, physical_force_mismatch_fixed=False, spatial_convergence_proven=False,
            full_live_P2_force_convergence_proven=False, general_nonzero_shift_or_temporal_current_derived=False,
            exact_finite_label_Galerkin_evolution_qualified=False, initial_physical_time=0.,
            full_coordinate_covectors_computed=False, derivative_controls=[], quadrature=[], arithmetic=[],
            fixed_metric_coordinate_variation_only=True, on_shell_coordinate_envelope_numerically_tested=False,
            tolerances=dict(directional_relative=2e-8, directional_absolute=1e-22,
                bulk_quadrature_relative=2e-6, gram_quadrature_relative=2e-5, dust_quadrature_relative=2e-6),
            no_direct_physical_acceleration_claim=True, modes_deleted=False)
        prior_path = evidence.output.parent/'annular-candidate-full-canonical-inverse-final-integrity.json'
        prior = json.loads(prior_path.read_text())
        evidence.own(prior_path)
        evidence.check('preceding_full_inverse_sealed_nonclaim', prior['state'] == 'complete'
            and prior['full_canonical_inverse_qualified'] and not prior['full_GR_limit_proven'])
        symbolic_checks(evidence)
        for branch in ['reference', 'MTS']:
            native = IndexedGradedP2System(257, branch == 'MTS', 2e-5)
            saved = checked_load(evidence, 'annular-candidate-initial-metric-attempt02', branch+'-velocity-owned-inputs.npz')
            mesh = owned_json(evidence, 'annular-transfer-kernel-overlay-attempt01', branch+'-exact-common-overlay.json')
            owner, coordinates, rates = common_material(native, saved, mesh)
            directions = probe_directions(owner, coordinates)
            density = checked_load(evidence, 'annular-candidate-initial-metric-attempt02', branch+'-radial22-density.npz')
            solver = restored_solver(owner, density, 22)
            for extension in (['reference'] if branch == 'reference' else ['primary', 'alternative']):
                case = branch+'-'+extension
                action_packet = owned_json(evidence, 'annular-complete-frozen-candidate-attempt01', case+'-action.json')
                solution = checked_load(evidence, 'annular-candidate-initial-metric-attempt02', case+'-22-metric.npz')
                action = CoordinateAction(owner, saved, mesh, action_packet, solver, solution, directions)
                path = evidence.output/(case+'-exact-state-and-variations.npz')
                np.savez_compressed(path, fields=np.array(action.exact_fields, dtype=str),
                    rates=np.array(action.exact_rates, dtype=str), factors=np.array(action.factor_vertices, dtype=str),
                    directions=np.array(action.directions, dtype=str), source=action.source, velocity=action.velocity)
                evidence.own(path, 'outputs')
                records = []
                for reference_order, material_order in [(10, 32), (16, 48)]:
                    key = case+'-'+str(reference_order)+'-'+str(material_order)
                    evidence.report['progress'] = dict(case=key, operation='compute_full_action_covectors', seconds=perf_counter()-started)
                    evidence.save()
                    print(json.dumps(evidence.report['progress']), flush=True)
                    result = action.evaluate(reference_order, material_order, deadline)
                    path = evidence.output/(key+'-covectors.npz')
                    np.savez_compressed(path, **{name:result[name] for name in ['bulk', 'gram', 'dust', 'wrong_source']},
                        gram_decimal=np.array(result['gram_decimal'], dtype=str),
                        gram_moments=np.array(result['gram_moments'], dtype=str),
                        **{name+'_contractions':values for name, values in result['contractions'].items()},
                        **{name+'_complex_derivatives':values for name, values in result['derivatives'].items()})
                    evidence.own(path, 'outputs')
                    evidence.check(key+'_finite_all_components_and_chart', all(result[name].shape == (1095, 15)
                        and np.all(np.isfinite(result[name])) for name in ['bulk', 'gram', 'dust'])
                        and result['minimum_metric'] > 0 and result['maximum_speed'] < 1,
                        dict(minimum_F=result['minimum_metric'], maximum_speed=result['maximum_speed']))
                    evidence.check(key+'_normalized_continuous_material_measure', abs(result['material_weight_sum']-1) < 2e-14)
                    for channel in ['bulk', 'gram', 'dust']:
                        for direction, (actual, expected) in enumerate(zip(result['contractions'][channel], result['derivatives'][channel])):
                            absolute = float(abs(actual-expected))
                            scale = max(abs(actual), abs(expected), 1e-30)
                            passed = absolute <= 1e-22+2e-8*scale
                            row = dict(branch=branch, extension=extension, reference_order=reference_order,
                                material_order=material_order, channel=channel, direction=direction,
                                covector_contraction=float(actual), complex_action_derivative=float(expected),
                                absolute_error=absolute, relative_error=float(absolute/scale), passed=bool(passed), valid_for_claim=False)
                            evidence.report['derivative_controls'].append(row)
                            evidence.check(key+'_'+channel+'_independent_variation_'+str(direction), passed, row)
                    negative = scaled_error(result['bulk'][-1], result['wrong_source'])
                    evidence.check(key+'_omitted_metric_spatial_terms_detected', negative > 1e-4, negative)
                    evidence.check(key+'_amplitude_gram_homogeneity', abs(result['derivatives']['gram'][-1]-2*result['actions']['gram'])
                        <= 1e-22+2e-12*abs(result['actions']['gram']))
                    records.append(result)
                    evidence.report['cases'].append(dict(branch=branch, extension=extension, reference_order=reference_order,
                        material_order=material_order, full_components=16425, sample_count=result['sample_count'],
                        minimum_F=result['minimum_metric'], maximum_speed_ratio=result['maximum_speed'],
                        omitted_metric_terms_relative_discrepancy=negative, actions=result['actions'],
                        channel_field_norms={name:float(np.linalg.norm(result[name][:-1])) for name in ['bulk', 'gram', 'dust']},
                        channel_source_norms={name:float(np.linalg.norm(result[name][-1])) for name in ['bulk', 'gram', 'dust']},
                        valid_for_claim=False))
                    evidence.save()
                for channel, tolerance in [('bulk', 2e-6), ('gram', 2e-5), ('dust', 2e-6)]:
                    for block, section in [('field', slice(None, -1)), ('source', slice(-1, None))]:
                        relative = scaled_error(records[0][channel][section], records[1][channel][section])
                        evidence.report['quadrature'].append(dict(branch=branch, extension=extension, channel=channel,
                            block=block, relative_difference=relative, tolerance=tolerance, passed=relative < tolerance,
                            spatial_convergence_test=False, valid_for_claim=False))
                with localcontext() as context:
                    context.prec = 40
                    lower = action.factor.apply(records[-1]['gram_moments'], transpose=True)
                higher = -records[-1]['gram_decimal'][:-1]
                arithmetic = scaled_error(np.asarray(lower, float), np.asarray(higher, float))
                evidence.check(case+'_Gram_transpose_40_64_digit_stability', arithmetic < 1e-20, arithmetic)
                with localcontext() as context:
                    context.prec = 64
                    prematurely_rounded = action.factor.apply(decimal_array(np.asarray(action.exact_fields, dtype=float)))
                sensitivity = scaled_error(np.asarray(prematurely_rounded, float), action.factor_values)
                evidence.report['arithmetic'].append(dict(branch=branch, extension=extension,
                    transpose_40_64_digit_relative_difference=arithmetic,
                    prematurely_rounded_field_factor_relative_difference=sensitivity,
                    original_binary_inputs_not_64_digit_physical_accuracy=True, valid_for_claim=False))
                evidence.save()
        evidence.report.update(full_coordinate_covectors_computed=True, independent_coordinate_derivatives_qualified=True,
            quadrature_qualified=all(row['passed'] for row in evidence.report['quadrature']),
            seconds=perf_counter()-started,
            next_target='Qualify a moving-coordinate stationary-envelope force response and safe all-mode trajectory step/precision before evolution; do not call canonical covectors physical accelerations.')
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), quadrature_qualified=evidence.report['quadrature_qualified'],
            seconds=perf_counter()-started)), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
