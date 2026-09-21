import json
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    from scipy.linalg import solve
    from annular_canonical_common_profile_refinement_20260912 import CommonProfile, RefinedContext
    from annular_canonical_trace_context_20260911 import load_archive
    from annular_canonical_rate_completion_20260911 import evaluate_initial
    from annular_canonical_trace_projection_stable_20260911 import kernel_family, trace_extension, gram_density_control

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260912'
    path = intake / 'annular-refined-kernel-load-diagnosis-attempt01.json'
    if path.exists():
        raise FileExistsError(path)
    report = {'state': 'running', 'cases': [], 'valid_for_physics_claim': False}
    common = CommonProfile(root)
    for intervals in [16, 32, 64]:
        context = RefinedContext(common, intervals, 'metric_Gram')
        initial = load_archive(intake / 'annular-common-profile-refinement-attempt01' / ('N' + str(intervals) + '_metric_Gram_initial_data.npz'))
        data, frames, completion = context.build(initial)
        baseline = evaluate_initial(frames['mass'], frames['scalar'], data, context.basis, context.weights, context.links, True, context.system.outer_clock)
        family, primitive, unused_carrier = kernel_family(context, data, frames['mass'], baseline['P_rate_coeff'])
        extended, diagnostics = trace_extension(context, frames['mass'], family)
        actual = evaluate_initial(extended, frames['scalar'], data, context.basis, context.weights, context.links, True, context.system.outer_clock)
        new_family, new_primitive, unused_carrier = kernel_family(context, data, extended, actual['P_rate_coeff'])
        coefficients, gp, controls = gram_density_control(context, data, actual, new_family, new_primitive)
        values = data['quad']
        bulk_velocity = .1 * values['N'] * values['F']**1.5 * values['pi'] * values['w']
        bulk_load = extended['quad']['p'].T @ (context.weights * gp)
        link_load = extended['quad']['p'].T @ (context.weights * bulk_velocity) - actual['mass_pair'] @ actual['mass_rate_coeff']
        load_defect = bulk_load - link_load
        load_trace = extended['nodes']['q'][[0, -1]] @ solve(actual['mass_pair'], load_defect)
        bulk_projected = solve(actual['mass_pair'], extended['quad']['p'].T @ (context.weights * (bulk_velocity - gp)))
        endpoint_bulk_velocity = .1 * data['nodes']['N'][[0, -1]] * data['nodes']['F'][[0, -1]]**1.5 * data['nodes']['pi'][[0, -1]] * data['nodes']['w'][[0, -1]]
        family_trace_defect = extended['nodes']['q'][[0, -1]] @ bulk_projected - (endpoint_bulk_velocity - new_family['nodes'][[0, -1]] @ coefficients)
        predicted = family_trace_defect + load_trace
        gap = actual['mu_t_nodes'][[0, -1]] - (endpoint_bulk_velocity - new_family['nodes'][[0, -1]] @ coefficients)
        sample = {'intervals': intervals, 'Cdot': float(abs(actual['constraint_rate']).max()), 'Pdot_change': float(abs(actual['P_t'] - baseline['P_t']).max()), 'added_Pdot_coeff': actual['P_rate_coeff'][-2:].tolist(), 'kernel_family_change': float(abs(family['quad'] - new_family['quad']).max()), 'link_log_change': float(abs(actual['endpoint_log'] - baseline['endpoint_log']).max()), 'kernel_controls': controls, 'kernel_load_defect_max': float(abs(load_defect).max()), 'kernel_load_defect_last_two': load_defect[-2:].tolist(), 'coordinate_trace_max': float(abs(extended['nodes']['q'][[0, -1]]).max()), 'added_momentum_max': float(abs(extended['quad']['p'][:, -2:]).max()), 'family_trace_defect': family_trace_defect.tolist(), 'load_trace_defect': load_trace.tolist(), 'observed_trace_defect': gap.tolist(), 'decomposition_error': float(abs(gap - predicted).max()), 'minimum_mass_momentum_rate_singular': min(completion['mass']['momentum_singular_values']), 'maximum_mass_momentum_rate_reconstruction_error': max(value for key, value in completion['mass']['rate_reconstruction_errors'].items() if key.endswith('_p'))}
        report['cases'].append(sample)
        path.write_text(json.dumps(report, indent=2) + '\n')
        print(json.dumps(sample), flush=True)
    report['state'] = 'complete'
    path.write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    run()
