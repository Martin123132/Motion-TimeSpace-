import argparse
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
    from annular_parent_coefficient_box_20260910 import Box
    from annular_initial_shift_jet_20260911 import initial_gr_jet, differential_controls

    parser = argparse.ArgumentParser()
    parser.add_argument('--attempt', required=True)
    parser.add_argument('--limit', type=int, default=1)
    arguments = parser.parse_args()
    if not arguments.attempt.isalnum() or arguments.limit < 1:
        raise ValueError('Use an alphanumeric new attempt and a positive limit.')
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260911'
    destination = intake / ('annular-initial-shift-jet-' + arguments.attempt)
    destination.mkdir(parents=True, exist_ok=False)
    report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': {}, 'outputs': {}, 'checks': [], 'samples': [], 'valid_for_physics_claim': False, 'full_parent_evolution_proved': False, 'Gram_initial_solution_proved': False, 'boundary_rate_selected_by_parent': False, 'scope': 'Frozen metric-seeded enriched bulk spaces. Initial GR Euler equations plus first lapse-constraint preservation. Affine family in unspecified inner shift rate, not a selected boundary condition or an evolution certificate.'}

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def own(path):
        report['inputs'][str(path.relative_to(root))] = digest(path)

    def artifact(path):
        report['outputs'][str(path.relative_to(root))] = digest(path)

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        if not passed:
            raise RuntimeError('Failed check: ' + name + ': ' + repr(detail))

    def contains_zero(value):
        return numerical.all(value.lo <= 0) and numerical.all(value.hi >= 0)

    save()
    try:
        prior_path = root / 'source-intake/navier-stokes/20260910/annular-joint-weak-action-final-integrity.json'
        prior = json.loads(prior_path.read_text())
        own(prior_path)
        for table in ['inputs', 'outputs']:
            for name, expected in prior[table].items():
                check_value = digest(root / name)
                if check_value != expected:
                    raise RuntimeError('Changed inherited evidence: ' + name)
                report['inputs'][name] = expected
        check('inherited_final_seal_and_hashes', prior['state'] == 'complete', len(report['inputs']))
        for name in ['annular_initial_shift_jet_20260911.py', Path(__file__).name]:
            path = root / 'scripts' / name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
            copy = destination / ('executed-' + name)
            copy.write_bytes(path.read_bytes())
            artifact(copy)
        case_path = root / 'source-intake/navier-stokes/20260909/annular-constraint-correction-initial/canonical.json'
        own(case_path)
        constants = {name: float(symbolic.sympify(value)) for name, value in json.loads(case_path.read_text())['parameters'].items()}
        roots_path = root / 'source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02/status.json'
        own(roots_path)
        samples = [sample for sample in json.loads(roots_path.read_text())['samples'] if sample['branch'] == 'GR' and sample['label'].endswith('_sample0')][:arguments.limit]
        for sample in samples:
            label = sample['label']
            report['active_sample'] = label
            save()
            print('Starting ' + label, flush=True)
            path = roots_path.parent / (label + '.npz')
            own(path)
            with numerical.load(path) as archive:
                saved = {name: archive[name].copy() for name in archive.files}
            basis = MixedActionBasis(saved['basis_radii'])
            links = MetricLinkQuadrature(basis)
            count = basis.radii.size
            configuration, momenta, clock = saved['original_configuration'], saved['original_momenta'], saved['affine_clock'][0]
            system = ReleasedHermiteRouthian(basis, configuration[:count], configuration[count:], constants, .1, momenta[:count], momenta[count:], clock, links)
            maps_equal = all(numerical.array_equal(value, numerical.asarray(getattr(basis, name[6:]))) for name, value in saved.items() if name.startswith('basis_'))
            maps_equal = maps_equal and all(numerical.array_equal(value, getattr(links, name[6:])) for name, value in saved.items() if name.startswith('links_'))
            check(label + '_original_maps_preserved', maps_equal)
            packed = Box(saved['initial_root_box_lower'], saved['initial_root_box_upper'])
            data = initial_gr_jet(system, packed, configuration, Box(clock), saved['endpoint_acceleration'])
            for name, diagnostic in data['diagnostics'].items():
                check(label + '_' + name + '_verified_inverse', diagnostic['componentwise_majorant_verified'] and diagnostic['contraction'] < 1, diagnostic)
            for name in ['mass_residual', 'mass_parameter_residual', 'scalar_residual', 'lapse_residual', 'shift_residual', 'boundary_trace_residual']:
                check(label + '_' + name + '_contains_zero', contains_zero(data[name]), float(data[name].magnitude.max()))
            controls = [differential_controls(system, packed, configuration, data, rate) for rate in [0., .001, -.001]]
            for control in controls:
                check(label + '_independent_action_time_derivative_' + str(control['boundary_rate']), max(control['scalar_EL_midpoint_error'], control['mass_EL_midpoint_error'], control['lapse_preservation_midpoint_error']) < 1e-8, control)
            arrays = {}
            for name, value in data.items():
                if isinstance(value, Box):
                    arrays[name + '_lower'], arrays[name + '_upper'] = value.lo, value.hi
                elif isinstance(value, numerical.ndarray):
                    arrays[name] = value
            output = destination / (label + '.npz')
            numerical.savez_compressed(output, **arrays)
            with numerical.load(output) as archive:
                check(label + '_archive_roundtrip', set(archive.files) == set(arrays) and all(numerical.array_equal(archive[name], value) for name, value in arrays.items()))
            artifact(output)
            row = {'label': label, 'diagnostics': data['diagnostics'], 'controls': controls, 'coupled_matrix_condition_midpoint': float(numerical.linalg.cond(data['coupled_matrix'].midpoint)), 'shift_rate_enclosure_width': float((data['shift_speed'].hi - data['shift_speed'].lo).max()), 'lapse_rate_enclosure_width': float((data['lapse_rate'].hi - data['lapse_rate'].lo).max()), 'inner_mass_reaction_affine_midpoint': data['inner_mass_reaction'].midpoint.tolist(), 'frozen_basis': True, 'initial_jet_family_verified': True, 'evolution_proved': False}
            report['samples'].append(row)
            print(json.dumps(row), flush=True)
            save()
        for module in tuple(sys.modules.values()):
            filename = getattr(module, '__file__', None)
            if filename:
                path = Path(filename).resolve()
                if path.parent == root / 'scripts' and path.suffix == '.py':
                    own(path)
        check('no_new_python_cache', not (root / 'scripts/__pycache__').exists())
        protected = root.parent / 'formalization-workbench'
        start = datetime.fromisoformat(report['started_utc']).timestamp()
        touched = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start]
        check('frozen_workbench_mtime_gate', not touched, touched)
        report['state'] = 'complete'
        report['completed_utc'] = datetime.now(timezone.utc).isoformat()
        report.pop('active_sample', None)
        save()
        print('Complete: ' + str(len(report['checks'])) + ' checks', flush=True)
    except Exception as error:
        report['state'] = 'failed'
        report['error'] = repr(error)
        report['traceback'] = traceback.format_exc()
        save()
        raise


if __name__ == '__main__':
    run()
