from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_primitive_geometry_20260918 import PrimitiveP2System
from annular_live_P2_current_20260918 import P2Material, LiveP2Tangent, physical_sample
from annular_live_barycentric_20260915 import BarycentricLiveContinuum
from annular_live_jump_aware_comparison_20260915 import sample_geometry_fast, jump_aware_difference
from run_annular_live_continuum_evolution_20260915 import proper_acceleration_test
from run_annular_P2_continuum_bridge_20260918 import checked_load
import argparse
import json
import numpy as np


def physical_comparison(system, coordinates, rates, geometry, oracle, target, order=4):
    material = P2Material(system, coordinates)
    points, weights = np.polynomial.legendre.leggauss(order)
    rows = []
    for label in [-.25, 0., .25]:
        interpolation = material.interpolation([label])[0]
        values, velocity = interpolation @ coordinates, interpolation @ rates
        layer = system.layer(label, geometry)
        source = target.material.values([label])[0]
        endpoints = list(layer.mapping(layer.edges, values[-1])[0])
        for lower, upper in [(oracle.inner+oracle.width*label, source[0]),
                (source[0], oracle.outer+oracle.width*label)]:
            endpoints.extend(lower+(upper-lower)*oracle.coordinate)
        endpoints = np.unique(endpoints)
        lengths = np.diff(endpoints)
        radius = ((endpoints[:-1, None]+endpoints[1:, None])/2+lengths[:, None]*points/2).ravel()
        quadrature = (lengths[:, None]*weights/2).ravel()
        actual = np.array(physical_sample(layer, values, velocity, radius))
        expected = np.array(sample_geometry_fast(oracle, target, radius, np.full(len(radius), label)))
        lapse, root = target.metric(radius)
        norm_weights = np.stack([radius**2/(lapse*root), radius**2*lapse*root])
        error = float(quadrature @ np.sum(norm_weights*(actual-expected)**2, axis=0))
        norm = float(quadrature @ np.sum(norm_weights*expected**2, axis=0))
        target_lapse, target_root = target.metric(source[0])
        energy = np.sqrt(oracle.source_mass**2+target_root**2*source[1]**2)
        target_velocity = target_lapse*target_root**2*source[1]/energy
        lapse, root = geometry.metric(values[-1])
        clock = np.sqrt(lapse**2-velocity[-1]**2/root**2)
        target_clock = target_lapse*oracle.source_mass/energy
        rows.append(dict(label=label, physical_relative_L2_error=float(np.sqrt(error/norm)),
            physical_absolute_energy_norm=float(np.sqrt(error)), target_energy_norm=float(np.sqrt(norm)),
            source_error=float(abs(values[-1]-source[0])), velocity_error=float(abs(velocity[-1]-target_velocity)),
            proper_clock_rate_error=float(abs(clock-target_clock))))
    radius = np.unique(np.concatenate([np.linspace(5.21, 6.79, 241), np.linspace(6.015, 6.045, 101)]))
    target_mass = target.evaluate(radius, target.mass_coefficients)
    lapse, unused = geometry.metric(radius)
    target_lapse, unused = target.metric(radius)
    return dict(layers=rows, field_error=max(row['physical_relative_L2_error'] for row in rows),
        source_error=max(row['source_error'] for row in rows), velocity_error=max(row['velocity_error'] for row in rows),
        clock_rate_error=max(row['proper_clock_rate_error'] for row in rows),
        mass_error=float(max(abs(geometry.values(radius)[0]-target_mass))),
        lapse_error=float(max(abs(lapse-target_lapse))))


