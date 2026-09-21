from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_primitive_geometry_20260918 import PrimitiveP2System
from annular_live_P2_current_20260918 import P2Material, LiveP2Tangent
from derive_annular_P2_broken_traction_identity_20260918 import broken_traction
from run_annular_P2_continuum_bridge_20260918 import checked_load
from time import perf_counter
import argparse
import hashlib
import json
import numpy as np


def checked_json(evidence, folder, name):
    status_path = evidence.output.parent/folder/'status.json'
    status = json.loads(status_path.read_text())
    path = status_path.parent/name
    expected = status['outputs'][str(path.relative_to(evidence.root))]
    evidence.check(folder+'_hash_'+name, status['state'] == 'complete'
        and hashlib.sha256(path.read_bytes()).hexdigest() == expected)
    evidence.own(status_path)
    evidence.own(path)
    return json.loads(path.read_text())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--branch', choices=['reference', 'MTS'], required=True)
    args = parser.parse_args()
    evidence = EvidenceRun('annular-P2-saved-force-budget-'+args.branch+'-attempt01', __file__)
    try:
        started = perf_counter()
        evidence.report.update(github_action=False, subagents_used=False, no_forward_evolution=True,
            same_saved_canonical_polynomials=True, finite_Gram_retained=True,
            material_transfer_not_an_evolved_material_refinement=True,
            not_a_trajectory_time_refinement=True, no_force_correction_applied=True,
            full_live_P2_force_convergence_proven=False, force_extraction_gate=2e-9)
        saved = checked_load(evidence, 'annular-P2-continuum-bridge-'+args.branch+'-65-attempt01', 'trajectory.npz')
        comparison = checked_json(evidence, 'annular-P2-continuum-comparison-65-attempt01', args.branch+'-65.json')
        initial_system = PrimitiveP2System(65, args.branch == 'MTS', layer_degree=14,
            radial_degree=18, action_order=32, label_order=20)
        index = 0 if args.branch == 'reference' else 1
        coordinates, momenta = saved['states'].reshape(5, 2, len(initial_system.labels), initial_system.count+1)[index]
        material = P2Material(initial_system, coordinates)
        probes = np.linspace(-.5, .5, 101)
        initial_interpolation = material.interpolation(probes)
        target = comparison['times'][index]
        evidence.check('saved_and_comparison_time_match', float(saved['times'][index]) == target['time'])
        configurations = [
            ('baseline', 14, 18, 32, 20),
            ('action48', 14, 18, 48, 20),
            ('action64', 14, 18, 64, 20),
            ('label28', 14, 18, 32, 28),
            ('radial26', 14, 26, 32, 20),
            ('material18', 18, 18, 32, 20),
            ('material22', 22, 18, 32, 20),
            ('combined', 22, 26, 64, 28),
        ]
        baseline_force = None
        for name, degree, radial, action, label in configurations:
            case_started = perf_counter()
            system = PrimitiveP2System(65, args.branch == 'MTS', layer_degree=degree,
                radial_degree=radial, action_order=action, label_order=label)
            interpolation = material.interpolation(system.labels)
            position, momentum = interpolation @ coordinates, interpolation @ momenta
            transferred = P2Material(system, position)
            checked_interpolation = transferred.interpolation(probes)
            transfer_error = float(max(np.max(abs(checked_interpolation @ position-initial_interpolation @ coordinates)),
                np.max(abs(checked_interpolation @ momentum-initial_interpolation @ momenta))))
            evidence.check(name+'_canonical_polynomial_preserved', transfer_error < 2e-12, transfer_error)
            tangent = LiveP2Tangent(system, position, momentum)
            current = tangent.layer_data(0.)
            row = broken_traction(tangent)
            controlled = broken_traction(tangent, order=48)
            if baseline_force is None:
                baseline_force = row['force']
            lapse, root = tangent.geometry.metric(current.coordinates[-1])
            canonical = float(system.canonical_residual(position, momentum, tangent.rates, tangent.geometry))
            radial_residual = [float(value) for value in tangent.geometry.off_grid_residual(tangent.rates)]
            row.update(configuration=name, branch=args.branch, time=float(saved['times'][index]),
                base_count=65, layer_degree=degree, radial_degree=radial, action_order=action, label_order=label,
                transfer_error=transfer_error, canonical_residual=canonical, radial_residual=radial_residual,
                source_Euler_residual=float(abs(current.source_euler)),
                scalar_Euler_residual=float(max(abs(current.euler))),
                source_position=float(current.coordinates[-1]), source_velocity=float(current.rates[-1]),
                clock_rate=float(np.sqrt(lapse**2-current.rates[-1]**2/root**2)),
                continuum_force=float(target['continuum_wave_force']),
                force_difference_from_baseline=float(row['force']-baseline_force),
                force_error_from_continuum=float(row['force']-target['continuum_wave_force']),
                identity_quadrature_change=abs(controlled['derived_defect']-row['derived_defect']),
                seconds=perf_counter()-case_started)
            evidence.report['cases'].append(row)
            evidence.save()
            print(json.dumps(row), flush=True)
            evidence.check(name+'_canonical_radial_inversion', canonical < 2e-10
                and max(radial_residual) < 2e-9, [canonical, radial_residual])
            evidence.check(name+'_broken_traction_identity', row['identity_error'] < 2e-9, row['identity_error'])
            evidence.check(name+'_identity_quadrature', row['identity_quadrature_change'] < 2e-9)
            if name == 'baseline':
                evidence.check('saved_force_reproduced', abs(row['force']-target['force']['reduced_wave_force']) < 2e-12,
                    row['force']-target['force']['reduced_wave_force'])
        changes = {row['configuration']: row['force_difference_from_baseline'] for row in evidence.report['cases']}
        maximum = max(abs(value) for value in changes.values())
        evidence.report.update(seconds=perf_counter()-started, maximum_force_change=maximum,
            tested_held_state_controls_below_extraction_gate=maximum < 2e-9,
            not_a_certified_numerical_error_bound=True,
            existing_trajectory_accuracy_gates_unchanged=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
