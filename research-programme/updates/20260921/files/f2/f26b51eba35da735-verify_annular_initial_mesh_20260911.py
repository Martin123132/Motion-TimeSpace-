import hashlib
import json
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
    from annular_time_link_adjoint_20260911 import frozen_maps, coupled_slice_jet

    root = Path(__file__).resolve().parents[1]
    destination = root / 'source-intake/navier-stokes/20260911/annular-initial-mesh-control-attempt01'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'samples': [], 'inputs': {}, 'outputs': {}, 'valid_for_physics_claim': False, 'scope': 'Untuned zero-inner-shift-rate midpoint refinement diagnostic for both GR and metric-Gram. No interval or convergence certificate.'}

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def own(path):
        report['inputs'][str(path.relative_to(root))] = digest(path)

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    save()
    for name in [Path(__file__).name, 'annular_time_link_adjoint_20260911.py']:
        path = root / 'scripts' / name
        own(path)
        (destination / ('executed-' + name)).write_bytes(path.read_bytes())
    case_path = root / 'source-intake/navier-stokes/20260909/annular-constraint-correction-initial/canonical.json'
    own(case_path)
    constants = {name: float(symbolic.sympify(value)) for name, value in json.loads(case_path.read_text())['parameters'].items()}
    for intervals in [32, 64]:
        for branch in ['GR', 'metric_Gram']:
            label = 'canonical_N' + str(intervals) + '_' + branch + '_sample0'
            path = root / 'source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02' / (label + '.npz')
            own(path)
            print('Starting ' + label, flush=True)
            with numerical.load(path) as archive:
                saved = {name: archive[name].copy() for name in archive.files}
            basis = MixedActionBasis(saved['basis_radii'])
            count = basis.radii.size
            configuration, momenta = saved['original_configuration'], saved['original_momenta']
            packed = (saved['initial_root_box_lower'] + saved['initial_root_box_upper']) / 2
            system = ReleasedHermiteRouthian(basis, configuration[:count], configuration[count:], constants, .1, momenta[:count], momenta[count:], saved['affine_clock'][0], MetricLinkQuadrature(basis))
            try:
                maps = frozen_maps(system, packed, configuration)
                result = coupled_slice_jet(system, packed, configuration, saved['endpoint_acceleration'], maps, branch != 'GR')
                arrays = {name: value for name, value in result.items() if isinstance(value, numerical.ndarray)}
                output = destination / (label + '.npz')
                numerical.savez_compressed(output, **arrays)
                report['outputs'][str(output.relative_to(root))] = digest(output)
                row = {'label': label, 'state': 'evaluated', 'maximum_lapse_rate': float(abs(basis.node_value @ result['lapse_rate']).max()), 'maximum_shift_rate': float(abs(result['shift_speed']).max()), 'maximum_scalar_acceleration_coefficients': float(abs(result['acceleration']).max()), 'maximum_J_minus_one': float(abs(result['sources']['endpoint_jacobian'] - 1).max()), 'schur_condition': float(numerical.linalg.cond(result['schur'])), 'schur_minimum_eigenvalue': float(numerical.linalg.eigvalsh(result['schur'])[0]), 'residuals': result['residuals'], 'finite_values': all(numerical.all(numerical.isfinite(value)) for value in arrays.values())}
            except Exception as error:
                row = {'label': label, 'state': 'failed', 'error': repr(error)}
            report['samples'].append(row)
            save()
            print(json.dumps(row), flush=True)
    report['state'] = 'complete'
    report['completed_utc'] = datetime.now(timezone.utc).isoformat()
    save()


if __name__ == '__main__':
    run()
