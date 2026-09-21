from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_barycentric_20260915 import BarycentricLiveContinuum as LiveContinuumCharacteristics
from annular_live_jump_aware_comparison_20260915 import sample_geometry_fast as sample_geometry
from annular_repaired_live_geometry_20260915 import RepairedLiveSystem, MaterialState, material_weight
from annular_repaired_live_current_20260915 import LiveTangent
import numpy as np
import json
import time


def compare_state(system, coordinates, momenta, clocks, oracle, oracle_state, label_order=6):
    rates, geometry = system.solve(coordinates, momenta)
    target_geometry = oracle.solve(oracle_state)
    material = MaterialState(system, coordinates)
    nodes, weights = np.polynomial.legendre.leggauss(label_order)
    labels, weights = nodes/2, weights*material_weight(nodes/2)/2
    scalar_difference, scalar_norm = 0., 0.
    source_errors, velocity_errors, clock_errors = [], [], []
    for label, layer_weight in zip(labels, weights):
        interpolation = material.interpolation([label])[0]
        values, velocities = interpolation @ coordinates, interpolation @ rates
        target = target_geometry.material.values([label])[0]
        layer = system.layer(label, geometry)
        endpoints = np.unique(np.concatenate([layer.radii, [values[-1], target[0]], target_geometry.edges]))
        endpoints = endpoints[(endpoints >= layer.radii[0]) & (endpoints <= layer.radii[-1])]
        lengths = np.diff(endpoints)
        radius = (endpoints[:-1, None]+lengths[:, None]*layer.fractions).ravel()
        quadrature = (lengths[:, None]*layer.weights).ravel()
        shape, radial, motion = layer.basis(radius, values[-1])
        temporal = shape @ velocities[:-1]+(motion @ values[:-1])*velocities[-1]
        gradient = radial @ values[:-1]
        target_temporal, target_gradient = sample_geometry(oracle, target_geometry, radius, np.full(len(radius), label))
        lapse, root = target_geometry.metric(radius)
        kinetic, stiffness = radius**2/(lapse*root), radius**2*lapse*root
        scalar_difference += layer_weight*np.dot(quadrature, kinetic*(temporal-target_temporal)**2+stiffness*(gradient-target_gradient)**2)
        scalar_norm += layer_weight*np.dot(quadrature, kinetic*target_temporal**2+stiffness*target_gradient**2)
        source_errors.append(abs(values[-1]-target[0]))
        lapse, root = target_geometry.metric(target[0])
        energy = np.sqrt(oracle.source_mass**2+root**2*target[1]**2)
        velocity_errors.append(abs(velocities[-1]-lapse*root**2*target[1]/energy))
        clock_errors.append(abs(interpolation @ clocks-target[2]))
    radius = np.unique(np.concatenate([np.linspace(5.21, 6.79, 257), np.linspace(6.015, 6.045, 101)]))
    target_mass = target_geometry.evaluate(radius, target_geometry.mass_coefficients)
    mass_error = float(np.max(abs(geometry.values(radius)[0]-target_mass)))
    lapse, root = geometry.metric(radius)
    target_lapse, target_root = target_geometry.metric(radius)
    return dict(field_error=float(np.sqrt(scalar_difference/scalar_norm)), scalar_norm=float(scalar_norm),
                source_error=float(max(source_errors)), velocity_error=float(max(velocity_errors)), clock_error=float(max(clock_errors)),
                mass_error=mass_error, lapse_error=float(np.max(abs(lapse-target_lapse))), root_error=float(np.max(abs(root-target_root))))