def reduced_force(system, coordinates, momenta, step=2e-5):
    tangent = LiveP2Tangent(system, coordinates, momenta, difference_step=step)
    current = tangent.layer_data(0.)
    actual = -current.wave_source_euler
    layer = current.layer
    changed = current.tangent_layer.evaluate(0., current.changed_coordinates, current.changed_rates)
    dust_rate = float(changed['material_momentum'].imag/current.step)
    total = float(layer.source_covector(0., current.coordinates, current.rates))
    raw_wave = float(layer.source_covector(0., current.coordinates, current.rates, wave=True))
    field_rate = float(changed['field_momenta'][-1].imag/current.step)
    return dict(reduced_wave_force=float(actual), raw_wave_covector=raw_wave,
        field_source_momentum_rate=field_rate, total_canonical_source_covector=total,
        dust_momentum_rate=dust_rate, material_covector=total-raw_wave,
        source_Euler_residual=float(abs(current.source_euler)),
        dust_balance_error=float(abs(dust_rate-(total-raw_wave+actual))),
        scalar_Euler_residual=float(max(abs(current.euler))))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--counts', nargs='+', type=int, default=[17, 33])
    args = parser.parse_args()
    tag = '-'.join(map(str, args.counts))
    evidence = EvidenceRun('annular-P2-continuum-comparison-'+tag+'-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, fixed_width=.02, coupling=.1, duration=.004,
            common_analytic_preparation=True, compare_same_Eulerian_radii=True, source_position_gap_included=True,
            waveform_labels=[-.25,0.,.25], force_labels=[0.], force_is_reduced_not_raw_covector=True,
            full_live_P2_force_convergence_proven=False, proper_acceleration_comparison_claimed=False,
            gates=dict(oracle_relative_L2=.001, oracle_aligned_field=2e-6, oracle_source_gap=1e-8,
                oracle_force_absolute=2e-7, oracle_force_peak_relative=.02,
                sampled_waveform_relative=.005, sampled_force_absolute=2e-7, sampled_force_peak_relative=.005,
                source_error=5e-7, velocity_error=2e-5, clock_rate_error=2e-7,
                force_differentiation_control=2e-9),
            gates_are_new_short_horizon_checks_not_replacement_for_old_full_horizon_failures=True,
            inherited_material_time_errors_not_rigorous_global_error_bounds=True)
        prior = evidence.output.parent/'annular-P2-tight-error-budget-final-integrity.json'
        evidence.own(prior)
        evidence.check('prior_integrity_complete', json.loads(prior.read_text())['state'] == 'complete')
        budgets = evidence.output.parent/'annular-P2-readout-error-budget-attempt01/status.json'
        evidence.own(budgets)
        evidence.report['inherited_readout_budgets'] = json.loads(budgets.read_text())['cases']
        oracles, saved = {}, {}
        for degree in [384, 512]:
            oracles[degree] = BarycentricLiveContinuum(degree, 8, 18, radial_spacing=.025, label_order=12)
            saved[degree] = checked_load(evidence, 'annular-P2-continuum-bridge-continuum-'+str(degree)+'-attempt01', 'trajectory.npz')
        times = saved[512]['times']
        evidence.check('independent_comparison_times_match', np.array_equal(times, saved[384]['times'])
            and len(times) == 5 and times[0] == 0. and times[-1] == .004)
        oracle_errors = jump_aware_difference(oracles[384], saved[384]['states'], oracles[512], saved[512]['states'])
        force_arrays, geometry_arrays = {}, {}
        for degree in [384, 512]:
            geometry_arrays[degree], force_arrays[degree] = [], []
            for state in saved[degree]['states']:
                unused, geometry, forces = oracles[degree].rhs_with_geometry(state)
                geometry_arrays[degree].append(geometry)
                force_arrays[degree].append(float(forces['radiation'][4]))
        oracle_force_error = float(max(abs(np.array(force_arrays[384])-force_arrays[512])))
        oracle_force_scale = float(max(abs(np.array(force_arrays[512]))))
        oracle_summary = dict(errors=oracle_errors, central_wave_forces=force_arrays,
            force_absolute_error=oracle_force_error, force_peak_scale=oracle_force_scale,
            force_peak_relative_error=oracle_force_error/oracle_force_scale)
        oracle_pass = (max(row['physical_relative_L2_error'] for row in oracle_errors) < .001
            and max(row['aligned_field_error'] for row in oracle_errors) < 2e-6
            and max(row['maximum_source_gap'] for row in oracle_errors) < 1e-8
            and oracle_force_error < 2e-7 and oracle_force_error/oracle_force_scale < .02)
        oracle_summary['sampled_refinement_gate_pass'] = bool(oracle_pass)
        current = oracles[512].current_test(saved[512]['states'][-1])
        acceleration = proper_acceleration_test(oracles[512], saved[512]['states'][-1])
        oracle_summary.update(final_current_error=current['error'], final_proper_acceleration_identity_error=acceleration['error'])
        evidence.report['independent_oracle'] = oracle_summary
        evidence.save()
        evidence.check('oracle_temporal_constraint_control', current['error'] < 2e-8, current['error'])
        evidence.check('oracle_derived_proper_acceleration_control', acceleration['error'] < 2e-7, acceleration['error'])
        print(dict(oracle_refinement_pass=oracle_pass, force_error=oracle_force_error,
            waveform_error=max(row['physical_relative_L2_error'] for row in oracle_errors)), flush=True)
        for count in args.counts:
            for branch in ['reference', 'MTS']:
                key = branch+'-'+str(count)
                system = PrimitiveP2System(count, branch == 'MTS', layer_degree=14, radial_degree=18,
                    action_order=32, label_order=20)
                if count == 17:
                    data = checked_load(evidence, 'annular-P2-tight-budget-'+branch+'-attempt01', 'principal.npz')
                else:
                    data = checked_load(evidence, 'annular-P2-continuum-bridge-'+key+'-attempt01', 'trajectory.npz')
                evidence.check(key+'_times_match', np.array_equal(times, data['times']))
                states = data['states'].reshape(len(times), 2, len(system.labels), system.count+1)
                rows = []
                for index, (time, state, rates) in enumerate(zip(times, states, data['rates'])):
                    coordinates, momenta = state
                    solved_rates, geometry = system.solve(coordinates, momenta)
                    evidence.check(key+'_saved_rates_'+str(index), float(max(abs(solved_rates-rates).ravel())) < 2e-10)
                    row = physical_comparison(system, coordinates, rates, geometry, oracles[512], geometry_arrays[512][index])
                    row.update(time=float(time), force=reduced_force(system, coordinates, momenta),
                        continuum_wave_force=force_arrays[512][index])
                    row['force_absolute_error'] = abs(row['force']['reduced_wave_force']-row['continuum_wave_force'])
                    if index in [0, len(times)-1]:
                        controlled = reduced_force(system, coordinates, momenta, step=1e-5)
                        row['force_half_difference_step_change'] = abs(controlled['reduced_wave_force']-row['force']['reduced_wave_force'])
                        evidence.check(key+'_force_derivative_control_'+str(index), row['force_half_difference_step_change'] < 2e-9,
                            row['force_half_difference_step_change'])
                    evidence.check(key+'_physical_force_balance_'+str(index), row['force']['dust_balance_error'] < 2e-9
                        and row['force']['source_Euler_residual'] < 2e-9, row['force'])
                    rows.append(row)
                    print(dict(key=key, time=float(time), field_error=row['field_error'], force=row['force']['reduced_wave_force'],
                        target=row['continuum_wave_force'], force_error=row['force_absolute_error']), flush=True)
                higher_order = physical_comparison(system, coordinates, rates, geometry, oracles[512], geometry_arrays[512][-1], order=8)
                quadrature_change = abs(higher_order['field_error']-rows[-1]['field_error'])
                evidence.check(key+'_waveform_quadrature_control', quadrature_change < 1e-7, quadrature_change)
                summary = dict(key=key, branch=branch, base_count=count, scalar_nodes=system.count,
                    maximum_waveform_error=max(row['field_error'] for row in rows), initial_waveform_error=rows[0]['field_error'],
                    final_waveform_error=rows[-1]['field_error'], maximum_force_error=max(row['force_absolute_error'] for row in rows),
                    maximum_source_error=max(row['source_error'] for row in rows),
                    maximum_velocity_error=max(row['velocity_error'] for row in rows),
                    maximum_clock_rate_error=max(row['clock_rate_error'] for row in rows),
                    maximum_mass_error=max(row['mass_error'] for row in rows), maximum_lapse_error=max(row['lapse_error'] for row in rows),
                    quadrature_change=quadrature_change, oracle_refinement_qualified=bool(oracle_pass),
                    final_wave_force=rows[-1]['force']['reduced_wave_force'], final_continuum_wave_force=rows[-1]['continuum_wave_force'])
                summary['peak_normalized_force_error'] = summary['maximum_force_error']/oracle_force_scale
                summary['half_percent_sampled_waveform_pass'] = bool(summary['maximum_waveform_error'] < .005)
                summary['short_sampled_force_pass'] = bool(summary['maximum_force_error'] < 2e-7
                    and summary['peak_normalized_force_error'] < .005)
                summary['source_and_clock_rate_smoke_pass'] = bool(summary['maximum_source_error'] < 5e-7
                    and summary['maximum_velocity_error'] < 2e-5 and summary['maximum_clock_rate_error'] < 2e-7)
                summary['sampled_comparison_qualified'] = bool(oracle_pass and summary['half_percent_sampled_waveform_pass']
                    and summary['short_sampled_force_pass'] and summary['source_and_clock_rate_smoke_pass'])
                path = evidence.output/(key+'.json')
                path.write_text(json.dumps(dict(summary=summary, times=rows), indent=2, allow_nan=False)+'\n', encoding='utf-8')
                evidence.own(path, 'outputs')
                evidence.report['cases'].append(summary)
                evidence.save()
        refinement = {}
        for branch in ['reference', 'MTS']:
            cases = sorted([row for row in evidence.report['cases'] if row['branch'] == branch], key=lambda row:row['base_count'])
            refinement[branch] = [dict(coarse=coarse['base_count'], fine=fine['base_count'],
                waveform_ratio=fine['maximum_waveform_error']/coarse['maximum_waveform_error'],
                force_ratio=fine['maximum_force_error']/coarse['maximum_force_error']) for coarse, fine in zip(cases[:-1],cases[1:])]
        evidence.report.update(refinement=refinement, diagnostic_completed=True,
            scientific_gate_failures=[row['key'] for row in evidence.report['cases'] if not row['sampled_comparison_qualified']],
            scientific_failure_not_erased_by_successful_execution=True,
            only_five_time_samples_not_a_continuous_time_peak_bound=True,
            no_new_full_GR_or_PPN_claim=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
