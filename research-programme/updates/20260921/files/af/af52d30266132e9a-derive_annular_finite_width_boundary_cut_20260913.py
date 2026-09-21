import hashlib
import json
import sys
import traceback
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as np
    from annular_canonical_common_profile_aligned_20260912 import CommonProfile
    from annular_finite_width_boundary_cut_20260913 import CutPreparation

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260913'
    destination = intake / 'annular-finite-width-boundary-cut-attempt01'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'checks': [], 'inputs': {}, 'outputs': {}, 'cases': [], 'collar_controls': [],
              'valid_for_physics_claim': False, 'full_first_jet_closed': False, 'full_GR_limit_proven': False,
              'full_physical_radial_port_action_signed': False, 'boundary_histories_complete': False,
              'unique_parent_regularizer_derived': False, 'new_spacetime_evolution': False,
              'point_scalar_reaction_derived': False, 'old_forced_IBVP_solved': False,
              'candidate_cross_cut_action_decomposition_constructed': True,
              'original_cut_radii_mass_value_drive_outer_scalar_velocity_clock_values_targeted': True,
              'momentum_lifts_are_initial_data_unknowns_not_C1_force_fits': True,
              'matched_tolerance': 1e-10}

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        save()
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    save()
    try:
        previous_path = intake / 'annular-finite-width-bulk-current-final-integrity.json'
        previous = json.loads(previous_path.read_text())
        check('previous_bulk_seal_complete_without_boundary_promotion', previous['state'] == 'complete' and not previous['full_physical_radial_port_action_signed'])
        for table in ['inputs', 'outputs']:
            for filename, expected in previous[table].items():
                if filename in report['inputs']:
                    continue
                if hashlib.sha256((root / filename).read_bytes()).hexdigest() != expected:
                    raise RuntimeError('Changed inherited evidence: ' + filename)
                report['inputs'][filename] = expected
        own(previous_path)
        for path in [Path(__file__), root / 'scripts/annular_finite_width_boundary_cut_20260913.py']:
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
            snapshot = destination / ('executed-' + path.name)
            snapshot.write_bytes(path.read_bytes())
            own(snapshot, 'outputs')
        common = CommonProfile(root)
        outer_clock = float(common.coarse.system.outer_clock)
        branch_drive = None
        for branch in ['GR', 'metric_Gram']:
            source_path = root / 'source-intake/navier-stokes/20260912/annular-interface-layer-clock-attempt03' / (branch + '_source_snapshot.npz')
            drive_path = root / 'source-intake/navier-stokes/20260912/annular-cubic-lapse-boundary-attempt07' / (branch + '_corrected_initial_data.npz')
            with np.load(source_path, allow_pickle=False) as archive:
                source = {key: archive[key].copy() for key in archive.files}
            with np.load(drive_path, allow_pickle=False) as archive:
                drive = archive['boundary_velocity'].copy()
            own(source_path)
            own(drive_path)
            kinetic_seed = common.kinetic(source['radii'])[0]
            check(branch + '_archived_clock_matches_owner', abs(source['lapse'][-1] / np.sqrt(1 - 2 * source['mu'][-1] / source['radii'][-1]) - outer_clock) < 1e-11)
            if branch_drive is not None:
                check('same_driven_components_in_GR_MTS', np.array_equal(drive[[0, 2]], branch_drive[[0, 2]]))
            branch_drive = drive
            for case, (width, shape) in enumerate([(1 / 128, 'beta22'), (1 / 256, 'beta22'), (1 / 128, 'beta23')]):
                name = branch + '_' + str(case)
                preparation = CutPreparation(source, branch != 'GR', kinetic_seed, outer_clock, drive, width, shape)
                coefficients, model, solve_status = preparation.solve()
                primary = model.unrestricted_checks(order=24, degree=28)
                higher = model.unrestricted_checks(order=36, degree=44)
                scalar = model.stencil([0.])
                residuals = [higher['endpoint_mu'][0] - source['mu'][0], higher['endpoint_mu1'][0] - drive[0],
                             scalar['q'][0, -1] - drive[2], higher['endpoint_N'][-1] / higher['endpoint_U'][-1] - outer_clock,
                             *higher['endpoint_P1']]
                check(name + '_actual_original_initial_boundary_conditions', max(abs(value) for value in residuals) < 1e-10, residuals)
                check(name + '_unrestricted_C0_C1_primary_higher', max(abs(data[key]).max() for data in [primary, higher] for key in ['C0', 'C1']) < 1e-10)
                check(name + '_boundary_and_connection_negative_controls', min(abs(higher[key]).max() for key in ['no_radial_boundary_C0', 'no_radial_boundary_C1', 'no_connection_time_C1']) > 1e-10)
                check(name + '_boundary_power_is_derived_metric_work', abs(higher['boundary_power'] - np.array([-1., 1.]) * higher['endpoint_N'] * higher['endpoint_mu1'] / (.1 * higher['endpoint_U'])).max() < 1e-13)
                direct_current = np.array([model.direct_flux(radius, order=40) for radius in source['radii'][[0, -1]]])
                check(name + '_direct_cross_cut_current_matches', abs(direct_current - higher['endpoint_K']).max() < 1e-11)
                check(name + '_positive_geometry_and_finite_arrays', all(np.isfinite(value).all() for value in higher.values()) and min(higher['U'].min(), higher['N'].min(), scalar['J'].min()) > 0)
                row = {'branch': branch, 'case': case, 'width': width, 'shape': shape, 'coefficients': coefficients.tolist(), 'solve': solve_status,
                       'source_inner_mass_drive': float(drive[0]), 'source_outer_scalar_velocity': float(drive[2]), 'source_outer_clock': outer_clock,
                       'inner_scalar_velocity_derived_not_fixed': float(scalar['q'][0, 0]), 'maximum_initial_boundary_error': float(max(abs(value) for value in residuals)),
                       'C0_max': float(max(abs(primary['C0']).max(), abs(higher['C0']).max())), 'C1_max': float(max(abs(primary['C1']).max(), abs(higher['C1']).max())),
                       'no_radial_boundary_C1_max': float(abs(higher['no_radial_boundary_C1']).max()), 'no_connection_time_C1_max': float(abs(higher['no_connection_time_C1']).max()),
                       'boundary_power': higher['boundary_power'].tolist(), 'outer_mass_rate_not_prescribed': float(higher['endpoint_mu1'][-1]),
                       'maximum_momentum_change': float(abs(model.momentum - source['momentum']).max()), 'minimum_F': float(higher['U'].min()**2),
                       'lapse_endpoint_log_slope_lifts': model.clock_adjustment[0].tolist(), 'full_first_jet_closed': False, 'old_forced_IBVP_solved': False}
                report['cases'].append(row)
                for label, data in [('primary', primary), ('higher', higher)]:
                    path = destination / (name + '_' + label + '.npz')
                    np.savez_compressed(path, **data)
                    own(path, 'outputs')
                path = destination / (name + '_prepared_collar.npz')
                np.savez_compressed(path, coefficients=coefficients, radii=model.radii, momentum=model.momentum,
                                    scalar=model.scalar, scalar_slope=model.scalar_slope, momentum_slope=model.momentum_slope,
                                    kinetic_seed=kinetic_seed, lifts=preparation.lifts, drive=drive, outer_clock=outer_clock,
                                    lapse_adjustment=model.clock_adjustment[0], lapse_normalization=model.clock_adjustment[1])
                own(path, 'outputs')
                if case == 0:
                    perturbed = preparation.build(coefficients, exterior_kick=.2)
                    probes = np.linspace(model.radii[0], model.radii[-1], 193)
                    baseline_metric, changed_metric = model.metric(probes), perturbed.metric(probes)
                    metric_error = max(abs(changed_metric[key] - baseline_metric[key]).max() for key in ['mu', 'U', 'N'])
                    endpoint_scalar_error = max(abs(perturbed.stencil([0.])[key] - scalar[key]).max() for key in ['chi', 'p', 'q'])
                    change_current = perturbed.direct_flux(model.radii[0], order=48) - direct_current[0]
                    check(branch + '_point_traces_do_not_own_collar_current', metric_error < 1e-11 and endpoint_scalar_error < 1e-11 and abs(change_current) > 1e-7)
                    report['collar_controls'].append({'branch': branch, 'exterior_only_momentum_perturbation': .2, 'interior_metric_max_change': float(metric_error), 'all_original_node_trace_max_change': float(endpoint_scalar_error), 'inner_current_change': float(change_current), 'perturbed_drive_not_reimposed': True})
                save()
                print(json.dumps(row), flush=True)
        for module in tuple(sys.modules.values()):
            filename = getattr(module, '__file__', None)
            if filename:
                path = Path(filename).resolve()
                if path.parent == root / 'scripts' and path.suffix == '.py':
                    own(path)
        check('six_matched_initial_preparations_complete', len(report['cases']) == 6)
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        report['state'] = 'complete'
        save()
    except Exception as error:
        report.update({'state': 'failed', 'error': repr(error), 'traceback': traceback.format_exc()})
        save()
        raise


if __name__ == '__main__':
    run()