def main():
    evidence = EvidenceRun('annular-repaired-live-continuum-comparison-attempt02', __file__)
    try:
        oracle_directory = evidence.output.parent/'annular-live-continuum-degree512-attempt01'
        oracle_status_path = oracle_directory/'status.json'
        oracle_status = json.loads(oracle_status_path.read_text())
        evidence.own(oracle_status_path)
        evidence.check('independent_live_oracle_qualified', oracle_status['state'] == 'complete'
                       and oracle_status['sampled_finite_time_continuum_accuracy_qualified'])
        oracle_path = oracle_directory/'degree512.npz'
        evidence.own(oracle_path)
        saved_oracle = np.load(oracle_path)
        oracle = LiveContinuumCharacteristics(512, 8, 18, radial_spacing=.025, label_order=12)
        previous_oracle_path = evidence.output.parent/'annular-live-continuum-refinement-attempt02/degree384.npz'
        evidence.own(previous_oracle_path)
        previous_oracle_states = np.load(previous_oracle_path)['states']
        previous_oracle = LiveContinuumCharacteristics(384, 8, 18, radial_spacing=.025, label_order=12)
        force_comparison = []
        for coarse_state, fine_state in zip(previous_oracle_states, saved_oracle['states']):
            coarse_force = previous_oracle.rhs_with_geometry(coarse_state)[2]['radiation'][4]
            fine_force = oracle.rhs_with_geometry(fine_state)[2]['radiation'][4]
            force_comparison.append([float(coarse_force), float(fine_force)])
        force_comparison = np.array(force_comparison)
        oracle_force_error = float(np.max(abs(force_comparison[:, 0]-force_comparison[:, 1])))
        oracle_force_scale = float(np.max(abs(force_comparison[:, 1])))
        evidence.report['oracle_force_refinement'] = dict(forces=force_comparison.tolist(), absolute_error=oracle_force_error,
                                                         relative_error=oracle_force_error/oracle_force_scale)
        evidence.check('independent_continuum_radiation_force_refines', oracle_force_error < 2e-7
                       and oracle_force_error/oracle_force_scale < .02, evidence.report['oracle_force_refinement'])
        old_directory = evidence.output.parent/'annular-repaired-live-evolution-attempt01'
        evidence.own(old_directory/'status.json')
        for count in [17, 33, 65]:
            for gram in [False, True]:
                started = time.perf_counter()
                branch = 'MTS' if gram else 'reference'
                key = branch+'-'+str(count)
                old_path = old_directory/(key+'-main.npz')
                evidence.own(old_path)
                saved = np.load(old_path)
                system = RepairedLiveSystem(count, gram, 8, 10)
                size = 2*9*(count+1)
                rows = []
                evidence.check(key+'_same_times', np.allclose(saved['time'], saved_oracle['times'], rtol=0., atol=1e-15))
                for time_value, state, oracle_state in zip(saved['time'], saved['state'].T, saved_oracle['states']):
                    coordinates, momenta = state[:size].reshape(2, 9, count+1)
                    row = compare_state(system, coordinates, momenta, state[size:], oracle, oracle_state)
                    row['time'] = float(time_value)
                    rows.append(row)
                coordinates, momenta = saved['state'][:size, -1].reshape(2, 9, count+1)
                tangent = LiveTangent(system, coordinates, momenta)
                finite_force = -tangent.layer_data(0.)[7]
                unused, target_geometry, force = oracle.rhs_with_geometry(saved_oracle['states'][-1])
                continuum_force = force['radiation'][4]
                summary = dict(key=key, branch=branch, count=count, width=.02, coupling=.1, duration=.02,
                               seconds=time.perf_counter()-started,
                               maximum_field_error=max(row['field_error'] for row in rows), final_field_error=rows[-1]['field_error'],
                               maximum_source_error=max(row['source_error'] for row in rows),
                               maximum_velocity_error=max(row['velocity_error'] for row in rows),
                               maximum_clock_error=max(row['clock_error'] for row in rows),
                               maximum_mass_error=max(row['mass_error'] for row in rows),
                               maximum_lapse_error=max(row['lapse_error'] for row in rows),
                               final_wave_force=float(finite_force), continuum_final_wave_force=float(continuum_force),
                               final_force_absolute_error=float(abs(finite_force-continuum_force)),
                               strict_half_percent_waveform_gate=bool(max(row['field_error'] for row in rows) < .005),
                               valid_for_physics_claim=False)
                if count == 65:
                    control = compare_state(system, coordinates, momenta, saved['state'][size:, -1], oracle,
                                            saved_oracle['states'][-1], label_order=10)
                    summary['material_quadrature_field_error_change'] = abs(control['field_error']-rows[-1]['field_error'])
                    evidence.check(key+'_physical_error_material_quadrature_control', summary['material_quadrature_field_error_change'] < 1e-7, summary)
                diagnostic = evidence.output/(key+'-diagnostics.json')
                diagnostic.write_text(json.dumps(dict(summary=summary, times=rows), indent=2, allow_nan=False)+'\n', encoding='utf-8')
                evidence.own(diagnostic, 'outputs')
                evidence.report['cases'].append(summary)
                evidence.save()
                print(summary, flush=True)
                evidence.check(key+'_finite_physical_norm_and_diagnostics', all(np.isfinite(row['field_error']) and row['scalar_norm'] > 0 for row in rows))
                evidence.check(key+'_source_and_clock_smoke_accuracy', summary['maximum_source_error'] < 5e-7
                               and summary['maximum_velocity_error'] < 2e-5 and summary['maximum_clock_error'] < 2e-7, summary)
        for branch in ['reference', 'MTS']:
            rows = [row for row in evidence.report['cases'] if row['branch'] == branch]
            evidence.check(branch+'_sampled_waveform_refines', rows[-1]['maximum_field_error'] < .8*rows[-2]['maximum_field_error']
                           and rows[-2]['maximum_field_error'] < .8*rows[-3]['maximum_field_error'], rows)
        evidence.report.update(independent_live_continuum_comparison_completed=True,
                               strict_live_waveform_accuracy_qualified=all(row['strict_half_percent_waveform_gate'] for row in evidence.report['cases'] if row['count'] == 65),
                               strict_half_percent_gate_not_relaxed=True, same_original_repaired_live_preparation=True,
                               same_finite_width_and_coupling=True, original_Gram_rows_retained=True,
                               moving_field_source_momentum_rate_retained_in_force=True,
                               physical_quadrature_splits_both_source_positions=True,
                               additional_live_force_resolution_required=True, full_GR_limit_proven=False, valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
