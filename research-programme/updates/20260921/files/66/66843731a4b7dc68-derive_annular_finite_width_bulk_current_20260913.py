import hashlib
import json
import sys
import traceback
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as np
    import sympy as sp
    from annular_finite_width_bulk_current_20260913 import FiniteWidthBulk

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260913'
    destination = intake / 'annular-finite-width-bulk-current-attempt01'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'checks': [], 'inputs': {}, 'outputs': {}, 'cases': [],
              'valid_for_physics_claim': False, 'full_first_jet_closed': False,
              'full_GR_limit_proven': False, 'full_physical_radial_port_action_signed': False,
              'unique_parent_regularizer_derived': False, 'new_spacetime_evolution': False,
              'old_boundary_drives_transferred': False, 'source_extension_parent_selected': False,
              'pilot_shared_metric_bulk_initial_data': True, 'matched_compact_tolerance': 1e-10,
              'unchanged_h_Gram_weights_and_old_evidence': True,
              'source_extension': 'Layer-linear or layer-flat initial profiles from archived canonical79 node values; not a unique parent choice. Off-layer gaps have no new scalar kinetic field. Layer variations remain allowed.',
              'lapse': 'Common manufactured positive lapse .85*exp(slope*(R-r0)); slope 0 or .1. Not old physical clock ports.',
              'left_mass': 'Archived first-node mass assigned to the enlarged left endpoint as new pilot initial condition, not claimed to reproduce the old global solution.'}

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
        previous_path = intake / 'annular-finite-width-full-scalar-final-integrity.json'
        previous = json.loads(previous_path.read_text())
        check('previous_action_seal_complete_without_full_jet_promotion', previous['state'] == 'complete' and previous['full_first_jet_closed'] is False)
        for table in ['inputs', 'outputs']:
            for filename, expected in previous[table].items():
                if filename in report['inputs']:
                    if report['inputs'][filename] != expected:
                        raise RuntimeError('Conflicting inherited hash: ' + filename)
                    continue
                if hashlib.sha256((root / filename).read_bytes()).hexdigest() != expected:
                    raise RuntimeError('Changed inherited evidence: ' + filename)
                report['inputs'][filename] = expected
        own(previous_path)
        for path in [Path(__file__), root / 'scripts/annular_finite_width_bulk_current_20260913.py']:
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
            snapshot = destination / ('executed-' + path.name)
            snapshot.write_bytes(path.read_bytes())
            own(snapshot, 'outputs')
        radius, mass, density, coupling, lapse, lapse_r, kernel, kernel_r, density_t = sp.symbols('R mu epsilon kappa N N_R K K_R epsilon_t', positive=True)
        root_f = sp.sqrt(1 - 2 * mass / radius)
        mass_r = coupling * root_f**2 * density
        root_r = sp.diff(root_f, radius) + sp.diff(root_f, mass) * mass_r
        generator = -lapse_r / lapse + mass / (radius**2 * root_f**2) + coupling * density / radius
        mass_t = -coupling * root_f * kernel / lapse
        mass_tr = -coupling * ((root_r / lapse - root_f * lapse_r / lapse**2) * kernel + root_f * kernel_r / lapse)
        direct_c1 = mass_tr / (coupling * root_f) + mass_r * mass_t / (coupling * radius * root_f**3) + density * mass_t / (radius * root_f) - root_f * density_t
        full_c1 = direct_c1 - kernel * generator / lapse
        check('symbolic_full_C1_equals_scalar_power_Ward', sp.simplify(full_c1 + (kernel_r + 2 * generator * kernel + lapse * root_f * density_t) / lapse) == 0)
        check('symbolic_missing_transport_not_zero', sp.simplify((direct_c1 - full_c1) - kernel * generator / lapse) == 0)
        cases = [(1 / 128, 'beta22', .1, 'linear'), (1 / 256, 'beta22', .1, 'linear'),
                 (1 / 128, 'beta23', .1, 'linear'), (1 / 128, 'beta22', 0., 'linear'),
                 (1 / 128, 'beta22', .1, 'flat')]
        for branch in ['GR', 'metric_Gram']:
            source_path = root / 'source-intake/navier-stokes/20260912/annular-interface-layer-clock-attempt03' / (branch + '_source_snapshot.npz')
            with np.load(source_path, allow_pickle=False) as archive:
                source = {key: archive[key].copy() for key in archive.files}
            own(source_path)
            for index, (width, shape, slope, extension) in enumerate(cases):
                name = branch + '_' + str(index)
                model = FiniteWidthBulk(source, branch != 'GR', width, shape, slope, extension)
                check(name + '_same_parent_stencil', np.array_equal(model.factors, source['factors']) and np.array_equal(model.sampling, source['sampling']))
                zero = model.initial_scalar([0.])
                check(name + '_source_values_recovered_without_fits', max(abs(zero['chi'][0] - source['scalar']).max(), abs(zero['p'][0] - source['momentum']).max(), abs(zero['energy'][0] - source['energy']).max()) < 1e-14)
                primary, fit = model.compact_checks(degree=28, order=24)
                higher, higher_fit = model.compact_checks(degree=40, order=36)
                offsets = np.array([-.49, -.231, .0, .117, .49])
                stencil = model.stencil(offsets)
                anchor_error = max(abs(np.sum((stencil['J'] * stencil['I'])[:, model.factor == factor], axis=1)).max() for factor in range(len(model.factors)))
                power_error = abs(stencil['fields']['N'] * stencil['fields']['U'] * stencil['energy1'] - stencil['power']).max()
                check(name + '_anchor_cancellation_and_live_power', max(anchor_error, power_error) < 1e-12)
                probes = model.radii[[0, 3, 8, 12, 16]] + width * np.array([-.17, .23, -.29, .41, .09])
                direct = np.array([model.direct_flux(radius) for radius in probes])
                fitted = model.flux(probes, higher_fit)[0]
                direct_error = float(abs(direct - fitted).max())
                check(name + '_independent_oriented_link_integral', direct_error < 1e-11, direct_error)
                check(name + '_finite_arrays_positive_chart', all(np.isfinite(value).all() for value in higher.values()) and min(higher['U'].min(), higher['N'].min(), stencil['J'].min()) > 0)
                check(name + '_local_current_Ward_identity', abs(higher['ward']).max() < 1e-10, float(abs(higher['ward']).max()))
                check(name + '_higher_quadrature_agreement', max(abs(higher[key] - primary[key]).max() for key in ['C0', 'C1']) < 1e-10)
                row = {'branch': branch, 'case': index, 'width': width, 'shape': shape, 'lapse_slope': slope, 'extension': extension,
                       'C0_primary_max': float(abs(primary['C0']).max()), 'C1_primary_max': float(abs(primary['C1']).max()),
                       'C0_higher_max': float(abs(higher['C0']).max()), 'C1_higher_max': float(abs(higher['C1']).max()),
                       'compact_bulk_C0_C1_pass': bool(max(abs(primary['C0']).max(), abs(primary['C1']).max(), abs(higher['C0']).max(), abs(higher['C1']).max()) < 1e-10),
                       'local_Ward_max': float(abs(higher['ward']).max()), 'independent_current_integral_max': direct_error,
                       'minimum_F': float(higher['U'].min()**2), 'minimum_J': float(stencil['J'].min()),
                       'maximum_P1': float(abs(higher['P1']).max()), 'maximum_mass_rate': float(abs(higher['mu1']).max()),
                       'missing_transport_C1_max': float(abs(higher['missing_transport_C1']).max()),
                       'missing_J_C1_max': float(abs(higher['missing_J_C1']).max()),
                       'old_boundary_drives_transferred': False, 'valid_for_physics_claim': False,
                       'initial_mass_left': float(source['mu'][0]), 'initial_mass_right': model.final_mass, 'ode_steps': model.steps}
                report['cases'].append(row)
                for label, arrays in [('primary', primary), ('higher', higher)]:
                    path = destination / (name + '_' + label + '.npz')
                    np.savez_compressed(path, **arrays)
                    own(path, 'outputs')
                path = destination / (name + '_initial_source_and_flux.npz')
                np.savez_compressed(path, edges=model.edges, radii=model.radii, scalar=model.scalar, momentum=model.momentum,
                                    scalar_slope=model.scalar_slope, momentum_slope=model.momentum_slope,
                                    flux_coefficients=higher_fit[0], flux_primitive=higher_fit[1], offsets=offsets,
                                    scalar_rate=stencil['q'], momentum_rate=stencil['p1'], J=stencil['J'])
                own(path, 'outputs')
                save()
                print(json.dumps(row), flush=True)
        check('matched_matrix_complete', len(report['cases']) == 10)
        report['all_compact_bulk_tests_pass'] = all(row['compact_bulk_C0_C1_pass'] for row in report['cases'])
        check('negative_controls_detect_missing_transport_and_J', all(row['missing_transport_C1_max'] > 1e-10 and row['missing_J_C1_max'] > 1e-10 for row in report['cases']))
        for module in tuple(sys.modules.values()):
            filename = getattr(module, '__file__', None)
            if filename:
                path = Path(filename).resolve()
                if path.parent == root / 'scripts' and path.suffix == '.py':
                    own(path)
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        report['state'] = 'complete'
        save()
    except Exception as error:
        report.update({'state': 'failed', 'error': repr(error), 'traceback': traceback.format_exc()})
        save()
        raise


if __name__ == '__main__':
    run()
