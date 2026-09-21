import hashlib
import json
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    from scipy.linalg import solve
    from annular_canonical_common_profile_aligned_20260912 import CommonProfile
    from annular_cubic_lapse_boundary_fixed_20260912 import CubicContext
    from annular_canonical_trace_context_20260911 import load_archive
    from annular_gram_joint_action_20260909 import gram_matrices

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260912'
    destination = intake / 'annular-cubic-Ptrace-diagnosis-attempt01.json'
    if destination.exists():
        raise FileExistsError(destination)
    report = {'state': 'running', 'inputs': {}, 'cases': [], 'valid_for_physics_claim': False}
    common = CommonProfile(root)
    for branch in ['GR', 'metric_Gram']:
        context = CubicContext(common, branch)
        label = branch + '_corrected'
        archives = {}
        for kind in ['primary', 'higher', 'data', 'frames']:
            path = intake / 'annular-cubic-lapse-boundary-attempt02' / (label + '_' + kind + '.npz')
            report['inputs'][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
            archives[kind] = load_archive(path)
        data, frames = archives['data'], archives['frames']
        factors, sampling = gram_matrices(context.basis.radii.size)
        density = sampling.T @ (factors @ data['nodes__chi'])**2 / (2 * context.basis.spacing)
        node_force = context.basis.radii * data['nodes__N'] * density / numerical.sqrt(data['nodes__F']) if context.include_gram else numerical.zeros(context.basis.radii.size)
        for variant, surface, weights in [('primary', 'quad', context.weights), ('higher', 'check', context.check_weights)]:
            radius = data[surface + '__R']
            geometry = data[surface + '__F']
            lapse = data[surface + '__N']
            energy = data[surface + '__pi']**2 / (2 * radius**2) + radius**2 * data[surface + '__w']**2 / 2
            bulk_Pdot = lapse * energy / (radius * numerical.sqrt(geometry)) - data[surface + '__N_r'] / (.1 * numerical.sqrt(geometry)) + lapse * data[surface + '__mu'] / (.1 * radius**2 * geometry**1.5)
            mass_pair = archives[variant]['mass_pair']
            qmap = frames['mass__' + surface + '__q']
            nodal_load = frames['mass__nodes__q'].T @ node_force
            bulk_load = qmap.T @ (weights * bulk_Pdot)
            actual_load = mass_pair.T @ archives[variant]['P_rate_coeff']
            ibp_load = actual_load - bulk_load - nodal_load
            traces = frames['mass__nodes__p'][[0, -1]]
            components = {name: traces @ solve(mass_pair.T, values) for name, values in [('bulk_projection', bulk_load), ('nodal_source', nodal_load), ('quadrature_IBP', ibp_load)]}
            reconstruction = sum(components.values())
            row = {'branch': branch, 'variant': variant, 'components': {name: value.tolist() for name, value in components.items()}, 'actual': archives[variant]['P_t_nodes'][[0, -1]].tolist(), 'decomposition_error': float(abs(reconstruction - archives[variant]['P_t_nodes'][[0, -1]]).max()), 'weak_IBP_load_max': float(abs(ibp_load).max()), 'mass_pair_condition': float(numerical.linalg.cond(mass_pair))}
            report['cases'].append(row)
    report['state'] = 'complete'
    report['inputs'][str(Path(__file__).relative_to(root))] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    destination.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report['cases']), flush=True)


if __name__ == '__main__':
    run()
