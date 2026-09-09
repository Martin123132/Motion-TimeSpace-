import hashlib
import json
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from annular_adm_mixed_action_20260909 import MixedActionBasis
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian
    from annular_metric_time_links_20260909 import finite_metric_link_potential
    from annular_action_boundary_current_20260909 import boundary_balance, canonical_momenta, changed_system, gram_current, linear_time_boundary

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    destination = intake / 'annular-action-boundary-current-derived'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': {}, 'outputs': {}, 'checks': [], 'samples': [], 'valid_for_physics_claim': False, 'scope': 'Derive actual endpoint scalar reactions, oriented Gram cut current, coefficient/momentum endpoint terms and the full temporal boundary term. Check exact global boundary-energy balance without imposing separate endpoint mass balances or modifying sources.'}
    (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    def own(path):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        report['inputs'][str(path.relative_to(root))] = digest
        return digest

    def maximum(value):
        return float(numerical.max(numerical.abs(value)))

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        save()
        print(name + ': ' + str(bool(passed)), flush=True)

    save()
    try:
        prior_path = intake / 'annular-released-Hermite-final-integrity.json'
        own(prior_path)
        prior = json.loads(prior_path.read_text())
        check('previous_released_action_complete', prior['state'] == 'complete' and prior['owner_check_count'] == 336)
        check('all_previous_sources_and_outputs_unchanged', all(own(root / name) == digest for name, digest in {**prior['inputs'], **prior['outputs']}.items()))
        for name in ['annular_action_boundary_current_20260909.py', 'derive_annular_action_boundary_current_20260909.py']:
            path = root / 'scripts' / name
            own(path)
            compile(path.read_bytes(), str(path), 'exec')
        for case_name in ['canonical', 'nonlinear_modulated']:
            case_path = intake / 'annular-constraint-correction-initial' / (case_name + '.json')
            own(case_path)
            case = json.loads(case_path.read_text())
            constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
            kappa = float(symbolic.sympify(case['normalization_kappa']))
            for intervals in [16, 32, 64]:
                for branch in ['GR', 'metric_Gram']:
                    tag = case_name + '_N' + str(intervals) + '_' + branch
                    report['active_job'] = tag
                    save()
                    source_path = intake / 'annular-released-Hermite-initial-derived' / (tag + '.npz')
                    own(source_path)
                    with numerical.load(source_path) as loaded:
                        source = {name: loaded[name].copy() for name in loaded.files}
                    basis = MixedActionBasis(source['radius'])
                    links = MetricLinkQuadrature(basis)
                    include_gram = branch != 'GR'
                    system = ReleasedHermiteRouthian(basis, source['scalar'], source['slope'], constants, kappa, source['momentum'], source['slope_momentum'], source['outer_clock'][0], links)
                    packed = source['corrected']
                    tangent = system.constraint_tangent(packed, include_gram, source['endpoint_acceleration'], source['outer_clock'][1])
                    check(tag + '_unchanged_initial_tangent', maximum(tangent['packed_speed'] - source['packed_speed']) < 2e-12)
                    balance = boundary_balance(system, packed, tangent, include_gram, source['outer_clock'][1])
                    check(tag + '_global_boundary_energy_homogeneity', maximum(balance['energy_homogeneity_error']) < 2e-11, maximum(balance['energy_homogeneity_error']))
                    check(tag + '_full_energy_work_identity', maximum(balance['full_energy_work_identity_error']) < 2e-11, maximum(balance['full_energy_work_identity_error']))
                    check(tag + '_two_end_boundary_balance_with_remainder', maximum(balance['global_boundary_identity_error']) < 2e-11, maximum(balance['global_boundary_identity_error']))
                    check(tag + '_continuum_GR_flux_sign_and_normalization', maximum(balance['continuum_GR_normalization_error']) < 1e-14)
                    check(tag + '_both_boundary_orientations_retained', balance['reaction_flux_positive_R'].shape == (2,) and balance['local_boundary_balance'].shape == (2,))
                    base_bulk = system.independent_action(packed, include_gram) + numerical.dot(system.momentum, packed[system.slices[2]]) + numerical.dot(system.slope_momentum, packed[system.slope_slice]) + system.outer_clock * packed[system.slices[0]][-1] / kappa
                    for scale in [0.999, 1.001]:
                        changed = packed.copy()
                        for selected in [system.slices[1], system.slices[2], system.slope_slice]:
                            changed[selected] *= scale
                        scaled_bulk = system.independent_action(changed, include_gram) + numerical.dot(system.momentum, changed[system.slices[2]]) + numerical.dot(system.slope_momentum, changed[system.slope_slice]) + system.outer_clock * changed[system.slices[0]][-1] / kappa
                        check(tag + '_independent_global_clock_scaling_' + str(scale), abs(scaled_bulk - scale * base_bulk) < 2e-12)
                    offshell = {name: value.copy() for name, value in tangent.items()}
                    offshell['packed_speed'][system.slices[0]] += 0.0003 * numerical.cos(31 * basis.faces)
                    offshell_balance = boundary_balance(system, packed, offshell, include_gram, source['outer_clock'][1])
                    check(tag + '_off_shell_boundary_identity_retains_free_row_work', maximum(offshell_balance['global_boundary_identity_error']) < 2e-11 and maximum(offshell_balance['global_boundary_remainder']) > 1e-10, {'identity_error': maximum(offshell_balance['global_boundary_identity_error']), 'nonzero_remainder': maximum(offshell_balance['global_boundary_remainder'])})
                    extra = {}
                    if include_gram:
                        current = gram_current(system, packed, tangent)
                        check(tag + '_factor_current_sums_vanish', maximum(current['factor_current_sum']) < 1e-13)
                        check(tag + '_cut_integral_equals_metric_link_adjoint', maximum(current['cut_shift_covector'] - current['endpoint_shift_covector']) < 1e-13)
                        check(tag + '_endpoint_link_plus_coefficient_flux_equals_reaction', maximum(current['Gram_boundary_reaction_flux'] - current['Gram_boundary_link_flux'] - current['Gram_boundary_coefficient_flux']) < 1e-14)
                        check(tag + '_actual_sampling_excludes_physical_endpoints', not numerical.any(current['endpoint_sampling_weights']))
                        step = 1e-25
                        changed = changed_system(system, packed, tangent, 1j * step, source['outer_clock'][1])
                        complex_packed = packed + 1j * step * tangent['packed_speed']
                        bare_euler = system.scalar_force(packed, False) - canonical_momenta(changed, complex_packed, False)[0].imag / step
                        check(tag + '_Gram_Euler_split_independent_of_total_reaction', maximum(balance['scalar_Euler'] - bare_euler - current['Gram_scalar_Euler']) < 2e-12)
                        if case_name == 'canonical':
                            check(tag + '_canonical_boundary_flux_is_cut_current', maximum(current['Gram_boundary_coefficient_flux']) == 0)
                        if intervals == 16:
                            probe = 0.02 * numerical.sin(23 * basis.faces)
                            boundary_rate = linear_time_boundary(system, packed, tangent, probe, 1j * step).imag / step
                            reduced = numerical.dot(tangent['Gram_shift'], probe)
                            finite_arrays = dict(source, defect=system.defect, defect_time=packed[system.slope_slice] / basis.spacing, defect_acceleration=tangent['packed_speed'][system.slope_slice] / basis.spacing, **tangent)
                            for amplitude in [0.001, 0.0005]:
                                raw = (finite_metric_link_potential(system, finite_arrays, probe, amplitude) - finite_metric_link_potential(system, finite_arrays, probe, -amplitude)) / (2 * amplitude)
                                error = abs(raw - reduced - boundary_rate)
                                check(tag + '_nonlinear_time_link_variation_with_time_boundary_' + str(amplitude), error < 2e-4 * max(abs(raw), abs(reduced), abs(boundary_rate), 1e-25) + 1e-15, {'raw': float(raw), 'reduced': float(reduced), 'time_boundary': float(boundary_rate), 'error': float(error)})
                        extra = {'Gram_' + name: value for name, value in current.items()}
                    artifact = destination / (tag + '.npz')
                    numerical.savez_compressed(artifact, **balance, **extra, **{'offshell_' + name: value for name, value in offshell_balance.items()})
                    report['outputs'][str(artifact.relative_to(root))] = hashlib.sha256(artifact.read_bytes()).hexdigest()
                    report['samples'].append({'case': case_name, 'intervals': intervals, 'branch': branch, 'local_boundary_balance': balance['local_boundary_balance'].tolist(), 'global_boundary_identity_error': maximum(balance['global_boundary_identity_error']), 'energy_work_identity_error': maximum(balance['full_energy_work_identity_error']), 'boundary_clock_trace_difference': (balance['variational_boundary_clocks'] - balance['physical_boundary_clocks']).tolist(), 'reaction_flux_positive_R': balance['reaction_flux_positive_R'].tolist(), 'continuum_GR_flux_positive_R': balance['continuum_GR_flux_positive_R'].tolist(), 'physical_boundary_data_changed': False, 'separate_endpoint_balance_imposed': False, 'global_balance_implies_shift_closure': False})
                    save()
        for module in tuple(sys.modules.values()):
            filename = getattr(module, '__file__', None)
            if filename:
                path = Path(filename).resolve()
                if path.parent == root / 'scripts' and path.suffix == '.py':
                    own(path)
        check('all_owned_sources_unchanged', all(hashlib.sha256((root / name).read_bytes()).hexdigest() == digest for name, digest in report['inputs'].items()))
        check('no_bytecode_cache', not (root / 'scripts/__pycache__').exists())
        report.update(passed=sum(row['passed'] for row in report['checks']), total=len(report['checks']), completed_utc=datetime.now(timezone.utc).isoformat())
        report['state'] = 'complete' if report['passed'] == report['total'] else 'failed'
        save()
        if report['state'] == 'complete':
            (destination / 'COMPLETE').write_text(report['completed_utc'] + '\n')
        print(json.dumps({key: report[key] for key in ['state', 'passed', 'total', 'completed_utc']}), flush=True)
        if report['state'] != 'complete':
            raise SystemExit(1)
    except Exception as error:
        report.update(state='failed', failure=repr(error), traceback=traceback.format_exc(), completed_utc=datetime.now(timezone.utc).isoformat())
        save()
        raise


if __name__ == '__main__':
    run()
