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
    from annular_canonical_nodal_data_20260911 import CanonicalInitialNodalData
    from annular_canonical_boundary_20260911 import wronskian_tent

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260911'
    destination = intake / 'annular-canonical-independent-control-attempt01'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'inputs': {}, 'checks': [], 'near_null_modes': [], 'valid_for_physics_claim': False}

    def own(path):
        report['inputs'][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    own(Path(__file__))
    (destination / ('executed-' + Path(__file__).name)).write_bytes(Path(__file__).read_bytes())
    roots = root / 'source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02'
    for size in [16, 32, 64]:
        for branch in ['GR', 'metric_Gram']:
            label = 'canonical_N' + str(size) + '_' + branch + '_sample0'
            source = roots / (label + '.npz')
            old_path = intake / ('annular-time-link-adjoint-attempt01' if size == 16 else 'annular-initial-mesh-control-attempt01') / (label + '.npz')
            own(source)
            own(old_path)
            with numerical.load(source) as archive:
                radii = archive['basis_radii']
                faces = archive['basis_faces']
                packed = (archive['initial_root_box_lower'] + archive['initial_root_box_upper']) / 2
            with numerical.load(old_path) as archive:
                eigenvalues, eigenvectors = numerical.linalg.eigh(archive['schur'])
            count, face_count = radii.size, faces.size
            lapse = packed[face_count:face_count + count]
            velocity = packed[face_count + count:face_count + 2 * count]
            peak = 1 + int(abs(velocity[1:-1]).argmin())
            tent, primitive = wronskian_tent(radii, lapse, peak)
            wronskian = (lapse[:-1] * tent[1:] - tent[:-1] * lapse[1:]) / numerical.diff(radii)
            jumps = velocity[1:-1] / lapse[1:-1]**2 * numerical.diff(wronskian)
            alignment = float(abs(tent @ eigenvectors[:, 0]) / numerical.linalg.norm(tent))
            check(label + '_kinematic_tent_not_residual_fit', abs(numerical.delete(jumps, peak - 1)).max() < 1e-9 and tent[0] == 0 and tent[-1] == 0)
            report['near_null_modes'].append({'label': label, 'tent_alignment': alignment, 'peak_radius': float(radii[peak]), 'q_at_peak': float(velocity[peak]), 'product_derivative_jump_at_peak': float(jumps[peak - 1]), 'smallest_schur_eigenvalue_midpoint': float(eigenvalues[0])})
    label = 'canonical_N16_GR_sample0'
    source, output = roots / (label + '.npz'), intake / 'annular-canonical-initial-data-nodal01' / (label + '.npz')
    own(source)
    own(output)
    with numerical.load(source) as archive:
        saved = {name: archive[name].copy() for name in archive.files}
    with numerical.load(output) as archive:
        constructed = {name: archive[name].copy() for name in archive.files}
    case_path = root / 'source-intake/navier-stokes/20260909/annular-constraint-correction-initial/canonical.json'
    own(case_path)
    constants = {name: float(symbolic.sympify(value)) for name, value in json.loads(case_path.read_text())['parameters'].items()}
    basis = MixedActionBasis(saved['basis_radii'])
    count = basis.radii.size
    configuration, momenta = saved['original_configuration'], saved['original_momenta']
    packed = (saved['initial_root_box_lower'] + saved['initial_root_box_upper']) / 2
    system = ReleasedHermiteRouthian(basis, configuration[:count], configuration[count:], constants, .1, momenta[:count], momenta[count:], saved['affine_clock'][0], MetricLinkQuadrature(basis))
    model = CanonicalInitialNodalData(system, packed, configuration, False, constructed['boundary_velocity'])
    unused_mass, unused_pi, reactions = model.set_state(constructed['state'])
    result = model.evaluate(numerical.concatenate([model.fixed_lapse, reactions]))
    mass_time = model.maps['mass_map'] @ result['mass_rate']
    mass_gradient_time = model.maps['mass_gradient'] @ result['mass_rate']
    momentum_time = model.momentum_map @ result['momentum_rate']
    pi_time = model.pi_map @ result['pi_rate']
    gradient_time = model.gradient @ result['scalar_velocity']

    def full_bulk_constraint(time):
        mass = model.mass_q + time * mass_time
        mass_r = model.mass_r + time * mass_gradient_time
        pi = model.pi + time * pi_time
        momentum = time * momentum_time
        gradient = model.scalar_gradient + time * gradient_time
        spatial_f = 1 - 2 * mass / model.radius
        scale_r = (mass_r / model.radius - mass / model.radius**2) * spatial_f**-1.5
        density = mass_r / (.1 * numerical.sqrt(spatial_f)) - numerical.sqrt(spatial_f) * (pi**2 / (2 * model.radius**2) + model.radius**2 * gradient**2 / 2)
        density -= .1 * spatial_f**1.5 * momentum * pi * gradient
        density -= .1 * model.radius * spatial_f**3 * scale_r * momentum**2 / 2
        gradient_density = -.1 * model.radius * spatial_f**2.5 * momentum**2 / 2
        return basis.node_value.T @ (model.weights * density) + basis.node_gradient.T @ (model.weights * gradient_density)

    independent = full_bulk_constraint(1e-25j).imag / 1e-25
    check('GR_full_canonical_action_constraint_time_derivative', abs(independent - result['constraint_rate']).max() < 1e-12, float(abs(independent - result['constraint_rate']).max()))
    actual_boundary_velocity = numerical.array([result['mass_rate'][0], result['scalar_velocity'][0], result['scalar_velocity'][count - 1]])
    boundary_power = float(reactions @ actual_boundary_velocity)
    outer_power = float(system.outer_clock * result['mass_rate'][system.face_count - 1] / .1)
    constraint_work = float(model.fixed_lapse @ result['constraint_rate'])
    check('GR_boundary_energy_balance_without_new_clock_law', abs(outer_power - boundary_power - constraint_work) < 1e-12, {'outer_mass_power': outer_power, 'boundary_reaction_power': boundary_power, 'constraint_work': constraint_work, 'error': abs(outer_power - boundary_power - constraint_work)})
    radius, lapse, field_f, kappa = symbolic.symbols('R N F kappa', positive=True)
    momentum = symbolic.symbols('P', real=True)
    connection = kappa * symbolic.sqrt(field_f) * momentum / (lapse * (1 - kappa**2 * field_f**2 * momentum**2))
    ratio = symbolic.diff(connection, lapse) / symbolic.diff(connection, momentum)
    check('canonical_Gram_lapse_transport_chain_rule', symbolic.simplify(symbolic.diff(ratio, momentum).subs(momentum, 0) + 1 / lapse) == 0)
    check('no_python_cache', not (root / 'scripts/__pycache__').exists())
    report['state'] = 'complete'
    report['completed_utc'] = datetime.now(timezone.utc).isoformat()
    (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'state': report['state'], 'checks': report['checks'], 'near_null_modes': report['near_null_modes']}), flush=True)


if __name__ == '__main__':
    run()
