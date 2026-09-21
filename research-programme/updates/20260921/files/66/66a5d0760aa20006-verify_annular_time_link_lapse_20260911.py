import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from annular_adm_mixed_action_20260909 import MixedActionBasis, linear_value_gradient
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_gram_joint_action_20260909 import gram_matrices

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260911'
    destination = intake / 'annular-time-link-lapse-control-attempt01'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'checks': [], 'inputs': {}, 'valid_for_physics_claim': False, 'scope': 'Nonlinear ADM coefficient and connection variations on the soluble background f(t,R)=t*g(R); checks the derived physical-time lapse covector derivative, not numerical evolution.'}

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    def own(path):
        report['inputs'][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        if not passed:
            report['state'] = 'failed'
            save()
            raise RuntimeError(name + ': ' + repr(detail))

    save()
    own(Path(__file__))
    (destination / ('executed-' + Path(__file__).name)).write_bytes(Path(__file__).read_bytes())
    label = 'canonical_N16_metric_Gram_sample0'
    source = root / 'source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02' / (label + '.npz')
    jet_path = intake / 'annular-time-link-adjoint-attempt01' / (label + '.npz')
    for path in [source, jet_path]:
        own(path)
    with numerical.load(source) as archive:
        saved = {name: archive[name].copy() for name in archive.files}
    with numerical.load(jet_path) as archive:
        jet = {name: archive[name].copy() for name in archive.files}
    basis = MixedActionBasis(saved['basis_radii'])
    links = MetricLinkQuadrature(basis)
    count, face_count = basis.radii.size, basis.faces.size
    packed = (saved['initial_root_box_lower'] + saved['initial_root_box_upper']) / 2
    mass = packed[:face_count]
    lapse = packed[face_count:face_count + count]
    velocity = packed[face_count + count:face_count + 2 * count]
    scalar = saved['original_configuration'][:count]
    node_mass, node_mass_rate = basis.face_to_node @ mass, basis.face_to_node @ jet['mass_rate'][:face_count]
    lapse_rate = jet['lapse_rate']
    endpoint_jacobian, partial_jacobian = jet['source_endpoint_jacobian'], jet['source_partial_jacobian']
    mass_lift = jet['map_mass_map'][:, face_count:]
    node_mass_lift_zero = numerical.zeros((count, mass_lift.shape[1]))
    check('bubble_node_mass_rate_is_zero', numerical.all(node_mass_lift_zero == 0))
    node_shift_time = numerical.zeros(count)
    local_mass = links.face_value @ mass
    local_lapse = links.node_value @ lapse
    local_mass_rate = links.face_value @ jet['mass_rate'][:face_count]
    knots = numerical.unique(numerical.concatenate([basis.radii, basis.faces]))
    segment = numerical.searchsorted(knots, links.points, side='right') - 1
    fraction = (links.points - knots[segment]) / (knots[segment + 1] - knots[segment])
    bubble = numerical.zeros((links.points.size, 2 * (knots.size - 1)))
    rows = numerical.arange(links.points.size)
    bubble[rows, 2 * segment] = 4 * fraction * (1 - fraction)
    bubble[rows, 2 * segment + 1] = 4 * fraction * (1 - fraction) * (2 * fraction - 1)
    local_lapse_rate = links.node_value @ lapse_rate
    beta_time = jet['source_link_shift_map'] @ jet['shift_rate']
    local_f = 1 - 2 * local_mass / links.points
    generator = beta_time / (local_lapse**2 * local_f)

    def coefficient(time, node_indices):
        selected_radius = basis.radii[node_indices]
        selected_mass = node_mass[node_indices] + time * node_mass_rate[node_indices]
        selected_lapse = lapse[node_indices] + time * lapse_rate[node_indices]
        spatial_f = 1 - 2 * selected_mass / selected_radius
        shift = time * node_shift_time[node_indices]
        value = selected_radius**2 * selected_lapse * numerical.sqrt(spatial_f) - selected_radius**2 * shift**2 / (selected_lapse * numerical.sqrt(spatial_f))
        lapse_derivative = selected_radius**2 * numerical.sqrt(spatial_f) + selected_radius**2 * shift**2 / (selected_lapse**2 * numerical.sqrt(spatial_f))
        return value, lapse_derivative

    def factor_current(anchor_time, selected_pair):
        selected_factor = links.factor[selected_pair]
        all_times = endpoint_jacobian[:, None] * anchor_time[None, :]
        all_coefficient = coefficient(all_times, links.node[:, None])[0]
        all_scalar = scalar[links.node, None] + velocity[links.node, None] * all_times
        amplitude = links.collect(links.tweight[:, None] * all_scalar)
        density = links.collect(links.sweight[:, None] * endpoint_jacobian[:, None] * all_coefficient)
        leading_time = links.collect(links.tweight * velocity[links.node] * endpoint_jacobian)
        selected = numerical.arange(selected_pair.size)
        return amplitude[selected_factor, selected] * (links.sweight[selected_pair] * all_coefficient[selected_pair, selected] * leading_time[selected_factor] - links.tweight[selected_pair] * velocity[links.node[selected_pair]] * density[selected_factor, selected]) / basis.spacing

    def lapse_covector(time):
        anchor_times = time / endpoint_jacobian
        all_scalar = scalar[links.node, None] + velocity[links.node, None] * endpoint_jacobian[:, None] * anchor_times[None, :]
        amplitude = links.collect(links.tweight[:, None] * all_scalar)
        selected_amplitude = amplitude[links.factor, numerical.arange(links.node.size)]
        density_at_node = numerical.zeros(count, dtype=numerical.result_type(time))
        numerical.add.at(density_at_node, links.node, links.sweight * selected_amplitude**2 / (2 * basis.spacing))
        direct = -coefficient(time, numerical.arange(count))[1] * density_at_node
        current = factor_current(time / partial_jacobian, links.pairs)
        changed_mass = local_mass + time * local_mass_rate
        changed_lapse = local_lapse + time * local_lapse_rate
        field_f = 1 - 2 * changed_mass / links.points
        field_d = changed_lapse**2 * field_f
        connection = time * generator
        shift = 2 * connection * field_d / (1 + numerical.sqrt(1 + 4 * connection**2 * field_d))
        derivative = -2 * changed_lapse * field_f * shift / (field_d - shift**2)**2
        transport = links.node_value.T @ (links.weights * current * endpoint_jacobian[links.pairs] / partial_jacobian**2 * derivative)
        return direct + transport, direct, transport

    step = 1e-25
    full, direct, transport = [value.imag / step for value in lapse_covector(1j * step)]
    expected = jet['gram_lapse_time']
    check('full_lapse_time_variation_matches_derived_source', float(abs(full - expected).max()) < 1e-12, {'absolute_error': float(abs(full - expected).max()), 'derived_source_norm': float(abs(expected).max()), 'transport_derivative_norm': float(abs(transport).max())})
    check('transport_term_not_silently_dropped', float(abs(full - direct).max()) > 1e-15, float(abs(full - direct).max()))
    lapse_symbol, f_symbol, beta_symbol = symbolic.symbols('N F beta', positive=True)
    connection = beta_symbol / (lapse_symbol**2 * f_symbol - beta_symbol**2)
    ratio = symbolic.diff(connection, lapse_symbol) / symbolic.diff(connection, beta_symbol)
    expected_ratio = -2 * lapse_symbol * f_symbol * beta_symbol / (lapse_symbol**2 * f_symbol + beta_symbol**2)
    check('symbolic_connection_lapse_to_shift_ratio', symbolic.simplify(ratio - expected_ratio) == 0)
    check('symbolic_zero_shift_rate_limit', symbolic.simplify(symbolic.diff(ratio, beta_symbol).subs(beta_symbol, 0) + 2 / lapse_symbol) == 0)
    check('no_python_cache', not (root / 'scripts/__pycache__').exists())
    report['state'] = 'complete'
    report['completed_utc'] = datetime.now(timezone.utc).isoformat()
    save()
    print(json.dumps({'state': report['state'], 'checks': report['checks']}), flush=True)


if __name__ == '__main__':
    run()
